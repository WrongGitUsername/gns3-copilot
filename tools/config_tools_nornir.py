"""
This module provides a tool to execute configuration commands on multiple devices in a GNS3 topology using Nornir.
"""
import json
import logging
from typing import List, Dict, Any
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_netmiko.tasks import netmiko_send_config
from nornir_utils.plugins.functions import print_result
from langchain.tools import BaseTool
from .gns3_topology_reader import GNS3TopologyTool
from .logging_config import setup_tool_logger

# config log
logger = setup_tool_logger("config_tools_nornir")

# Nornir configuration groups
groups_data = {
    "cisco_IOSv_telnet": {
        "platform": "cisco_ios",
        "hostname": "127.0.0.1",
        "timeout": 120,
        "username": "",
        "password": "",
        "connection_options": {
            "netmiko": {
                "extras": {
                    "device_type": "cisco_ios_telnet"
                }
            }
        }
    }
}

defaults = {
    "data": {
        "location": "gns3"
    }
}

class ExecuteMultipleDeviceConfigCommands(BaseTool):
    """
    A tool to execute configuration commands on multiple devices in a GNS3 topology using Nornir.
    This class uses Nornir to manage connections and execute configuration commands on multiple devices concurrently.

    IMPORTANT SAFETY NOTE:
    This tool is intended for configuration changes only. Use extreme caution when executing configuration commands.
    """

    name: str = "execute_multiple_device_config_commands"
    description: str = """
    Executes CONFIGURATION commands on multiple devices in the current GNS3 topology.
    Use this tool ONLY for changing device settings (e.g., 'configure', 'interface', 'ip address', 'router ospf').
    For viewing information, use the 'execute_multiple_device_commands' tool.
    Input should be a JSON array containing device names and their respective configuration commands to execute.
    Example input:
        [
            {
                "device_name": "R-1",
                "config_commands": [
                    "interface Loopback0",
                    "ip address 1.1.1.1 255.255.255.255",
                    "description CONFIG_BY_TOOL"
                ]
            },
            {
                "device_name": "R-2", 
                "config_commands": [
                    "interface Loopback0",
                    "ip address 2.2.2.2 255.255.255.255",
                    "description CONFIG_BY_TOOL"
                ]
            }
        ]
    Returns a list of dictionaries, each containing the device name and configuration results.

    IMPORTANT SAFETY WARNING: 
    Do NOT use this tool for dangerous operations that could reboot, erase, or factory-reset devices.
    Forbidden operations include but are not limited to:
    - reload / reboot commands
    - write erase / erase startup-config
    - format / erase nvram / delete flash:
    - boot system commands
    - factory-reset commands
    - any commands that require user confirmation prompts
    """

    def _run(self, tool_input: str, run_manager=None) -> List[Dict[str, Any]]:  # pylint: disable=unused-argument
        """
        Executes configuration commands on multiple devices in the current GNS3 topology.

        Args:
            tool_input (str): A JSON string containing a list of device configuration commands to execute.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing device names and configuration results.
        """

        try:
            device_configs_list = json.loads(tool_input)
            if not isinstance(device_configs_list, list):
                return [{"error": "Input must be a JSON array of device configuration objects"}]
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON input: %s", e)
            return [{"error": f"Invalid JSON input: {e}"}]

        # Create a mapping of device names to their configuration commands
        device_configs_map = {}
        for device_config in device_configs_list:
            device_name = device_config["device_name"]
            config_commands = device_config["config_commands"]
            device_configs_map[device_name] = config_commands

        # Task to execute configuration commands for all devices concurrently
        def run_all_device_configs(task: Task) -> Result:
            """Execute configuration commands for a device based on device_configs_map"""
            device_name = task.host.name
            config_commands = device_configs_map.get(device_name, [])
            
            try:
                # Use netmiko_send_config for configuration commands
                # This method automatically handles entering and exiting configuration mode
                result = task.run(
                    task=netmiko_send_config,
                    config_commands=config_commands
                )
                return Result(host=task.host, result=result.result)
            except Exception as e:
                return Result(host=task.host, result=f"Error executing configuration commands: {str(e)}", failed=True)

        # Get topology information
        topo = GNS3TopologyTool()
        topology = topo._run()
        
        # Dynamically build hosts_data from topology
        hosts_data = {}
        for device_config in device_configs_list:
            device_name = device_config["device_name"]
            
            # Check if device exists in topology
            if not topology or device_name not in topology.get("nodes", {}):
                continue
                
            node_info = topology["nodes"][device_name]
            if "console_port" not in node_info:
                continue
                
            # Add device to hosts_data
            hosts_data[device_name] = {
                "port": node_info["console_port"],
                "groups": ["cisco_IOSv_telnet"]
            }
        
        # Dynamically initialize Nornir
        try:
            dynamic_nr = InitNornir(
                inventory={
                    "plugin": "DictInventory",
                    "options": {
                        "hosts": hosts_data,
                        "groups": groups_data,
                        "defaults": defaults,
                    },
                },
                runner={
                    "plugin": "threaded",
                    "options": {
                        "num_workers": 10
                    },
                },
                logging={
                    "enabled": False # Disable Nornir's automatic logging
                },
            )
        except Exception as e:
            logger.error("Failed to initialize Nornir: %s", e)
            return [{"error": f"Failed to initialize Nornir: {e}"}]
        
        results = []
        
        # Execute all devices concurrently in a single run
        try:
            task_result = dynamic_nr.run(
                task=run_all_device_configs
            )
            
            # Process results for all devices
            for device_config in device_configs_list:
                device_name = device_config["device_name"]
                config_commands = device_config["config_commands"]
                
                # Check if device is in dynamically built hosts_data
                if device_name not in hosts_data:
                    # Device not found in topology or missing console_port
                    device_result = {
                        "device_name": device_name,
                        "status": "failed",
                        "error": f"Device '{device_name}' not found in topology or missing console_port"
                    }
                    results.append(device_result)
                    continue
                
                # Check if device has results
                if device_name not in task_result:
                    # Device not found in task results
                    device_result = {
                        "device_name": device_name,
                        "status": "failed",
                        "error": f"Device '{device_name}' not found in task results"
                    }
                    results.append(device_result)
                    continue
                
                # Process task results
                multi_result = task_result[device_name]
                device_result = {"device_name": device_name}
                
                if multi_result[0].failed:
                    # Task execution failed
                    device_result["status"] = "failed"
                    device_result["error"] = f"Configuration execution failed: {multi_result[0].exception}"
                    device_result["output"] = multi_result[0].result
                else:
                    # Task execution successful
                    device_result["status"] = "success"
                    device_result["output"] = multi_result[0].result
                    device_result["config_commands"] = config_commands
                
                results.append(device_result)
                
        except Exception as e:
            # Overall execution failed
            logger.error("Error executing configuration commands on all devices: %s", e)
            for device_config in device_configs_list:
                device_name = device_config["device_name"]
                device_result = {
                    "device_name": device_name,
                    "status": "failed",
                    "error": f"Execution error: {str(e)}"
                }
                results.append(device_result)
        
        logger.info("Multiple device configuration execution completed. Results: %s", 
                   json.dumps(results, indent=2, ensure_ascii=False))
        
        return results

if __name__ == "__main__":
    # Example usage
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
    
    exe_config = ExecuteMultipleDeviceConfigCommands()
    result = exe_config._run(tool_input=json.dumps(device_configs))
    print("Configuration execution results:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
