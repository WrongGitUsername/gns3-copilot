import sys
import os
# Add the parent directory to Python path to import tools package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
from nornir import InitNornir
from nornir.core.task import Task, Result
from nornir.core.inventory import Inventory
from nornir.core import Config
from nornir_salt.plugins.inventory import DictInventory
from nornir_netmiko.tasks import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from tools.gns3_topology_reader import GNS3TopologyTool
import json


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

#hosts_data = {
#    "R-1": {
#        "port": 5004,
#        "groups": ["cisco_IOSv_telnet"]
#    },
#    "R-2": {
#        "port": 5002,
#        "groups": ["cisco_IOSv_telnet"]
#    }
#}

defaults = {
    "data": {
        "location": "gns3"
    }
}

# Task to execute multiple commands for a specific device
def run_device_commands(task: Task, commands: list) -> Result:
    """执行指定设备的命令列表"""
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

def execute_device_commands(device_commands_list):
    """
    执行多个设备的命令并返回格式化结果
    
    Args:
        device_commands_list: 设备命令列表
        [
            {
                "device_name": "R-1",
                "commands": ["show ver", "show ip int br"]
            },
            {
                "device_name": "R-2", 
                "commands": ["show ver", "show ip int br"]
            }
        ]
    
    Returns:
        [
            {
                "device_name": "R-1",
                "show ver": "命令输出内容...",
                "show ip int br": "命令输出内容..."
            },
            {
                "device_name": "R-2",
                "show ver": "命令输出内容...", 
                "show ip int br": "命令输出内容..."
            }
        ]
    """
    # 获取拓扑信息
    topo = GNS3TopologyTool()
    topology = topo._run()
    
    # 动态构建 hosts_data
    hosts_data = {}
    for device_cmd in device_commands_list:
        device_name = device_cmd["device_name"]
        
        # 检查设备是否在拓扑中
        if not topology or device_name not in topology.get("nodes", {}):
            continue
            
        node_info = topology["nodes"][device_name]
        if "console_port" not in node_info:
            continue
            
        # 添加设备到 hosts_data
        hosts_data[device_name] = {
            "port": node_info["console_port"],
            "groups": ["cisco_IOSv_telnet"]
        }
    
    # 动态初始化 Nornir
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
        }
    )
    
    results = []
    
    for device_cmd in device_commands_list:
        device_name = device_cmd["device_name"]
        commands = device_cmd["commands"]
        
        # 检查设备是否在动态构建的 hosts_data 中
        if device_name not in hosts_data:
            # 设备不存在于拓扑中或没有 console_port
            device_result = {"device_name": device_name}
            for cmd in commands:
                device_result[cmd] = f"Device '{device_name}' not found in topology or missing console_port"
            results.append(device_result)
            continue
        
        # 过滤设备
        filtered_nr = dynamic_nr.filter(name=device_name)
        
        if len(filtered_nr.inventory.hosts) == 0:
            # 设备不存在，添加错误信息
            device_result = {"device_name": device_name}
            for cmd in commands:
                device_result[cmd] = f"Device '{device_name}' not found in inventory"
            results.append(device_result)
            continue
        
        # 执行命令
        try:
            task_result = filtered_nr.run(
                task=run_device_commands,
                commands=commands
            )
            
            # 格式化结果
            device_result = {"device_name": device_name}
            for host_name, multi_result in task_result.items():
                if multi_result[0].failed:
                    # 任务执行失败
                    for cmd in commands:
                        device_result[cmd] = f"Task execution failed: {multi_result[0].exception}"
                else:
                    # 任务执行成功
                    command_results = multi_result[0].result
                    for cmd, output in command_results.items():
                        device_result[cmd] = output
            
            results.append(device_result)
            
        except Exception as e:
            # 整体执行失败
            device_result = {"device_name": device_name}
            for cmd in commands:
                device_result[cmd] = f"Execution error: {str(e)}"
            results.append(device_result)
    
    return results

# 示例使用
if __name__ == "__main__":
    # 示例输入
    device_commands = [
        {
            "device_name": "R-1",
            "commands": ["show ver", "show ip int br"]
        },
        {
            "device_name": "R-2",
            "commands": ["show ver", "show ip int br"]
        }
    ]
    
    # 执行命令
    results = execute_device_commands(device_commands)
    
    # 打印结果
    print("执行结果:")
    print(json.dumps(results, indent=2, ensure_ascii=False))
