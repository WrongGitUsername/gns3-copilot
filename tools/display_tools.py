"""
This module provides a tool to execute commands on devices in a GNS3 topology.
"""
import json
import logging
import time
from pprint import pprint
from netmiko import ConnectHandler, NetmikoTimeoutException
from langchain.tools import BaseTool
from tools.gns3_topology_reader import GNS3TopologyTool

# config log
logger = logging.getLogger("display_tools")
logger.setLevel(logging.DEBUG)

# Prevent duplicate handlers if the module is reloaded
if not logger.handlers:
    # log to files
    file_handler = logging.FileHandler("log/display_tools.log", mode="a")
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

class ExecuteDisplayCommands(BaseTool):
    """
    A tool to execute display (show) commands on devices in a GNS3 topology.
    This class uses Netmiko to connect to devices and execute a list of display-related commands.

    **Important:**
    This tool is strictly for read-only operations.
    It is forbidden to execute any configuration commands, including 'configure terminal' or any command that changes device state.
    Only use this tool for safe, non-intrusive 'show' or display commands.
    """

    name: str = "execute_display(show)_commands"
    description: str = """
    Executes a list of display (show) commands on a specified device in the current GNS3 topology.
    Input should be a JSON object with the device name and a list of commands to execute.
    Example input:
        {
            "device_name": "R-4",
            "commands": [
                "show running-config | section ospf",
                "show ip ospf neighbor",
                "show ip ospf interface brief",
                "show ip ospf database"
            ]
        }
    Returns a dictionary mapping each command to its output, or an error dictionary if an error occurs.

    **Do NOT use this tool for any configuration commands (such as 'configure terminal').**
    """

    def _run(self, tool_input: str, run_manager=None) -> dict:  # pylint: disable=unused-argument
        """
        Executes a list of display (show) commands on a specified device in the current GNS3 topology.

        Args:
            tool_input (str): A JSON string containing the device name and a list of commands to execute.

        Returns:
            dict: A dictionary containing the command outputs, or an error dictionary if an error occurs.
        """

        try:
            input_data = json.loads(tool_input)
            device_name = input_data.get("device_name")
            commands = input_data.get("commands", [])
        except json.JSONDecodeError as e:
            logger.error("Invalid JSON input: %s", e)
            return {"error": f"Invalid JSON input: {e}"}

        if not device_name or not commands:
            return {"error": "Missing 'device_name' or 'commands' in input."}

        # get topology information
        topo = GNS3TopologyTool()
        topology = topo._run()

        # check if node and console_port exist
        if not topology or device_name not in topology.get("nodes", {}):
            logger.error("Device '%s' not found in the topology.", device_name)
            return {"error": f"Device '{device_name}' not found in the topology."}

        node_info = topology["nodes"][device_name]
        if "console_port" not in node_info:
            logger.error("Device '%s' found, but it does not have a console_port.", device_name)
            return {"error": f"Device '{device_name}' does not have a console_port."}

        # define device connection parameters
        device = {
            'device_type': 'cisco_ios_telnet',
            'host': 'localhost',  # GNS3 server address
            'port': node_info["console_port"],
            'username': '',
            'password': '',
            'session_timeout': 120,  # increase timeout for slow devices
        }

        try:
            logger.info("Connecting to %s at localhost:%s...", device_name, device['port'])
            conn = ConnectHandler(**device)

            # fix "Error: Pattern not detected: 'terminal\\ length\\ 0' in output"
            time.sleep(1)
            conn.write_channel("\n")
            time.sleep(1)
            conn.write_channel("\n")

            # disable paging to ensure long output is returned in one go
            conn.disable_paging()

            # enter enable mode
            conn.enable()

            # print netmiko auto-discovered prompt
            actual_prompt = conn.find_prompt()
            logger.info("Successfully connected. Device prompt is : %s", actual_prompt)

            results = {}
            # execute commands
            for command in commands:
                logger.info("--- Executing: %s ---", command)
                try:
                    output = conn.send_command(command, read_timeout=60)
                    results[command] = output
                except Exception as e:
                    logger.error("Error occurred while executing command '%s': %s", command, e)
                    results[command] = f"Error: {str(e)}"

            # output results
            logger.debug(
                "Command execution results: %s", 
                json.dumps(results, indent=2, ensure_ascii=False)
                )

            logger.info("Disconnecting...")
            conn.disconnect()

            return results

        except NetmikoTimeoutException:
            logger.error(
                "Connection to %s timed out. Please check connectivity "
                "and if the device is responsive.",
                device_name
                )
            return {"error": f"Connection to {device_name} timed out."}
        except (ValueError, KeyError, TypeError) as e:
            logger.error("Error occurred: %s", e)
            return {"error": f"An error occurred: {e}"}

if __name__ == "__main__":
    # input device name and commands to execute
    dev_name, cmds = ('R-4', [
    'show running-config | section ospf',
    'show ip ospf neighbor',
    'show ip ospf interface brief',
    'show ip ospf database',
    'show ip ospf',
    'show ip route ospf',
    'show ip protocols',
    'show ip interface brief',
    'show version',
    'show ip ospf interface',
    #'show ip ospf events', # time too long
    'show ip ospf statistics',
    'show ip ospf border-routers',
    'show ip ospf virtual-links',
    'show ip ospf sham-links',
    'show ip ospf traffic',
    'show ip ospf retransmission-list',
    'show ip ospf request-list',
    'show ip ospf database router',
    'show ip ospf database network',
    'show ip ospf database summary',
    'show ip ospf database external',
    'show ip ospf database opaque-area',
    'show ip ospf database opaque-as',
    'show ip ospf database self-originate',
    'show ip ospf max-metric',
    'show ip ospf mpls ldp interface',
    'show ip ospf neighbor detail'
    ])

    exe_cmd = ExecuteDisplayCommands()
    result = exe_cmd._run(tool_input=json.dumps({
        "device_name": dev_name,
        "commands": cmds
    }))
    pprint(result)
