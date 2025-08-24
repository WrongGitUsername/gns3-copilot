#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试连通性分析功能
验证智能RAG增强执行器是否能正确分析设备配置并执行连通性测试
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.rag_enhanced_executor import RAGEnhancedCommandExecutor
from core.get_project_info import ProjectInfoManager
from core.get_all_devices_config import DeviceConfigCollector

def test_connectivity_analysis():
    """测试连通性分析功能"""
    print("=== 测试连通性分析功能 ===\n")
    
    try:
        # 1. 获取项目和设备信息
        print("1. 获取设备配置...")
        config_collector = DeviceConfigCollector()
        
        # 使用拓扑信息获取设备
        opened_projects, topology_data = config_collector.get_topology_info()
        
        if not topology_data:
            print("❌ 无法获取拓扑信息")
            return
        
        # 从拓扑数据中提取设备信息
        devices_info = []
        for project_name, project_data in topology_data.items():
            configurable_devices = config_collector.filter_configurable_devices(project_data['nodes'])
            devices_info.extend(configurable_devices)
        
        if not devices_info:
            print("❌ 无法获取设备配置")
            return
        
        print(f"✅ 找到 {len(devices_info)} 个设备")
        for device in devices_info:
            print(f"   - {device['name']} (端口: {device['console']})")
        
        # 2. 创建RAG增强执行器
        print("\n3. 初始化RAG增强执行器...")
        
        # 创建一个模拟的LLM对象
        class MockLLM:
            def invoke(self, prompt):
                return "show ip interface brief"
        
        mock_llm = MockLLM()
        telnet_host = "192.168.102.1"  # 使用默认的telnet主机地址
        
        executor = RAGEnhancedCommandExecutor(telnet_host, mock_llm)
        
        # 3. 测试连通性查询检测
        print("\n4. 测试连通性查询检测...")
        test_queries = [
            "ping R-2 from R-1",
            "test connectivity between R-1 and R-6", 
            "检查R-1和R-6之间的连通性",
            "show ip route",  # 非连通性查询
            "R-1连接到R-2吗？"
        ]
        
        for query in test_queries:
            is_connectivity = executor._is_connectivity_query(query)
            print(f"   查询: '{query}' -> 连通性查询: {is_connectivity}")
        
        # 4. 测试实际连通性分析
        print("\n5. 测试实际连通性分析...")
        connectivity_query = "ping R-2 from R-1"
        
        print(f"执行查询: {connectivity_query}")
        result = executor.execute_intelligent_query(
            connectivity_query, 
            devices_info, 
            target_device="R-1"
        )
        
        print("结果:")
        print(result)
        
        # 5. 测试设备IP获取
        print("\n6. 测试设备IP获取...")
        for device_name in ['R-1', 'R-2']:
            ip = executor._get_device_ip(device_name, devices_info)
            print(f"   {device_name} IP地址: {ip}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_connectivity_analysis()
