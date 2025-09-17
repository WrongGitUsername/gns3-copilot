"""
This module provides a tool to execute commands on devices in a GNS3 topology.
"""
import json
import logging
from pprint import pprint
from netmiko import ConnectHandler, NetmikoTimeoutException
from .gns3_topology_reader import get_open_project_topology
from langchain.tools import BaseTool

# config log
logger = logging.getLogger("device_command_tool")
logger.setLevel(logging.DEBUG)

# log to files
file_handler = logging.FileHandler("log/device_command_tool.log", mode="a")
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

class ExecuteCommands(BaseTool):
    """
    A tools to execute commands on devices in a GNS3 topology.
    This class uses Netmiko to connect to devices and execute a list of commands.
    """

    name: str = "execute_device_commands"
    description: str = """
    Executes a list of commands on a specified device in the GNS3 topology.
    Input is a JSON object containing the device name and a list of commands.
    example:
        {
            "device_name": "R-4",
            "commands": [
                "show running-config | section ospf",
                "show ip ospf neighbor",
                "show ip ospf interface brief",
                "show ip ospf database"
            ]
        }
        returns JSON with results.
    """

    def _run(self, tool_input: str, run_manager = None) -> dict:  # pylint: disable=unused-argument
        """
        Executes a list of commands on a specified device in the GNS3 topology.

        Args:
            device_name (str): The name of the device to connect to.
            commands (list): A list of commands to execute.

        Returns:
            dict: A dictionary containing the command outputs.
        """

        input_data = json.loads(tool_input)
        device_name = input_data.get("device_name")
        commands = input_data.get("commands", [])

        # get topology info 
        topology = get_open_project_topology()

        # check if node and console_port exist
        if not topology or device_name not in topology.get("nodes", {}):
            logger.error("Device '%s' not found in the topology.", device_name)
            return {}

        node_info = topology["nodes"][device_name]
        if "console_port" not in node_info:
            logger.error("Device '%s' found, but it does not have a console_port.", device_name)
            return {}

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
                output = conn.send_command(command, read_timeout=60)
                results[command] = output

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
            return {}
        except (ValueError, KeyError, TypeError) as e:
            logger.error("Error occurred: %s", e)
            return {}

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
    #'show ip ospf events', # 耗时太长，内容太多。
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

    exe_cmd = ExecuteCommands()
    result = exe_cmd._run(tool_input=json.dumps({
        "device_name": dev_name,
        "commands": cmds
    }))
    pprint(result)
