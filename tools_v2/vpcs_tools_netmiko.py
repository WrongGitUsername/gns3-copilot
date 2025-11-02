"""
This module provides a tool to configure and operate VPCS (Virtual PC Simulator) nodes 
in GNS3 topology using Netmiko for sequential command execution.

The module enables batch configuration and management of multiple VPCS devices,
allowing sequential IP configuration, network testing, and other VPCS-specific
operations across the entire GNS3 topology.
"""
import json
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
from netmiko import ConnectHandler
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException
from langchain.tools import BaseTool
from .gns3_topology_reader import GNS3TopologyTool
from log_config import setup_tool_logger

# Configure logger for VPCS operations
logger = setup_tool_logger("vpcs_tools_netmiko")

# Load environment variables
load_dotenv()

class VPCSCommands(BaseTool):
    """
    A tool to configure and operate VPCS (Virtual PC Simulator) nodes in GNS3 topology using Netmiko.
    This class enables sequential IP configuration, network testing, and VPCS-specific operations
    across multiple virtual PC instances.

    **Key Features:**
    - Batch IP address configuration for multiple VPCS nodes
    - Sequential network connectivity testing (ping, traceroute)
    - VPCS-specific command execution (ip, ping, show, etc.)
    - Sequential execution for improved reliability

    **Supported VPCS Commands:**
    - IP configuration: `ip <address>/<mask> <gateway>`
    - Network testing: `ping <target>`, `trace <target>`
    - Display commands: `show ip`, `show arp`, `version`
    - Route management: `ip <network>/<mask> <gateway>`

    **Note:** This tool supports both configuration and display commands for VPCS devices,
    unlike network device tools that may be read-only.
    """

    name: str = "configure_vpcs_devices"
    description: str = """
    Configures and operates VPCS (Virtual PC Simulator) nodes in GNS3 topology using Netmiko.
    Supports IP configuration, network testing, and VPCS-specific commands for multiple devices sequentially.
    
    Input should be a JSON array containing VPCS device names and their respective commands to execute.
    Example input:
        [
            {
                "device_name": "PC1",
                "commands": ["ip 10.0.0.2/24 10.0.0.1", "ping 10.0.0.1", "show ip"]
            },
            {
                "device_name": "PC2", 
                "commands": ["ip 20.0.0.2/24 20.0.0.1", "ping 20.0.0.1", "show ip"]
            }
        ]
    
    Supported VPCS commands:
    - IP configuration: ip <address>/<mask> <gateway>
    - Network testing: ping <target>, trace <target>
    - Display commands: show ip, show arp, version
    
    Returns a list of dictionaries, each containing the VPCS device name and command outputs.
    """

    def _run(
        self,
        tool_input: str,
        run_manager=None
        ) -> List[Dict[str, Any]]:  # pylint: disable=unused-argument
        """
        Executes VPCS configuration and operation commands on multiple devices in the current GNS3 topology.

        Args:
            tool_input (str): A JSON string containing a list of VPCS device commands to
            execute. Each device should specify VPCS-specific commands like IP configuration,
            network testing, or display commands.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing VPCS device names and
            command outputs. Includes success/failure status for each command.
        """

        try:
            device_commands_list = json.loads(tool_input)
            if not isinstance(device_commands_list, list):
                return [{"error": "Input must be a JSON array of device command objects"}]
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON input: %s", e)
            return [{"error": f"Invalid JSON input: {e}"}]

        # Get topology information
        topo = GNS3TopologyTool()
        topology = topo._run()

        results = []

        # Execute commands for each device sequentially
        for device_cmd in device_commands_list:
            device_name = device_cmd["device_name"]
            commands = device_cmd["commands"]
            device_result = {"device_name": device_name}

            # Check if device exists in topology
            if not topology or device_name not in topology.get("nodes", {}):
                for cmd in commands:
                    device_result[cmd] = f"Device '{device_name}' not found in topology"
                results.append(device_result)
                continue

            node_info = topology["nodes"][device_name]
            if "console_port" not in node_info:
                for cmd in commands:
                    device_result[cmd] = f"Device '{device_name}' missing console_port"
                results.append(device_result)
                continue

            # Build connection parameters for Netmiko
            device = {
                "device_type": "generic_telnet",
                "host": os.getenv("GNS3_SERVER_HOST", "localhost"),
                "port": node_info["console_port"],
                "username": os.getenv("GNS3_SERVER_USERNAME", ""),
                "password": os.getenv("GNS3_SERVER_PASSWORD", ""),
                "timeout": 30,
            }

            # Connect to device and execute commands
            net_connect = None
            try:
                logger.info(f"Connecting to {device_name} at {device['host']}:{device['port']}...")
                net_connect = ConnectHandler(**device)
                current_prompt = net_connect.find_prompt().strip()
                logger.info(f"Connected to {device_name}, prompt: {current_prompt}")

                # Execute all commands for this device
                for cmd in commands:
                    try:
                        logger.info(f"Executing command on {device_name}: {cmd}")
                        output = net_connect.send_command_timing(
                            cmd,
                            read_timeout=15,
                            delay_factor=2,
                        )
                        device_result[cmd] = output.strip()
                        logger.info(f"Command executed successfully on {device_name}")
                    except Exception as cmd_e:
                        error_msg = f"Error executing command '{cmd}' on {device_name}: {str(cmd_e)}"
                        device_result[cmd] = error_msg
                        logger.error(error_msg)

            except NetmikoAuthenticationException:
                error_msg = f"Authentication failed for {device_name}. Please check username and password."
                logger.error(error_msg)
                for cmd in commands:
                    device_result[cmd] = error_msg

            except NetmikoTimeoutException:
                error_msg = f"Connection timeout for {device_name}. Please check if device is running and accessible."
                logger.error(error_msg)
                for cmd in commands:
                    device_result[cmd] = error_msg

            except Exception as e:
                error_msg = f"Error connecting to {device_name}: {str(e)}"
                logger.error(error_msg)
                for cmd in commands:
                    device_result[cmd] = error_msg

            finally:
                # Always try to disconnect
                if net_connect:
                    try:
                        net_connect.disconnect()
                        logger.info(f"Disconnected from {device_name}")
                    except Exception as disconnect_e:
                        logger.warning(f"Error disconnecting from {device_name}: {str(disconnect_e)}")

            results.append(device_result)

        logger.info(
            "Sequential device command execution completed. Results: %s",
            json.dumps(results, indent=2, ensure_ascii=False)
        )

        return results

if __name__ == "__main__":
    # Example usage
    device_commands = [
            {
                "device_name": "PC1",
                "commands": ["ip 10.0.0.2/24 10.0.0.1", "ping 10.0.0.1"]
            },
            {
                "device_name": "PC2", 
                "commands": ["ip 20.0.0.2/24 20.0.0.1", "ping 20.0.0.1"]
            }
        ]

    exe_cmd = VPCSCommands()
    result = exe_cmd._run(tool_input=json.dumps(device_commands))
    print("Execution results:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
