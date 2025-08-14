# Professional AInScan wrapper for hardware-timed acquisition
import os
import ctypes
import numpy as np
from ctypes import wintypes

# Ensure DLL path
if os.name == 'nt':
    for p in (
        r"C:\\Program Files (x86)\\Measurement Computing\\DAQ",
        r"C:\\Program Files\\Measurement Computing\\DAQ",
    ):
        if os.path.isdir(p):
            try:
                os.add_dll_directory(p)
            except Exception:
                pass

# Load cbw64.dll
_cb = None
try:
    _cb = ctypes.WinDLL('cbw64.dll')
except Exception:
    _cb = None

# Constants
NOERRORS = 0
CONTINUOUS = 0x1
BACKGROUND = 0x2
SINGLEENDED = 0x0
DIFFERENTIAL = 0x1

# Ranges
BIP10VOLTS = 1
BIP5VOLTS = 0
BIP2VOLTS = 2
BIP1VOLTS = 3

if _cb is not None:
    # int cbAInScan(int BoardNum, int LowChan, int HighChan, long Count, long* Rate, int Gain, HGLOBAL MemHandle, int Options)
    _cb.cbAInScan.argtypes = [
        ctypes.c_int,           # BoardNum
        ctypes.c_int,           # LowChan
        ctypes.c_int,           # HighChan  
        ctypes.c_long,          # Count
        ctypes.POINTER(ctypes.c_long),  # Rate
        ctypes.c_int,           # Gain
        wintypes.HGLOBAL,       # MemHandle
        ctypes.c_int            # Options
    ]
    _cb.cbAInScan.restype = ctypes.c_int

    # int cbGetStatus(int BoardNum, short* Status, long* CurCount, long* CurIndex, int FunctionType)
    _cb.cbGetStatus.argtypes = [
        ctypes.c_int,           # BoardNum
        ctypes.POINTER(ctypes.c_short),  # Status
        ctypes.POINTER(ctypes.c_long),   # CurCount
        ctypes.POINTER(ctypes.c_long),   # CurIndex
        ctypes.c_int            # FunctionType
    ]
    _cb.cbGetStatus.restype = ctypes.c_int

    # int cbStopBackground(int BoardNum, int FunctionType)
    _cb.cbStopBackground.argtypes = [ctypes.c_int, ctypes.c_int]
    _cb.cbStopBackground.restype = ctypes.c_int

    # HGLOBAL cbWinBufAlloc(long NumPoints)
    _cb.cbWinBufAlloc.argtypes = [ctypes.c_long]
    _cb.cbWinBufAlloc.restype = wintypes.HGLOBAL

    # int cbWinBufFree(HGLOBAL MemHandle)
    _cb.cbWinBufFree.argtypes = [wintypes.HGLOBAL]
    _cb.cbWinBufFree.restype = ctypes.c_int

    # int cbWinBufToArray(HGLOBAL MemHandle, unsigned short* DataArray, long FirstPoint, long Count)
    _cb.cbWinBufToArray.argtypes = [
        wintypes.HGLOBAL,
        ctypes.POINTER(ctypes.c_ushort),
        ctypes.c_long,
        ctypes.c_long
    ]
    _cb.cbWinBufToArray.restype = ctypes.c_int

    # int cbToEngUnits(int BoardNum, int Range, unsigned short DataVal, float* EngUnits)
    _cb.cbToEngUnits.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_ushort, ctypes.POINTER(ctypes.c_float)]
    _cb.cbToEngUnits.restype = ctypes.c_int


class AInScanManager:
    def __init__(self):
        self.board_num = 0
        self.channel = 0
        self.range = BIP10VOLTS
        self.sample_rate = 1000
        self.buffer_size = 1000
        self.mem_handle = None
        self.is_scanning = False
        
    def is_available(self) -> bool:
        return _cb is not None
        
    def start_scan(self, board_num: int, channel: int, range_val: int, sample_rate: int, buffer_size: int = None) -> bool:
        """Start hardware-timed continuous acquisition on single channel."""
        if not self.is_available():
            raise RuntimeError("cbw64.dll not available")
            
        if self.is_scanning:
            self.stop_scan()
            
        self.board_num = board_num
        self.channel = channel
        self.range = range_val
        self.sample_rate = sample_rate
        # Smaller buffer size to avoid memory issues
        self.buffer_size = buffer_size or min(10000, max(1000, sample_rate * 2))
        
        # Allocate buffer
        self.mem_handle = _cb.cbWinBufAlloc(ctypes.c_long(self.buffer_size))
        if not self.mem_handle:
            raise RuntimeError("Failed to allocate scan buffer")
            
        # Start scan with corrected parameters
        rate = ctypes.c_long(self.sample_rate)
        
        # Try finite scan first (safer than continuous for testing)
        err = _cb.cbAInScan(
            ctypes.c_int(self.board_num),
            ctypes.c_int(self.channel),      # LowChan
            ctypes.c_int(self.channel),      # HighChan (same = single channel)
            ctypes.c_long(self.buffer_size),
            ctypes.byref(rate),
            ctypes.c_int(self.range),
            self.mem_handle,
            BACKGROUND  # Remove CONTINUOUS for now
        )
        
        if err != NOERRORS:
            _cb.cbWinBufFree(self.mem_handle)
            self.mem_handle = None
            raise RuntimeError(f"cbAInScan failed with error {err}")
            
        self.actual_rate = rate.value
        self.is_scanning = True
        return True
        
    def get_data(self, num_points: int = None) -> tuple[np.ndarray, int]:
        """Get latest data from scan buffer. Returns (voltages, actual_points_read)."""
        if not self.is_scanning or not self.mem_handle:
            return np.array([]), 0
            
        # Get scan status
        status = ctypes.c_short(0)
        cur_count = ctypes.c_long(0)
        cur_index = ctypes.c_long(0)
        
        err = _cb.cbGetStatus(
            ctypes.c_int(self.board_num),
            ctypes.byref(status),
            ctypes.byref(cur_count),
            ctypes.byref(cur_index),
            ctypes.c_int(1)  # AIFUNCTION
        )
        
        if err != NOERRORS:
            return np.array([]), 0
            
        # Determine how many points to read
        available_points = cur_count.value
        if num_points is None:
            num_points = min(available_points, self.buffer_size // 2)
        else:
            num_points = min(num_points, available_points, self.buffer_size)
            
        if num_points <= 0:
            return np.array([]), 0
            
        # Read raw data
        raw_data = (ctypes.c_ushort * num_points)()
        start_index = max(0, cur_index.value - num_points)
        
        err = _cb.cbWinBufToArray(
            self.mem_handle,
            raw_data,
            ctypes.c_long(start_index),
            ctypes.c_long(num_points)
        )
        
        if err != NOERRORS:
            return np.array([]), 0
            
        # Convert to volts
        voltages = np.zeros(num_points, dtype=np.float32)
        for i in range(num_points):
            eng_val = ctypes.c_float(0.0)
            err = _cb.cbToEngUnits(
                ctypes.c_int(self.board_num),
                ctypes.c_int(self.range),
                raw_data[i],
                ctypes.byref(eng_val)
            )
            if err == NOERRORS:
                voltages[i] = eng_val.value
                
        return voltages, num_points
        
    def stop_scan(self):
        """Stop continuous scan and free resources."""
        if self.is_scanning:
            _cb.cbStopBackground(ctypes.c_int(self.board_num), ctypes.c_int(1))  # AIFUNCTION
            self.is_scanning = False
            
        if self.mem_handle:
            _cb.cbWinBufFree(self.mem_handle)
            self.mem_handle = None
            
    def get_actual_rate(self) -> int:
        """Get actual hardware sample rate achieved."""
        return getattr(self, 'actual_rate', self.sample_rate)
        
    def __del__(self):
        self.stop_scan()
