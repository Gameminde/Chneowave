# Minimal ctypes wrapper for Measurement Computing Universal Library (cbw64.dll)
import os
import sys
import ctypes
from ctypes import wintypes

# Try to ensure DLL path on Windows
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
_last_error = None
if os.name == 'nt':
    try:
        _cb = ctypes.WinDLL('cbw64.dll')
    except Exception as e:
        _last_error = e
else:
    _last_error = RuntimeError('Only supported on Windows with cbw64.dll installed')

# UL constants (minimal subset)
BIP10VOLTS = 1
BIP5VOLTS = 0
BIP2VOLTS = 2
BIP1VOLTS = 3
BIPPT5VOLTS = 4
BIPPT25VOLTS = 5

# Error codes
NOERRORS = 0

# Define prototypes (subset)
if _cb is not None:
    # int cbGetBoardName(int BoardNum, char* BoardName)
    _cb.cbGetBoardName.argtypes = [ctypes.c_int, ctypes.c_char_p]
    _cb.cbGetBoardName.restype = ctypes.c_int

    # int cbAIn(int BoardNum, int Chan, int Gain, unsigned short* DataValue)
    _cb.cbAIn.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.POINTER(ctypes.c_ushort)]
    _cb.cbAIn.restype = ctypes.c_int

    # int cbToEngUnits(int BoardNum, int Range, unsigned short DataVal, float* EngUnits)
    _cb.cbToEngUnits.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_ushort, ctypes.POINTER(ctypes.c_float)]
    _cb.cbToEngUnits.restype = ctypes.c_int


def last_error():
    return _last_error


def is_available() -> bool:
    return _cb is not None


def get_board_names(max_boards: int = 32):
    """Return list of tuples (board_num, name) configured in InstaCal."""
    if _cb is None:
        raise RuntimeError(f"cbw64.dll not available: {last_error()}")
    names = []
    for b in range(max_boards):
        buf = ctypes.create_string_buffer(256)
        try:
            err = _cb.cbGetBoardName(ctypes.c_int(b), buf)
            if err == NOERRORS and buf.value:
                names.append((b, buf.value.decode(errors='ignore')))
        except Exception:
            # invalid board number typically raises UL error internally; ignore
            continue
    return names


def ain_volts(board: int, chan: int = 0, rng: int = BIP10VOLTS) -> float:
    """Read single-ended analog value in volts using cbAIn + cbToEngUnits."""
    if _cb is None:
        raise RuntimeError(f"cbw64.dll not available: {last_error()}")
    data = ctypes.c_ushort(0)
    err = _cb.cbAIn(ctypes.c_int(board), ctypes.c_int(chan), ctypes.c_int(rng), ctypes.byref(data))
    if err != NOERRORS:
        raise RuntimeError(f"cbAIn error {err}")
    volts = ctypes.c_float(0.0)
    err = _cb.cbToEngUnits(ctypes.c_int(board), ctypes.c_int(rng), data, ctypes.byref(volts))
    if err != NOERRORS:
        raise RuntimeError(f"cbToEngUnits error {err}")
    return float(volts.value)
