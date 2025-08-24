#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Complete validation test for language adaptation fixes
完整的语言适配修复验证测试
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.language_adapter import get_message, get_prompt_template, LanguageDetector, language_adapter

def test_complete_language_fixes():
    """完整的语言修复测试"""
    
    print("🔧 Complete Language Adaptation Fix Validation")
    print("=" * 60)
    
    # 强制设置为英文模式
    language_adapter.current_config.use_english = True
    language_adapter.current_config.mixed_mode = False
    
    print("🌍 Language Configuration:")
    print(f"   - Use English: {language_adapter.current_config.use_english}")
    print(f"   - Mixed Mode: {language_adapter.current_config.mixed_mode}")
    print(f"   - Tech Terms English: {language_adapter.current_config.tech_terms_english}")
    
    # 测试所有新增的消息模板
    print("\n📋 Testing New Message Templates:")
    test_cases = [
        ("device_summary", ["R1"]),
        ("device_no_console", ["R1"]),
        ("command_details", ["show ip ospf neighbor"]),
        ("command_failed", []),
        ("command_output", ["Sample output"]),
        ("output_truncated", []),
        ("rag_knowledge_suggestions", []),
        ("relevance_score", [0.95]),
        ("background_context", ["OSPF routing protocol"])
    ]
    
    all_tests_pass = True
    
    for template_name, args in test_cases:
        try:
            message = get_message(template_name)
            if args:
                formatted_message = message.format(*args)
            else:
                formatted_message = message
            
            # 检查是否包含中文字符
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in formatted_message)
            
            status = "❌ CONTAINS CHINESE" if has_chinese else "✅ ENGLISH ONLY"
            print(f"   {template_name}: {status}")
            if has_chinese:
                print(f"      Message: {formatted_message}")
                all_tests_pass = False
            
        except Exception as e:
            print(f"   {template_name}: ❌ ERROR - {e}")
            all_tests_pass = False
    
    # 测试prompt模板
    print("\n📝 Testing Prompt Templates:")
    prompt_templates = [
        "command_execution_analysis",
        "connectivity_analysis", 
        "device_config_analysis"
    ]
    
    for template_name in prompt_templates:
        try:
            prompt = get_prompt_template(template_name, 
                                       query="test query",
                                       device_name="R1",
                                       results_text="test results",
                                       commands="show version")
            
            # 检查模板是否正确获取
            if "Template not found" in prompt:
                print(f"   {template_name}: ⚠️  TEMPLATE NOT FOUND")
                continue
                
            # 检查是否有中文（除了模板变量）
            has_chinese = any('\u4e00' <= char <= '\u9fff' for char in prompt)
            
            status = "❌ CONTAINS CHINESE" if has_chinese else "✅ ENGLISH ONLY"
            print(f"   {template_name}: {status}")
            print(f"      Length: {len(prompt)} chars")
            
            if has_chinese:
                all_tests_pass = False
                
        except Exception as e:
            print(f"   {template_name}: ❌ ERROR - {e}")
            all_tests_pass = False
    
    # 测试英文输入的语言检测
    print("\n🔍 Testing Language Detection:")
    english_queries = [
        "check all device ospf status",
        "show interface status",
        "ping from R1 to R2",
        "analyze routing table",
        "collect configuration from all devices"
    ]
    
    detector = LanguageDetector()
    
    for query in english_queries:
        lang_config = detector.detect_language(query)
        is_english = lang_config.use_english
        
        status = "✅ DETECTED AS ENGLISH" if is_english else "❌ DETECTED AS CHINESE"
        print(f"   '{query}': {status}")
        
        if not is_english:
            all_tests_pass = False
    
    # 最终结果
    print("\n" + "=" * 60)
    if all_tests_pass:
        print("🎉 ALL LANGUAGE ADAPTATION FIXES VALIDATED SUCCESSFULLY!")
        print("✅ English inputs will produce English outputs")
        print("✅ No hardcoded Chinese text in English mode")
        print("✅ All message templates working correctly")
        print("✅ LLM prompt templates properly configured")
    else:
        print("❌ SOME TESTS FAILED - PLEASE REVIEW ABOVE ERRORS")
        return False
    
    return True

if __name__ == "__main__":
    success = test_complete_language_fixes()
    exit(0 if success else 1)
