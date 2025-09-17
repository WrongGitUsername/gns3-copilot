"""
This module provides a tool to execute commands on devices in a GNS3 topology.
"""
import json
import logging
from pprint import pprint
from netmiko import ConnectHandler, NetmikoTimeoutException
from gns3_topology_reader import get_open_project_topology

# 配置日志记录
logger = logging.getLogger("device_command_tool")
logger.setLevel(logging.DEBUG)

# 文件日志处理（记录debug级别以上的日志）
file_handler = logging.FileHandler("log/device_command_tool.log", mode="a")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

# 控制台日志处理(记录info级别以上的日志)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# 将日志添加到日志记录
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def execute_commands(device_name, commands):
    """
    Executes a list of commands on a specified device in the GNS3 topology.

    Args:
        device_name (str): The name of the device to connect to.
        commands (list): A list of commands to execute.

    Returns:
        dict: A dictionary containing the command outputs.
    """
    # 获取拓扑信息
    topology = get_open_project_topology()

    # 检查节点和 console_port 是否存在
    if not topology or device_name not in topology.get("nodes", {}):
        logger.error("Device '%s' not found in the topology.", device_name)
        return None

    node_info = topology["nodes"][device_name]
    if "console_port" not in node_info:
        logger.error("Device '%s' found, but it does not have a console_port.", device_name)
        return None

    # 定义设备连接参数
    device = {
        'device_type': 'cisco_ios_telnet',
        'host': 'localhost',  # GNS3 服务器地址
        'port': node_info["console_port"],
        'username': '',
        'password': '',
        'session_timeout': 120,  # 增加超时以应对慢速设备
    }

    try:
        logger.info("Connecting to %s at localhost:%s...", device_name, device['port'])
        conn = ConnectHandler(**device)

        # 禁用分页，确保长输出可以一次性返回
        conn.disable_paging()

        # 进入特权模式
        conn.enable()

        # 打印netmiko 自动发现的提示符。
        actual_prompt = conn.find_prompt()
        logger.info("Successfully connected. Device prompt is : %s", actual_prompt)

        results = {}
        # 执行命令
        for command in commands:
            logger.info("--- Executing: %s ---", command)
            output = conn.send_command(command, read_timeout=60)
            results[command] = output

        # 输出为json格式
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
    except ValueError as e:
        logger.error("ValueError occurred: %s", e)
    except KeyError as e:
        logger.error("KeyError occurred: %s", e)
    except TypeError as e:
        logger.error("TypeError occurred: %s", e)


if __name__ == "__main__":
    # input 设备名称和要执行的命令
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
    # 其他常用 OSPF 排查命令
    'show ip ospf interface',
    #'show ip ospf events', #耗时太长，内容太多。
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

    exe_cmd = execute_commands(device_name=dev_name, commands=cmds)
    pprint(exe_cmd)
