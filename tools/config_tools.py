"""
This module provides a dedicated tool to execute configuration commands on devices 
in a GNS3 topology using Netmiko.
"""
import json
import logging
from pprint import pprint
from netmiko import ConnectHandler, NetmikoTimeoutException
from langchain.tools import BaseTool
from .gns3_topology_reader import GNS3TopologyTool
from .logging_config import setup_tool_logger

# --- Logging Configuration ---
logger = setup_tool_logger("device_config_tool")


class ExecuteConfigCommands(BaseTool):
    """
    A tool to execute configuration commands on devices in a GNS3 topology.
    This class uses Netmiko's specific methods for applying configurations.

    IMPORTANT SAFETY NOTE:
    This tool is intended for configuration changes only, but MUST NOT be used to reboot
    or factory-reset devices. Commands that reboot, erase, or otherwise make the device
    unavailable (for example: "reload", "write erase", "erase startup-config", "format",
    "erase nvram", "delete flash:", "boot system") are forbidden and will be refused.
    Use extreme caution and require manual confirmation for destructive operations.
    """

    name: str = "execute_config_commands"
    description: str = """
    Executes a list of CONFIGURATION commands on a specified device.
    Use this tool ONLY for changing device settings (e.g., 'configure', 'interface', 'ip address', 'router ospf').
    For viewing information, use the 'execute_device_commands' tool.
    Input is a JSON object with 'device_name' and 'config_commands'.
    Example:
        {
            "device_name": "R-1",
            "config_commands": [
                "interface Loopback0",
                "ip address 1.1.1.1 255.255.255.255",
                "description CONFIG_BY_TOOL"
            ]
        }
    Returns a dictionary with the output from the configuration session.

    SAFETY: the following commands (and similar) are FORBIDDEN and WILL BE REFUSED:
    - reload
    - write erase / erase startup-config
    - format / erase nvram / delete flash:
    - any explicit factory-reset or reboot command.
    - interaction commands requiring user confirmation (prompts like "Contiue? [confirm]")
    """

    def _run(self, tool_input: str, run_manager=None) -> dict:  # pylint: disable=unused-argument
        """
        Executes a list of configuration commands on a specified device.

        Args:
            tool_input (str): A JSON string containing the device name and a list of configuration commands.

        Returns:
            dict: A dictionary containing the output of the configuration session.
        """
        try:
            input_data = json.loads(tool_input)
            device_name = input_data.get("device_name")
            config_commands = input_data.get("config_commands", [])
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON input: %s", e)
            return {"error": f"Invalid JSON input: {e}"}

        if not device_name or not config_commands:
            return {"error": "Missing 'device_name' or 'config_commands' in input."}

        topo = GNS3TopologyTool()
        topology = topo._run()

        if not topology or device_name not in topology.get("nodes", {}):
            logger.error("Device '%s' not found in the topology.", device_name)
            return {"error": f"Device '{device_name}' not found in the topology."}

        node_info = topology["nodes"][device_name]
        if "console_port" not in node_info:
            logger.error("Device '%s' does not have a console_port.", device_name)
            return {"error": f"Device '{device_name}' does not have a console_port."}

        device = {
            'device_type': 'cisco_ios_telnet',
            'host': 'localhost',
            'port': node_info["console_port"],
            'username': '',
            'password': '',
            'session_timeout': 120,
        }

        try:
            logger.info("Connecting to %s for CONFIGURATION at localhost:%s...", device_name, device['port'])
            with ConnectHandler(**device) as conn:
                conn.enable()
                actual_prompt = conn.find_prompt()
                logger.info("Successfully connected. Device prompt is: %s", actual_prompt)

                logger.info("--- Applying configuration: %s ---", config_commands)
                
                # Use send_config_set for configuration commands.
                # This method automatically handles entering and exiting configuration mode.
                output = conn.send_config_set(config_commands)
                
                results = {
                    "device_name": device_name,
                    "status": "Configuration commands sent.",
                    "output": output
                }

                logger.debug(
                    "Configuration results: %s", 
                    json.dumps(results, indent=2, ensure_ascii=False)
                )
                logger.info("Configuration session on %s finished.", device_name)

                return results

        except NetmikoTimeoutException:
            logger.error("Connection to %s timed out during configuration.", device_name)
            return {"error": f"Connection to {device_name} timed out."}
        except Exception as e:
            logger.error("An error occurred during configuration on %s: %s", device_name, e, exc_info=True)
            return {"error": f"An error occurred: {e}"}


if __name__ == "__main__":
    # --- Test block for the configuration tool ---
    dev_name = 'R-1'
    # Example configuration commands
    config_cmds = [
        'interface Loopback101',
        'description Test interface by config tool',
        'ip address 101.101.101.101 255.255.255.255'
    ]

    config_tool = ExecuteConfigCommands()
    
    # Prepare the input as a JSON string, just like the agent would
    tool_input_str = json.dumps({
        "device_name": dev_name,
        "config_commands": config_cmds
    })
    
    result = config_tool._run(tool_input=tool_input_str)
    pprint(result)
