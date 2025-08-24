#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG-based network command knowledge base.

Uses LangChain to vectorize network troubleshooting books and intelligently retrieve related commands.
"""

import os
import sys
from typing import List, Dict, Optional
from pathlib import Path

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

# Import language adapter
try:
    from .language_adapter import get_message, language_adapter
    LANGUAGE_ADAPTER_AVAILABLE = True
except ImportError:
    LANGUAGE_ADAPTER_AVAILABLE = False

try:
    # Try new version import (langchain-huggingface)
    from langchain_huggingface import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    from langchain_community.document_loaders import (
        PyPDFLoader, 
        TextLoader, 
        UnstructuredMarkdownLoader,
        DirectoryLoader
    )
except ImportError:
    try:
        # Fallback to community version
        from langchain_community.embeddings import HuggingFaceEmbeddings
        from langchain_community.vectorstores import FAISS
        from langchain_community.document_loaders import (
            PyPDFLoader, 
            TextLoader, 
            UnstructuredMarkdownLoader,
            DirectoryLoader
        )
    except ImportError:
        # Final fallback to old version import
        from langchain.embeddings import HuggingFaceEmbeddings
        from langchain.vectorstores import FAISS
        from langchain.document_loaders import (
            PyPDFLoader, 
            TextLoader, 
            UnstructuredMarkdownLoader,
            DirectoryLoader
        )

from .bge_m3_config import BGEM3Config

class NetworkTroubleshootingRAG:
    """网络排错RAG知识库"""
    
    def __init__(self, knowledge_base_path: str = "./knowledge_base", 
                 vector_store_path: str = "./vector_store",
                 config_path: str = "rag_config.ini"):
        """
        初始化RAG知识库
        
        Args:
            knowledge_base_path: 知识库文档路径
            vector_store_path: 向量存储路径
            config_path: BGE-M3配置文件路径
        """
        self.knowledge_base_path = Path(knowledge_base_path)
        self.vector_store_path = Path(vector_store_path)
        
        # 加载BGE-M3配置
        self.config = BGEM3Config(config_path)
        
        # 确保目录存在
        self.knowledge_base_path.mkdir(exist_ok=True)
        self.vector_store_path.mkdir(exist_ok=True)
        
        # 使用配置初始化嵌入模型
        embedding_config = self.config.get_embedding_config()
        self.embeddings = HuggingFaceEmbeddings(**embedding_config)
        
        # 使用配置初始化文本分割器
        splitter_config = self.config.get_text_splitter_config()
        self.text_splitter = RecursiveCharacterTextSplitter(**splitter_config)
        
        self.vector_store = None
        self._load_or_create_vector_store()
    
    def build_vector_store(self):
        """构建向量存储（重新处理所有文档）"""
        if LANGUAGE_ADAPTER_AVAILABLE:
            print(get_message("vector_store_rebuilding"))
        else:
            print("🔄 Force rebuilding vector store...")
        
        # 删除现有向量存储
        if self.vector_store_path.exists():
            import shutil
            shutil.rmtree(self.vector_store_path)
            self.vector_store_path.mkdir(exist_ok=True)
        
        # 重新调用add_documents_from_directory来重建
        success = self.add_documents_from_directory()
        if success:
            if LANGUAGE_ADAPTER_AVAILABLE:
                print(get_message("vector_store_rebuilt"))
            else:
                print("✅ Vector store rebuild completed")
        else:
            if LANGUAGE_ADAPTER_AVAILABLE:
                print(get_message("no_documents_for_vector_store"))
            else:
                print("❌ No documents available for building vector store")
    
    def add_documents_from_directory(self, directory_path: str = None):
        """从目录加载并向量化文档"""
        if directory_path is None:
            directory_path = self.knowledge_base_path
            
        if LANGUAGE_ADAPTER_AVAILABLE:
            print(get_message("loading_documents_from", directory_path))
        else:
            print(f"📚 Starting to load documents from: {directory_path}")
        
        # 支持多种文档格式
        loaders = [
            DirectoryLoader(directory_path, glob="**/*.pdf", loader_cls=PyPDFLoader),
            DirectoryLoader(directory_path, glob="**/*.txt", loader_cls=TextLoader),
            DirectoryLoader(directory_path, glob="**/*.md", loader_cls=UnstructuredMarkdownLoader),
        ]
        
        documents = []
        for loader in loaders:
            try:
                docs = loader.load()
                documents.extend(docs)
                if LANGUAGE_ADAPTER_AVAILABLE:
                    print(get_message("documents_loaded", len(docs)))
                else:
                    print(f"✅ Loaded {len(docs)} documents")
            except Exception as e:
                if LANGUAGE_ADAPTER_AVAILABLE:
                    print(get_message("document_loading_error", str(e)))
                else:
                    print(f"⚠️ Error loading documents: {e}")
        
        if not documents:
            if LANGUAGE_ADAPTER_AVAILABLE:
                print(get_message("no_documents_for_vector_store"))
            else:
                print("❌ No documents found")
            return False
        
        # 分割文档
        if LANGUAGE_ADAPTER_AVAILABLE:
            print(get_message("splitting_documents"))
        else:
            print("🔧 Splitting documents...")
        split_docs = self.text_splitter.split_documents(documents)
        if LANGUAGE_ADAPTER_AVAILABLE:
            print(get_message("documents_split", len(split_docs)))
        else:
            print(f"📄 Split into {len(split_docs)} document chunks")
        
        # 创建向量存储
        if LANGUAGE_ADAPTER_AVAILABLE:
            print(get_message("creating_vector_embeddings"))
        else:
            print("🧠 Creating vector embeddings...")
        self.vector_store = FAISS.from_documents(split_docs, self.embeddings)
        
        # 保存向量存储
        self.vector_store.save_local(str(self.vector_store_path))
        if LANGUAGE_ADAPTER_AVAILABLE:
            print(get_message("vector_store_saved", str(self.vector_store_path)))
        else:
            print(f"💾 Vector store saved to: {self.vector_store_path}")
        
        return True
    
    def _load_or_create_vector_store(self):
        """加载现有向量存储或创建新的"""
        try:
            if (self.vector_store_path / "index.faiss").exists():
                if LANGUAGE_ADAPTER_AVAILABLE:
                    print(get_message("vector_store_loading"))
                else:
                    print("📖 Loading existing vector store...")
                self.vector_store = FAISS.load_local(
                    str(self.vector_store_path), 
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                if LANGUAGE_ADAPTER_AVAILABLE:
                    print(get_message("vector_store_loaded"))
                else:
                    print("✅ Vector store loaded successfully")
            else:
                if LANGUAGE_ADAPTER_AVAILABLE:
                    print(get_message("vector_store_not_found"))
                else:
                    print("🆕 No existing vector store found, will create new one...")
                self.add_documents_from_directory()
        except Exception as e:
            if LANGUAGE_ADAPTER_AVAILABLE:
                print(get_message("vector_store_load_failed", str(e)))
            else:
                print(f"❌ Failed to load vector store: {e}")
            self.vector_store = None
    
    def search_commands(self, query: str, k: int = 5) -> List[Dict]:
        """基于查询检索相关命令和解决方案"""
        if not self.vector_store:
            if LANGUAGE_ADAPTER_AVAILABLE:
                print(get_message("vector_store_not_initialized"))
            else:
                print("❌ Vector store not initialized")
            return []
        
        try:
            # 检索相关文档
            docs = self.vector_store.similarity_search(query, k=k)
            
            results = []
            for i, doc in enumerate(docs):
                # 提取命令和描述
                commands = self._extract_commands_from_text(doc.page_content)
                
                result = {
                    "score": 1.0 - (i * 0.1),  # 简单的相关性评分
                    "content": doc.page_content,
                    "commands": commands,
                    "source": doc.metadata.get("source", "unknown"),
                    "summary": doc.page_content[:200] + "..." if len(doc.page_content) > 200 else doc.page_content
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            print(f"❌ 检索失败: {e}")
            return []
    
    def _extract_commands_from_text(self, text: str) -> List[str]:
        """从文本中提取网络命令"""
        import re
        
        # 常见网络命令模式
        command_patterns = [
            r'show\s+[\w\s-]+',
            r'debug\s+[\w\s-]+',
            r'ping\s+[\w.]+',
            r'traceroute\s+[\w.]+',
            r'telnet\s+[\w.]+',
            r'ssh\s+[\w.@]+',
            r'configure\s+terminal',
            r'interface\s+[\w/]+',
            r'router\s+\w+',
            r'ip\s+[\w\s-]+',
        ]
        
        commands = []
        for pattern in command_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            commands.extend(matches)
        
        # 去重并清理
        unique_commands = list(set(commands))
        return [cmd.strip() for cmd in unique_commands if len(cmd.strip()) > 5]

def create_sample_knowledge_base():
    """创建示例知识库"""
    kb_path = Path("./knowledge_base")
    kb_path.mkdir(exist_ok=True)
    
    # 创建示例文档
    sample_docs = [
        {
            "filename": "ospf_troubleshooting.md",
            "content": """# OSPF故障排除指南

## OSPF邻居关系问题

### 问题描述
OSPF邻居无法建立或处于非FULL状态

### 诊断命令
- `show ip ospf neighbor` - 查看OSPF邻居状态
- `show ip ospf interface` - 查看OSPF接口配置
- `show ip ospf database` - 查看OSPF链路状态数据库
- `debug ip ospf adj` - 调试OSPF邻接过程

### 常见解决方案
1. 检查区域ID是否匹配
2. 验证Hello间隔和Dead间隔
3. 确认认证配置
4. 检查网络类型设置

## OSPF路由宣告问题

### 问题描述
OSPF路由未正确宣告或学习

### 诊断命令
- `show ip route ospf` - 查看OSPF学习的路由
- `show ip ospf database router` - 查看路由器LSA
- `show running-config | section router ospf` - 查看OSPF配置

### 解决方案
1. 检查network语句
2. 验证区域配置
3. 检查路由过滤设置
"""
        },
        {
            "filename": "bgp_troubleshooting.md", 
            "content": """# BGP故障排除指南

## BGP邻居建立问题

### 问题描述
BGP邻居无法建立或处于非Established状态

### 诊断命令
- `show ip bgp summary` - 查看BGP邻居摘要
- `show ip bgp neighbors` - 查看详细邻居信息
- `debug ip bgp` - 调试BGP进程
- `show tcp brief` - 查看TCP连接状态

### 常见原因
1. AS号不匹配
2. 邻居地址配置错误
3. TCP连接问题
4. 认证失败

## BGP路由传播问题

### 诊断命令
- `show ip bgp` - 查看BGP路由表
- `show ip route bgp` - 查看BGP学习的路由
- `show ip bgp neighbors advertised-routes` - 查看宣告给邻居的路由
- `show ip bgp neighbors received-routes` - 查看从邻居接收的路由
"""
        },
        {
            "filename": "interface_troubleshooting.md",
            "content": """# 接口故障排除

## 接口状态问题

### 诊断命令
- `show interfaces` - 查看所有接口状态
- `show ip interface brief` - 查看接口简要信息
- `show interface description` - 查看接口描述
- `show controllers` - 查看物理层信息

## 接口性能问题

### 诊断命令
- `show interfaces counters` - 查看接口计数器
- `show interfaces statistics` - 查看接口统计信息
- `ping` - 测试连通性
- `traceroute` - 追踪路径
"""
        }
    ]
    
    # 写入示例文档
    for doc in sample_docs:
        file_path = kb_path / doc["filename"]
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(doc["content"])
    
    print(f"✅ 示例知识库已创建在: {kb_path}")

if __name__ == "__main__":
    # 创建示例知识库
    create_sample_knowledge_base()
    
    # 初始化RAG系统
    rag = NetworkTroubleshootingRAG()
    
    # 测试查询
    test_queries = [
        "OSPF邻居无法建立",
        "BGP路由宣告问题", 
        "接口状态异常",
        "路由器连接问题"
    ]
    
    for query in test_queries:
        print(f"\n🔍 查询: {query}")
        results = rag.search_commands(query, k=3)
        
        for i, result in enumerate(results, 1):
            print(f"\n📋 结果 {i} (相关性: {result['score']:.2f}):")
            print(f"📄 来源: {result['source']}")
            print(f"📝 摘要: {result['summary']}")
            if result['commands']:
                print(f"🔧 相关命令: {', '.join(result['commands'][:3])}")
