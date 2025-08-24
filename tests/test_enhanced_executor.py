#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试增强型命令执行器的IP地址提取功能
"""

import re

def extract_ip_addresses(command_output: str) -> list:
    """从命令输出中提取IP地址"""
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    ips = re.findall(ip_pattern, command_output)
    
    # 过滤掉明显不是接口IP的地址
    valid_ips = []
    for ip in ips:
        # 跳过0.0.0.0, 255.255.255.255等特殊地址
        if ip not in ['0.0.0.0', '255.255.255.255'] and not ip.endswith('.255'):
            # 检查是否在合理的私有IP范围内
            if (ip.startswith('10.') or ip.startswith('192.168.') or 
                ip.startswith('172.') or ip.startswith('1.')):
                valid_ips.append(ip)
    
    return list(set(valid_ips))  # 去重

def test_ip_extraction():
    """测试IP地址提取功能"""
    
    # 模拟 show ip interface brief 输出
    sample_outputs = [
        """
Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         1.1.1.1         YES NVRAM  up                    up      
GigabitEthernet0/1         12.1.1.1        YES NVRAM  up                    up      
GigabitEthernet0/2         unassigned      YES NVRAM  administratively down down    
Loopback0                  1.1.1.1         YES NVRAM  up                    up
        """,
        """
Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         6.6.6.6         YES NVRAM  up                    up      
GigabitEthernet0/1         56.1.1.6        YES NVRAM  up                    up      
GigabitEthernet0/2         unassigned      YES NVRAM  administratively down down    
Loopback0                  6.6.6.6         YES NVRAM  up                    up
        """,
        """
Interface                  IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0         192.168.1.10    YES NVRAM  up                    up      
GigabitEthernet0/1         10.0.0.1        YES NVRAM  up                    up      
Loopback0                  172.16.1.1      YES NVRAM  up                    up
        """
    ]
    
    print("🔍 IP地址提取测试")
    print("=" * 60)
    
    for i, output in enumerate(sample_outputs, 1):
        print(f"\n📊 测试样例 {i}:")
        print("输入:")
        print(output.strip())
        
        extracted_ips = extract_ip_addresses(output)
        print(f"\n提取的IP地址: {extracted_ips}")

def parse_connectivity_query_test():
    """测试连通性查询解析"""
    
    test_queries = [
        "please ping R-1 to R-6 ip address",
        "ping from R-1 to R-6",
        "test connectivity between R-2 and R-5",
        "check if R-3 can reach R-4",
        "verify connection R-6 to R-1"
    ]
    
    device_names = ["R-1", "R-2", "R-3", "R-4", "R-5", "R-6", "IOSvL2-1"]
    
    print("\n\n🎯 连通性查询解析测试")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n📝 查询: '{query}'")
        
        # 查找查询中提到的设备
        found_devices = []
        for device_name in device_names:
            if device_name.lower() in query.lower():
                found_devices.append(device_name)
        
        print(f"找到的设备: {found_devices}")
        
        if len(found_devices) >= 2:
            print(f"源设备: {found_devices[0]}, 目标设备: {found_devices[1]}")
        elif len(found_devices) == 1:
            print(f"只找到一个设备: {found_devices[0]}")
        else:
            print("未找到设备")

if __name__ == "__main__":
    test_ip_extraction()
    parse_connectivity_query_test()
