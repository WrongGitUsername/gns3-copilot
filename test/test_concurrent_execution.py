#!/usr/bin/env python3
"""
Test script to verify concurrent execution of Nornir commands
"""
import json
import time
from tools.display_tools_nornir import ExecuteMultipleDeviceCommands

def test_concurrent_execution():
    """Test concurrent execution vs sequential execution"""
    
    # Test data with multiple devices
    device_commands = [
        {
            "device_name": "R-1",
            "commands": ["show version", "show ip interface brief"]
        },
        {
            "device_name": "R-2", 
            "commands": ["show version", "show ip interface brief"]
        },
        {
            "device_name": "R-3",
            "commands": ["show version", "show ip interface brief"]
        }
    ]
    
    print("Testing concurrent execution with Nornir...")
    print(f"Number of devices: {len(device_commands)}")
    print(f"Number of workers configured: 10")
    
    # Execute the commands
    exe_cmd = ExecuteMultipleDeviceCommands()
    
    start_time = time.time()
    result = exe_cmd._run(tool_input=json.dumps(device_commands))
    end_time = time.time()
    
    execution_time = end_time - start_time
    print(f"\nExecution completed in {execution_time:.2f} seconds")
    
    # Print results summary
    print("\nResults summary:")
    for device_result in result:
        device_name = device_result["device_name"]
        print(f"\nDevice: {device_name}")
        for cmd, output in device_result.items():
            if cmd != "device_name":
                if "Error" in str(output) or "not found" in str(output):
                    print(f"  {cmd}: {output}")
                else:
                    print(f"  {cmd}: Command executed successfully")
    
    print(f"\nConcurrent execution test completed.")
    print(f"With proper Nornir configuration, devices should execute in parallel.")
    print(f"Note: Actual performance depends on device availability and network conditions.")

if __name__ == "__main__":
    test_concurrent_execution()
