#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG知识库安装和初始化脚本
"""

import sys
import subprocess
import os
from pathlib import Path

def install_dependencies():
    """安装所有依赖"""
    print("📦 安装项目依赖...")
    
    # 安装基础依赖
    result = subprocess.run([
        sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
    ], capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"❌ 基础依赖安装失败: {result.stderr}")
        return False
    
    print("✅ 基础依赖安装完成")
    
    # 安装GPU版本的PyTorch（如果有GPU）
    try:
        import torch
        if torch.cuda.is_available():
            print("🚀 检测到GPU，安装GPU版本PyTorch...")
            gpu_result = subprocess.run([
                sys.executable, "-m", "pip", "install", 
                "torch", "torchvision", "torchaudio", 
                "--index-url", "https://download.pytorch.org/whl/cu124"
            ], capture_output=True, text=True)
            
            if gpu_result.returncode == 0:
                print("✅ GPU版本PyTorch安装成功")
            else:
                print("⚠️  GPU版本PyTorch安装失败，将使用CPU版本")
    except ImportError:
        print("💻 使用CPU版本PyTorch")
    
    return True
    """安装RAG相关依赖"""
    print("🔧 正在安装RAG依赖...")
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "-r", "requirements_rag.txt"
        ])
        print("✅ RAG依赖安装成功")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ 依赖安装失败: {e}")
        return False
    except FileNotFoundError:
        print("❌ 未找到requirements_rag.txt文件")
        return False

def initialize_rag_system():
    """初始化RAG系统"""
    print("🧠 正在初始化RAG系统...")
    
    try:
        from core.network_rag_kb import create_sample_knowledge_base, NetworkTroubleshootingRAG
        
        # 创建示例知识库
        create_sample_knowledge_base()
        
        # 初始化RAG系统
        rag = NetworkTroubleshootingRAG()
        
        print("✅ RAG系统初始化成功")
        return True
        
    except ImportError as e:
        print(f"❌ RAG模块导入失败: {e}")
        print("请先安装依赖: python setup_rag.py --install")
        return False
    except Exception as e:
        print(f"❌ RAG系统初始化失败: {e}")
        return False

def enable_rag_config():
    """启用RAG配置"""
    import configparser
    
    config_path = Path("rag_config.ini")
    config = configparser.ConfigParser()
    
    if config_path.exists():
        config.read(config_path)
    
    # 确保有rag section
    if 'rag' not in config:
        config.add_section('rag')
    
    # 启用RAG
    config.set('rag', 'enabled', 'true')
    
    # 写入配置
    with open(config_path, 'w') as f:
        config.write(f)
    
    print("✅ RAG配置已启用")

def test_rag_system():
    """测试RAG系统"""
    print("🧪 正在测试RAG系统...")
    
    try:
        from core.rag_enhanced_executor import RAGEnhancedCommandExecutor
        from core.llm_manager import LLMManager
        
        # 初始化LLM
        llm_manager = LLMManager()
        
        # 创建RAG执行器
        executor = RAGEnhancedCommandExecutor(
            telnet_host="192.168.102.1",
            llm=llm_manager.current_model,
            use_rag=True
        )
        
        # 测试查询
        test_query = "OSPF邻居建立问题"
        commands = executor._get_relevant_commands_enhanced(test_query)
        
        print(f"🔍 测试查询: {test_query}")
        print(f"📋 找到 {len(commands)} 个相关命令")
        
        for i, cmd in enumerate(commands[:3], 1):
            print(f"  {i}. {cmd['command']} [{cmd.get('source', 'unknown')}]")
        
        print("✅ RAG系统测试成功")
        return True
        
    except Exception as e:
        print(f"❌ RAG系统测试失败: {e}")
        return False

def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG知识库设置脚本")
    parser.add_argument("--install", action="store_true", help="安装RAG依赖")
    parser.add_argument("--init", action="store_true", help="初始化RAG系统")
    parser.add_argument("--enable", action="store_true", help="启用RAG配置")
    parser.add_argument("--test", action="store_true", help="测试RAG系统")
    parser.add_argument("--all", action="store_true", help="执行所有步骤")
    
    args = parser.parse_args()
    
    if not any(vars(args).values()):
        print("RAG知识库设置脚本")
        print("=" * 50)
        print("用法:")
        print("  python setup_rag.py --install  # 安装依赖")
        print("  python setup_rag.py --init     # 初始化系统")
        print("  python setup_rag.py --enable   # 启用配置")
        print("  python setup_rag.py --test     # 测试系统")
        print("  python setup_rag.py --all      # 执行所有步骤")
        return
    
    success = True
    
    if args.all or args.install:
        success &= install_dependencies()
    
    if success and (args.all or args.init):
        success &= initialize_rag_system()
    
    if success and (args.all or args.enable):
        enable_rag_config()
    
    if success and (args.all or args.test):
        test_rag_system()
    
    if success:
        print("\n🎉 RAG系统设置完成！")
        print("现在您可以:")
        print("1. 将网络排错书籍放入 ./knowledge_base/ 目录")
        print("2. 支持的格式: PDF, TXT, MD, DOCX")
        print("3. 重新启动系统后，RAG功能将自动生效")
    else:
        print("\n❌ 设置过程中出现错误，请检查上述信息")

if __name__ == "__main__":
    main()
