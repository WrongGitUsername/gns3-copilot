"""
Test script for config_tools_nornir module
"""
import json
import sys
import os

# Add the tools directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from tools.config_tools_nornir import ExecuteMultipleDeviceConfigCommands

def test_config_tools_nornir():
    """Test the ExecuteMultipleDeviceConfigCommands tool"""
    print("Testing ExecuteMultipleDeviceConfigCommands...")
    
    # Create test configuration commands
    device_configs = [
        {
            "device_name": "R-1",
            "config_commands": [
                "interface Loopback101",
                "description Test interface by config tool",
                "ip address 101.101.101.101 255.255.255.255"
            ]
        },
        {
            "device_name": "R-2",
            "config_commands": [
                "interface Loopback102",
                "description Test interface by config tool",
                "ip address 102.102.102.102 255.255.255.255"
            ]
        }
    ]
    
    # Create tool instance
    exe_config = ExecuteMultipleDeviceConfigCommands()
    
    # Execute configuration commands
    print("Executing configuration commands...")
    result = exe_config._run(tool_input=json.dumps(device_configs))
    
    # Print results
    print("Configuration execution results:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Check if any devices were successfully configured
    success_count = sum(1 for r in result if r.get("status") == "success")
    print(f"\nSuccessfully configured {success_count} out of {len(device_configs)} devices")
    
    return result

if __name__ == "__main__":
    test_config_tools_nornir()
