#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试语言适配功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.language_adapter import language_adapter, get_message, LanguageDetector

def test_language_detection():
    """测试语言检测功能"""
    print("=== 语言检测测试 ===")
    
    detector = LanguageDetector()
    
    # 测试英文输入
    test_cases = [
        "list all devices",
        "show ospf neighbors", 
        "get router configuration",
        "列出所有设备",
        "查看ospf邻居",
        "获取路由器配置",
        "check R-1 interface status",
        "检查R-1接口状态"
    ]
    
    for query in test_cases:
        detected_lang = detector.detect_language(query)
        lang_str = "英文" if detected_lang.use_english else "中文"
        print(f"输入: '{query}' -> 检测语言: {lang_str} (use_english: {detected_lang.use_english})")
    
def test_message_display():
    """测试消息显示功能"""
    print("\n=== 消息显示测试 ===")
    
    # 测试英文消息
    language_adapter.update_language_config("show interface status")
    print("English messages:")
    print(f"- {get_message('analyzing_request')}")
    print(f"- {get_message('getting_project_summary')}")
    print(f"- {get_message('executing_command').format('show ip route')}")
    
    # 测试中文消息
    language_adapter.update_language_config("显示接口状态")
    print("\nChinese messages:")
    print(f"- {get_message('analyzing_request')}")
    print(f"- {get_message('getting_project_summary')}")
    print(f"- {get_message('executing_command').format('show ip route')}")

def test_auto_switching():
    """测试自动语言切换"""
    print("\n=== 自动语言切换测试 ===")
    
    # 模拟英文用户查询
    english_query = "show interface status"
    language_adapter.update_language_config(english_query)
    print(f"English query: '{english_query}'")
    print(f"Message: {get_message('analyzing_request')}")
    
    # 模拟中文用户查询
    chinese_query = "显示接口状态"
    language_adapter.update_language_config(chinese_query)
    print(f"\nChinese query: '{chinese_query}'")
    print(f"Message: {get_message('analyzing_request')}")

if __name__ == "__main__":
    test_language_detection()
    test_message_display()
    test_auto_switching()
    
    print("\n✅ 语言适配测试完成")
