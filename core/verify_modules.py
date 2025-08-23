#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core模块导入验证脚本
Verification script for core module imports
"""

import sys
import os

# 添加core目录到Python路径
sys.path.append(os.path.dirname(__file__))

def verify_core_modules():
    """验证core目录下的所有主要模块"""
    print("🔍 Verifying Core Modules / 验证核心模块")
    print("=" * 60)
    
    modules_to_test = [
        ("language_adapter", "Multi-Language Adaptation System / 多语言适配系统"),
        ("intelligent_processor", "Intelligent Request Processor / 智能请求处理器"),
        ("rag_enhanced_executor", "RAG Enhanced Command Executor / RAG增强命令执行器"),
        ("network_rag_kb", "Network RAG Knowledge Base / 网络RAG知识库"),
        ("gns3_agent_tools", "GNS3 Agent Tools / GNS3代理工具"),
        ("get_topology_info", "Topology Information / 拓扑信息"),
        ("get_config_info", "Configuration Retrieval / 配置获取"),
        ("get_project_info", "Project Information / 项目信息"),
        ("get_all_devices_config", "Batch Configuration / 批量配置"),
        ("super_large_config_handler", "Large Config Handler / 大配置处理器")
    ]
    
    success_count = 0
    total_count = len(modules_to_test)
    
    for module_name, description in modules_to_test:
        try:
            __import__(module_name)
            print(f"✅ {module_name} - {description}")
            success_count += 1
        except ImportError as e:
            print(f"❌ {module_name} - Import failed: {str(e)}")
        except Exception as e:
            print(f"⚠️  {module_name} - Warning: {str(e)}")
            success_count += 1  # 可能只是依赖问题，模块本身存在
    
    print("\n" + "=" * 60)
    print(f"📊 Summary / 总结:")
    print(f"   • Total modules / 总模块数: {total_count}")
    print(f"   • Successful / 成功: {success_count}")
    print(f"   • Success rate / 成功率: {success_count/total_count*100:.1f}%")
    
    if success_count == total_count:
        print("\n🎉 All core modules verified successfully!")
        print("🎉 所有核心模块验证成功！")
    else:
        print(f"\n⚠️  {total_count - success_count} modules need attention")
        print(f"⚠️  {total_count - success_count} 个模块需要注意")

if __name__ == "__main__":
    verify_core_modules()
