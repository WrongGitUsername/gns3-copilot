"""
This module provides a tool to execute display commands on multiple devices in a GNS3 topology using Nornir.
"""
import json
import logging
from typing import List, Dict, Any
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from langchain.tools import BaseTool
from .gns3_topology_reader import GNS3TopologyTool

# config log
logger = logging.getLogger("display_tools_nornir")
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers if the module is reloaded
if not logger.handlers:
    # log to files
    file_handler = logging.FileHandler("log/display_tools_nornir.log", mode="a")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    # log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

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

class ExecuteMultipleDeviceCommands(BaseTool):
    """
    A tool to execute display (show) commands on multiple devices in a GNS3 topology using Nornir.
    This class uses Nornir to manage connections and execute commands on multiple devices concurrently.

    **Important:**
    This tool is strictly for read-only operations.
    It is forbidden to execute any configuration commands, including 'configure terminal' or any command that changes device state.
    Only use this tool for safe, non-intrusive 'show' or display commands.
    """

    name: str = "execute_multiple_device_commands"
    description: str = """
    Executes display (show) commands on multiple devices in the current GNS3 topology.
    Input should be a JSON array containing device names and their respective commands to execute.
    Example input:
        [
            {
                "device_name": "R-1",
                "commands": ["show version", "show ip interface brief"]
            },
            {
                "device_name": "R-2", 
                "commands": ["show version", "show ip ospf neighbor"]
            }
        ]
    Returns a list of dictionaries, each containing the device name and command outputs.

    **Do NOT use this tool for any configuration commands (such as 'configure terminal').**
    """

    def _run(self, tool_input: str, run_manager=None) -> List[Dict[str, Any]]:  # pylint: disable=unused-argument
        """
        Executes display commands on multiple devices in the current GNS3 topology.

        Args:
            tool_input (str): A JSON string containing a list of device commands to execute.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing device names and command outputs.
        """

        try:
            device_commands_list = json.loads(tool_input)
            if not isinstance(device_commands_list, list):
                return [{"error": "Input must be a JSON array of device command objects"}]
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON input: %s", e)
            return [{"error": f"Invalid JSON input: {e}"}]

        # Task to execute multiple commands for a specific device
        def run_device_commands(task: Task, commands: list) -> Result:
            """Execute specified commands on a device"""
            results = {}
            for cmd in commands:
                try:
                    result = task.run(
                        task=netmiko_send_command,
                        command_string=cmd
                    )
                    results[cmd] = result.result
                except Exception as e:
                    results[cmd] = f"Error executing command '{cmd}': {str(e)}"
            return Result(host=task.host, result=results)

        # Get topology information
        topo = GNS3TopologyTool()
        topology = topo._run()
        
        # Dynamically build hosts_data from topology
        hosts_data = {}
        for device_cmd in device_commands_list:
            device_name = device_cmd["device_name"]
            
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
        
        for device_cmd in device_commands_list:
            device_name = device_cmd["device_name"]
            commands = device_cmd["commands"]
            
            # Check if device is in dynamically built hosts_data
            if device_name not in hosts_data:
                # Device not found in topology or missing console_port
                device_result = {"device_name": device_name}
                for cmd in commands:
                    device_result[cmd] = f"Device '{device_name}' not found in topology or missing console_port"
                results.append(device_result)
                continue
            
            # Filter device
            filtered_nr = dynamic_nr.filter(name=device_name)
            
            if len(filtered_nr.inventory.hosts) == 0:
                # Device not found, add error message
                device_result = {"device_name": device_name}
                for cmd in commands:
                    device_result[cmd] = f"Device '{device_name}' not found in inventory"
                results.append(device_result)
                continue
            
            # Execute commands
            try:
                task_result = filtered_nr.run(
                    task=run_device_commands,
                    commands=commands
                )
                
                # Format results
                device_result = {"device_name": device_name}
                for host_name, multi_result in task_result.items():
                    if multi_result[0].failed:
                        # Task execution failed
                        for cmd in commands:
                            device_result[cmd] = f"Task execution failed: {multi_result[0].exception}"
                    else:
                        # Task execution successful
                        command_results = multi_result[0].result
                        for cmd, output in command_results.items():
                            device_result[cmd] = output
                
                results.append(device_result)
                
            except Exception as e:
                # Overall execution failed
                logger.error("Error executing commands on device %s: %s", device_name, e)
                device_result = {"device_name": device_name}
                for cmd in commands:
                    device_result[cmd] = f"Execution error: {str(e)}"
                results.append(device_result)
        
        logger.info("Multiple device command execution completed. Results: %s", 
                   json.dumps(results, indent=2, ensure_ascii=False))
        
        return results

if __name__ == "__main__":
    # Example usage
    device_commands = [
        {
            "device_name": "R-1",
            "commands": ["show version", "show ip interface brief"]
        },
        {
            "device_name": "R-2",
            "commands": ["show version", "show ip interface brief"]
        }
    ]
    
    exe_cmd = ExecuteMultipleDeviceCommands()
    result = exe_cmd._run(tool_input=json.dumps(device_commands))
    print("Execution results:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
