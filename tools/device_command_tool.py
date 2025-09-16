from netmiko import ConnectHandler, NetmikoTimeoutException
from gns3_topology_reader import get_open_project_topology

# input 设备名称和要执行的命令
device_name, commands = ('R-3', ['show running', 
'show ip ospf neighbor', 
'show ip interface brief', 
'show version',
'show ip route'])

# 获取拓扑信息
topology = get_open_project_topology()

# 检查节点和 console_port 是否存在
if not topology or device_name not in topology.get("nodes", {}):
    print(f"Device '{device_name}' not found in the topology.")
    exit()

node_info = topology["nodes"][device_name]
if "console_port" not in node_info:
    print(f"Device '{device_name}' found, but it does not have a console_port.")
    exit()

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
    print(f"Connecting to {device_name} at localhost:{device['port']}...")
    conn = ConnectHandler(**device)

    # 禁用分页，确保长输出可以一次性返回
    conn.disable_paging()

    # 进入特权模式
    conn.enable()

    # 打印netmiko 自动发现的提示符。
    actual_prompt = conn.find_prompt()
    print(f"Successfully connected. Device prompt is : {actual_prompt}")
    
    # 执行命令
    for command in commands:
        print(f"\n--- Executing: {command} ---")
        # 使用 read_timeout 确保命令有足够时间完成
        output = conn.send_command(command, read_timeout=60)
        print(output)

    print("\nDisconnecting...")
    conn.disconnect()

except NetmikoTimeoutException:
    print(f"Connection to {device_name} timed out. Please check connectivity and if the device is responsive.")
except Exception as e:
    print(f"An error occurred: {e}")
