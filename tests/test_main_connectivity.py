#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
直接测试主程序的连通性分析功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入主程序的核心组件
from core.intelligent_processor import IntelligentProcessor
from core.llm_manager import LLMManager
from core.rag_enhanced_executor import RAGEnhancedCommandExecutor

def test_main_connectivity():
    """测试主程序的连通性分析功能"""
    print("=== 测试主程序连通性分析功能 ===\n")
    
    try:
        # 1. 初始化LLM
        print("1. 初始化LLM...")
        llm_manager = LLMManager()
        llm = llm_manager.init_llm()
        
        # 2. 初始化RAG增强执行器
        print("2. 初始化RAG增强执行器...")
        telnet_host = "192.168.102.1"
        executor = RAGEnhancedCommandExecutor(telnet_host, llm)
        
        # 3. 初始化工具
        print("3. 初始化GNS3工具...")
        from core.gns3_agent_tools import GNS3AgentTools
        server_url = "http://192.168.101.1:3080"
        telnet_host = "192.168.102.1"
        tools = GNS3AgentTools(server_url, telnet_host)
        
        # 4. 初始化智能处理器
        print("4. 初始化智能处理器...")
        processor = IntelligentProcessor(tools, llm)
        
        # 5. 测试连通性查询
        test_queries = [
            "ping R-6 from R-1",
            "test connectivity between R-1 and R-2",
            "检查R-1到R-6的连通性"
        ]
        
        for query in test_queries:
            print(f"\n{'='*50}")
            print(f"测试查询: {query}")
            print('='*50)
            
            # 模拟主程序的处理流程
            result = processor.process_user_request(query)
            print(f"处理结果:\n{result}")
        
        print("\n=== 测试完成 ===")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_connectivity()
