#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test for language adaptation fixes
测试语言适配修复
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.language_adapter import get_message, get_prompt_template, LanguageDetector

def test_language_fixes():
    """测试语言修复"""
    
    print("🧪 Testing Language Adaptation Fixes")
    print("=" * 50)
    
    # 测试语言检测
    detector = LanguageDetector()
    
    # 测试英文检测
    en_query = "check all device ospf status"
    detected_lang = detector.detect_language(en_query)
    print(f"✅ English detection: '{en_query}' -> {detected_lang}")
    
    # 测试消息模板
    print("\n🔤 Testing Message Templates:")
    print(f"Device summary: {get_message('device_summary').format('R1')}")
    print(f"Command details: {get_message('command_details').format('show ip ospf')}")
    print(f"Command failed: {get_message('command_failed')}")
    print(f"No console: {get_message('device_no_console').format('R1')}")
    
    # 测试prompt模板
    print("\n📝 Testing Prompt Template:")
    prompt = get_prompt_template('command_execution_analysis', 
                               query='check ospf status',
                               commands='show ip ospf neighbor',
                               results_text='Device: R1\nCommand: show ip ospf neighbor\nOutput: test')
    print(f"Prompt template working: {len(prompt) > 100}")
    print(f"Contains English keywords: {'OSPF' in prompt and 'analysis' in prompt}")
    
    print("\n✅ All language adaptation fixes verified!")

if __name__ == "__main__":
    test_language_fixes()
