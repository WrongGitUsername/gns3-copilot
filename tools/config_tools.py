"""
This module provides a dedicated tool to execute configuration commands on devices 
in a GNS3 topology using Netmiko.
"""
import json
import logging
from pprint import pprint
from netmiko import ConnectHandler, NetmikoTimeoutException
from langchain.tools import BaseTool
from .gns3_topology_reader import get_open_project_topology

# --- Logging Configuration ---
logger = logging.getLogger("device_config_tool")
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers if the module is reloaded
if not logger.handlers:
    # Log to file
    file_handler = logging.FileHandler("log/device_config_tool.log", mode="a")
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


class ExecuteConfigCommands(BaseTool):
    """
    A tool to execute configuration commands on devices in a GNS3 topology.
    This class uses Netmiko's specific methods for applying configurations.
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
    Returns a JSON object with the output from the configuration session.
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

        topology = get_open_project_topology()

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