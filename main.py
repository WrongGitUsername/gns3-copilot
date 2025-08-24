#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GNS3 Smart Agent System v6.0.

Simplified network device management intelligent agent based on LangChain + Ollama.
Refactored version - Modular design.
"""

import os
import sys
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add project root directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import core modules
try:
    from core.llm_manager import LLMManager
    from core.gns3_agent_tools import GNS3AgentTools
    from core.intelligent_processor import IntelligentProcessor
    from core.language_adapter import language_adapter, get_message, update_language
except ImportError as e:
    print(f"❌ Core module import failed: {e}")
    print("Please ensure all modules in the core directory exist")
    sys.exit(1)


class GNS3SmartAgent:
    """GNS3 Smart Agent - Refactored version."""
    
    def __init__(self):
        self.server_url = os.getenv("GNS3_SERVER_URL", "http://192.168.101.1:3080")
        self.telnet_host = os.getenv("GNS3_TELNET_HOST", "192.168.102.1")
        
        # Ensure default use of English
        language_adapter.current_config.use_english = True
        
        print(f"🔧 GNS3 Server: {self.server_url}")
        print(f"🔧 Telnet Host: {self.telnet_host}")
        
        # Initialize LLM manager
        print(get_message("initializing_llm"))
        self.llm_manager = LLMManager()
        self.llm = self.llm_manager.init_llm()
        print(get_message("current_model", self.llm_manager.get_current_model_info().split(":")[0], 
                         self.llm_manager.get_current_model_info().split(":")[1]))
        
        # Initialize toolset
        print(get_message("initializing_toolset"))
        self.tools = GNS3AgentTools(self.server_url, self.telnet_host)
        
        # Initialize intelligent processor
        print(get_message("initializing_processor"))
        self.processor = IntelligentProcessor(self.tools, self.llm)
        
        print(get_message("agent_initialized"))
    
    def process_request(self, user_input: str) -> str:
        """Process user request."""
        # Update language configuration
        update_language(user_input)
        return self.processor.process_user_request(user_input)
    
    def run(self):
        """Run the intelligent agent."""
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
                
                # Process request
                start_time = datetime.now()
                response = self.process_request(user_input)
                end_time = datetime.now()
                
                # Display response (adjust according to current language configuration)
                if language_adapter.current_config.use_english:
                    print(f"\n🤖 Assistant: {response}")
                else:
                    print(f"\n🤖 助手: {response}")
                
                # Display processing time
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
    """Main function."""
    try:
        agent = GNS3SmartAgent()
        agent.run()
    except Exception as e:
        print(f"❌ Startup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
