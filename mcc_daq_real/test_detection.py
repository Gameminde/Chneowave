#!/usr/bin/env python3
"""
Test script to validate MCC DAQ detection and basic functionality
WITHOUT GUI - pure console output for debugging
"""
import sys
import time
from ul_wrapper import get_board_names, ain_volts, is_available
from ul_scan_wrapper import AInScanManager

def test_dll_availability():
    """Test if cbw64.dll is available"""
    print("=== Test DLL Availability ===")
    available = is_available()
    print(f"cbw64.dll available: {available}")
    return available

def test_board_detection():
    """Test board detection via InstaCal"""
    print("\n=== Test Board Detection ===")
    try:
        boards = get_board_names()
        print(f"Boards found: {len(boards)}")
        for board_num, name in boards:
            print(f"  Board {board_num}: {name}")
        return boards
    except Exception as e:
        print(f"Error detecting boards: {e}")
        return []

def test_single_read(board_num, channel=0, range_val=1):
    """Test single analog read"""
    print(f"\n=== Test Single Read (Board {board_num}, Channel {channel}) ===")
    try:
        voltage = ain_volts(board_num, channel, range_val)
        print(f"Voltage read: {voltage:.6f} V")
        return True
    except Exception as e:
        print(f"Error reading voltage: {e}")
        return False

def test_scan_manager(board_num, channel=0, range_val=1, freq=1000):
    """Test AInScan hardware-timed acquisition"""
    print(f"\n=== Test AInScan (Board {board_num}, Channel {channel}, {freq} Hz) ===")
    
    scan_mgr = AInScanManager()
    if not scan_mgr.is_available():
        print("AInScan manager not available")
        return False
        
    try:
        # Start scan
        success = scan_mgr.start_scan(board_num, channel, range_val, freq, 1000)
        if not success:
            print("Failed to start scan")
            return False
            
        print(f"Scan started at {scan_mgr.get_actual_rate()} Hz")
        
        # Collect data for 3 seconds
        for i in range(6):  # 6 * 0.5s = 3s
            time.sleep(0.5)
            voltages, num_points = scan_mgr.get_data(100)
            if num_points > 0:
                avg_v = sum(voltages) / len(voltages)
                min_v = min(voltages)
                max_v = max(voltages)
                print(f"  {i*0.5+0.5}s: {num_points} points, avg={avg_v:.4f}V, range=[{min_v:.4f}, {max_v:.4f}]")
            else:
                print(f"  {i*0.5+0.5}s: No data available")
                
        scan_mgr.stop_scan()
        print("Scan stopped successfully")
        return True
        
    except Exception as e:
        print(f"Error in scan test: {e}")
        scan_mgr.stop_scan()
        return False

def main():
    print("MCC DAQ Detection and Functionality Test")
    print("=" * 50)
    
    # Test 1: DLL availability
    if not test_dll_availability():
        print("\nERROR: cbw64.dll not available. Install MCC InstaCal/UL.")
        return False
        
    # Test 2: Board detection
    boards = test_board_detection()
    if not boards:
        print("\nERROR: No boards detected. Check InstaCal configuration.")
        return False
        
    # Test 3: Single reads on each board
    working_boards = []
    for board_num, name in boards:
        if test_single_read(board_num):
            working_boards.append((board_num, name))
            
    if not working_boards:
        print("\nERROR: No boards respond to single reads.")
        return False
        
    print(f"\nWorking boards: {len(working_boards)}")
    
    # Test 4: AInScan on first working board
    board_num, name = working_boards[0]
    print(f"\nTesting AInScan on Board {board_num}: {name}")
    
    if test_scan_manager(board_num, channel=0, range_val=1, freq=1000):
        print(f"\n✅ SUCCESS: Board {board_num} ({name}) is fully functional!")
        print("You can now use the GUI with confidence.")
        return True
    else:
        print(f"\n⚠️  WARNING: Board {board_num} ({name}) works for single reads but AInScan failed.")
        print("GUI will work but only with basic sampling, not hardware-timed acquisition.")
        return True

if __name__ == "__main__":
    success = main()
    input("\nPress Enter to exit...")
    sys.exit(0 if success else 1)
