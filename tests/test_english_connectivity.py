#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test English input/output for connectivity analysis
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.rag_enhanced_executor import RAGEnhancedCommandExecutor
from core.get_all_devices_config import DeviceConfigCollector
from core.language_adapter import language_adapter

def test_english_connectivity():
    """Test English input and output for connectivity analysis"""
    print("=== Testing English Connectivity Analysis ===\n")
    
    try:
        # Force English mode
        print("1. Setting language to English...")
        from core.language_adapter import LanguageConfig
        language_adapter.current_config = LanguageConfig(use_english=True, mixed_mode=False, tech_terms_english=True)
        print(f"Language mode: English = {language_adapter.current_config.use_english}")
        
        # 2. Get device info
        print("\n2. Getting device configuration...")
        config_collector = DeviceConfigCollector()
        opened_projects, topology_data = config_collector.get_topology_info()
        
        if not topology_data:
            print("❌ Failed to get topology information")
            return
        
        # Extract device info from topology data
        devices_info = []
        for project_name, project_data in topology_data.items():
            configurable_devices = config_collector.filter_configurable_devices(project_data['nodes'])
            devices_info.extend(configurable_devices)
        
        if not devices_info:
            print("❌ No devices found")
            return
        
        print(f"✅ Found {len(devices_info)} devices")
        for device in devices_info:
            print(f"   - {device['name']} (port: {device['console']})")
        
        # 3. Create RAG enhanced executor
        print("\n3. Initializing RAG enhanced executor...")
        
        class MockLLM:
            def invoke(self, prompt):
                return "show ip interface brief"
        
        mock_llm = MockLLM()
        telnet_host = "192.168.102.1"
        
        executor = RAGEnhancedCommandExecutor(telnet_host, mock_llm)
        
        # 4. Test English connectivity queries
        print("\n4. Testing English connectivity queries...")
        test_queries = [
            "ping R-2 from R-1",
            "test connectivity between R-1 and R-6", 
            "check connectivity R-1 to R-2"
        ]
        
        for query in test_queries:
            print(f"\n{'='*60}")
            print(f"Query: {query}")
            print('='*60)
            
            result = executor.execute_intelligent_query(
                query, 
                devices_info, 
                target_device="R-1"
            )
            
            print("Result:")
            print(result)
        
        print("\n=== Test completed ===")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_english_connectivity()
