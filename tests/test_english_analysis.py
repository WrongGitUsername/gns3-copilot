#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test English language adaptation for analysis reports
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.intelligent_processor import IntelligentProcessor
from core.llm_manager import LLMManager
from core.gns3_agent_tools import GNS3AgentTools
from core.language_adapter import language_adapter, LanguageConfig

def test_english_analysis_report():
    """Test English output for analysis reports"""
    print("=== Testing English Analysis Report ===\n")
    
    try:
        # 1. Force English mode
        print("1. Setting language to English...")
        language_adapter.current_config = LanguageConfig(use_english=True, mixed_mode=False, tech_terms_english=True)
        print(f"Language mode: English = {language_adapter.current_config.use_english}")
        
        # 2. Initialize components
        print("\n2. Initializing components...")
        llm_manager = LLMManager()
        llm = llm_manager.init_llm()
        
        server_url = "http://192.168.101.1:3080"
        telnet_host = "192.168.102.1"
        tools = GNS3AgentTools(server_url, telnet_host)
        
        processor = IntelligentProcessor(tools, llm)
        
        # 3. Test English queries that should produce analysis reports
        print("\n3. Testing English queries...")
        test_queries = [
            "Check R-2 R-3 R-5 ospf status",
            "Show interface status on R-1",
            "Check routing table on R-2"
        ]
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print('='*60)
            
            # Ensure English mode is set for each query
            language_adapter.update_language_config(query)
            language_adapter.current_config = LanguageConfig(use_english=True, mixed_mode=False, tech_terms_english=True)
            
            result = processor.process_user_request(query)
            
            # Print first 500 characters to check for Chinese text
            result_preview = result[:500] + "..." if len(result) > 500 else result
            print("Result preview:")
            print(result_preview)
            
            # Check for Chinese characters
            import re
            chinese_pattern = re.compile(r'[\u4e00-\u9fff]')
            chinese_chars = chinese_pattern.findall(result_preview)
            
            if chinese_chars:
                print(f"\n⚠️ Found Chinese characters: {set(chinese_chars)}")
            else:
                print("\n✅ No Chinese characters found in preview")
        
        print("\n=== Test completed ===")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_english_analysis_report()
