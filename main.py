#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNS3 智能Agent系统 v6.0
基于 LangChain + Ollama 的简化版网络设备管理智能体
重构版本 - 模块化设计
"""

import os
import sys
from datetime import datetime

# 加载环境变量
from dotenv import load_dotenv
load_dotenv()

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 导入核心模块
try:
    from core.llm_manager import LLMManager
    from core.gns3_agent_tools import GNS3AgentTools
    from core.intelligent_processor import IntelligentProcessor
    from core.language_adapter import language_adapter, get_message, update_language
except ImportError as e:
    print(f"❌ 核心模块导入失败: {e}")
    print("请确保 core 目录下的所有模块都存在")
    sys.exit(1)


class GNS3SmartAgent:
    """GNS3智能代理 - 重构版"""
    
    def __init__(self):
        self.server_url = os.getenv("GNS3_SERVER_URL", "http://192.168.101.1:3080")
        self.telnet_host = os.getenv("GNS3_TELNET_HOST", "192.168.102.1")
        
        # 确保默认使用英文
        language_adapter.current_config.use_english = True
        
        print(f"🔧 GNS3 Server: {self.server_url}")
        print(f"🔧 Telnet Host: {self.telnet_host}")
        
        # 初始化LLM管理器
        print(get_message("initializing_llm"))
        self.llm_manager = LLMManager()
        self.llm = self.llm_manager.init_llm()
        print(get_message("current_model", self.llm_manager.get_current_model_info().split(":")[0], 
                         self.llm_manager.get_current_model_info().split(":")[1]))
        
        # 初始化工具集
        print(get_message("initializing_toolset"))
        self.tools = GNS3AgentTools(self.server_url, self.telnet_host)
        
        # 初始化智能处理器
        print(get_message("initializing_processor"))
        self.processor = IntelligentProcessor(self.tools, self.llm)
        
        print(get_message("agent_initialized"))
    
    def process_request(self, user_input: str) -> str:
        """处理用户请求"""
        # 更新语言配置
        update_language(user_input)
        return self.processor.process_user_request(user_input)
    
    def run(self):
        """运行智能代理"""
        print("\n" + "="*70)
        print(get_message("app_title"))
        print(get_message("app_description"))
        print(get_message("app_version"))
        print("="*70)
        
        print(f"\n{get_message('usage_examples')}")
        print(get_message("example_topology"))
        print(get_message("example_devices"))
        print(get_message("example_config"))
        print(get_message("example_interfaces"))
        print(get_message("example_summary"))
        print(get_message("example_status"))
        print(get_message("example_project"))
        
        print(f"\n🧠 {get_message('current_model', self.llm_manager.get_current_model_info().split(':')[0].strip(), self.llm_manager.get_current_model_info().split(':')[1].strip())}")
        print(f"\n{get_message('chat_start')}")
        print("-" * 50)
        
        while True:
            try:
                user_input = input(f"\n{get_message('user_prompt')}").strip()
                
                if user_input.lower() in ['quit', 'exit', '退出', 'q']:
                    print(f"\n{get_message('goodbye')}")
                    break
                
                if not user_input:
                    continue
                
                # 处理请求
                start_time = datetime.now()
                response = self.process_request(user_input)
                end_time = datetime.now()
                
                # 显示回复（根据当前语言配置调整）
                if language_adapter.current_config.use_english:
                    print(f"\n🤖 Assistant: {response}")
                else:
                    print(f"\n🤖 助手: {response}")
                
                # 显示处理时间
                processing_time = (end_time - start_time).total_seconds()
                if language_adapter.current_config.use_english:
                    print(f"\n⏱️ Processing time: {processing_time:.2f} seconds")
                else:
                    print(f"\n⏱️ 处理时间: {processing_time:.2f}秒")
                print("-" * 50)
                
            except KeyboardInterrupt:
                print(f"\n\n{get_message('goodbye')}")
                break
            except EOFError:
                print(f"\n\n{get_message('goodbye')}")
                break
            except Exception as e:
                print(f"\n{get_message('error_occurred', str(e))}")
                print(get_message('please_retry'))


def main():
    """主函数"""
    try:
        agent = GNS3SmartAgent()
        agent.run()
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
