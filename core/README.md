# Core Modules / 核心功能模块

This directory contains core functional modules for GNS3 network device management with intelligent AI processing and multi-language support.

本目录包含GNS3网络设备管理的核心功能模块，具备智能AI处理和多语言支持功能。

## 📄 Module Overview / 模块说明

### 🧠 Intelligent Processing Modules / 智能处理模块

- **intelligent_processor.py** - Intelligent Request Processor / 智能请求处理器
  - LLM-powered intent analysis / LLM驱动的意图分析
  - Multi-language prompt templates / 多语言提示模板
  - Context-aware response generation / 上下文感知的响应生成
  - Chat history management / 对话历史管理

- **language_adapter.py** - Multi-Language Adaptation System / 多语言适配系统
  - Automatic language detection (English/Chinese) / 自动语言检测（英中文）
  - Intelligent message template switching / 智能消息模板切换
  - English-first strategy with Chinese fallback / 英文优先的中文回退策略
  - Professional bilingual prompts for LLM / 专业的LLM双语提示

- **rag_enhanced_executor.py** - RAG Enhanced Command Executor / RAG增强命令执行器
  - Vector knowledge base integration / 向量知识库集成
  - Intelligent command recommendation / 智能命令推荐
  - Multi-source knowledge fusion / 多源知识融合
  - Context-aware command selection / 上下文感知的命令选择

- **network_rag_kb.py** - Network Troubleshooting RAG Knowledge Base / 网络排错RAG知识库
  - BGE-M3 embeddings with GPU acceleration / GPU加速的BGE-M3嵌入
  - FAISS vector store for fast retrieval / FAISS向量存储快速检索
  - Network documentation processing / 网络文档处理
  - Semantic search capabilities / 语义搜索功能

### 🛠️ Device Management Modules / 设备管理模块

- **get_topology_info.py** - Topology Information Retrieval / 拓扑信息获取模块
  - GNS3 project topology structure analysis / GNS3项目拓扑结构分析
  - Link summary information / 链路摘要信息
  - Node and connection analysis / 节点和连接分析

- **get_config_info.py** - Device Configuration Retrieval (Enhanced) / 设备配置获取模块（增强版）
  - Large configuration file handling / 超大配置文件处理
  - Intelligent completion detection / 智能完成检测
  - Multi-strategy retry mechanism / 多策略重试机制
  - 10-minute extended timeout support / 10分钟超长等待支持

- **get_project_info.py** - Project Information Management / 项目信息管理模块
  - GNS3 project basic information retrieval / GNS3项目基本信息获取
  - Project status monitoring / 项目状态监控
  - Project configuration management / 项目配置管理

- **get_all_devices_config.py** - Batch Device Configuration Collection / 批量设备配置收集
  - Batch multi-device configuration retrieval / 批量获取多设备配置
  - Unified configuration management / 统一配置管理
  - Result aggregation and storage / 结果汇总和保存

- **super_large_config_handler.py** - Super Large Configuration Handler / 超大配置专用处理器
  - Specialized handling for >10MB configuration files / 专门处理>10MB配置文件
  - Multiple retrieval strategies / 多种获取策略
  - Progress monitoring and status tracking / 进度监控和状态跟踪

- **gns3_agent_tools.py** - GNS3 Agent Tools / GNS3代理工具集
  - Unified interface for GNS3 operations / GNS3操作的统一接口
  - Context building and management / 上下文构建和管理
  - Device state monitoring / 设备状态监控

## 🌍 Multi-Language Features / 多语言特性

### Intelligent Language Detection / 智能语言检测
- **Character-based analysis** / 基于字符的分析
- **English-first strategy** / 英文优先策略
- **Automatic Chinese switching** / 自动中文切换
- **Consistent experience across all modules** / 所有模块的一致体验

### Bilingual Components / 双语组件
- **User interface messages** / 用户界面消息
- **LLM prompt templates** / LLM提示模板
- **Error handling and responses** / 错误处理和响应
- **Technical documentation** / 技术文档

## 🚀 Quick Start / 快速开始

### Basic Operations / 基础操作
```bash
# Get topology information / 获取拓扑信息
python get_topology_info.py

# Get device configuration (standard) / 获取设备配置（标准）
python get_config_info.py

# Batch configuration retrieval / 批量获取配置
python get_all_devices_config.py

# Handle super large configurations / 处理超大配置
python super_large_config_handler.py
```

### Intelligent Processing / 智能处理
```python
# Import intelligent processor / 导入智能处理器
from core.intelligent_processor import IntelligentProcessor
from core.gns3_agent_tools import GNS3AgentTools

# Initialize with LLM / 使用LLM初始化
tools = GNS3AgentTools()
processor = IntelligentProcessor(tools, llm)

# Process user request (auto-detects language) / 处理用户请求（自动检测语言）
response = processor.process_request("show ip ospf neighbor")
response = processor.process_request("查看OSPF邻居状态")
```

### Language Adaptation / 语言适配
```python
# Import language adapter / 导入语言适配器
from core.language_adapter import get_message, get_prompt_template

# Get localized messages / 获取本地化消息
message = get_message('analyzing_request')  # Auto-detects language / 自动检测语言

# Get localized prompts / 获取本地化提示
prompt = get_prompt_template('main_prompt', 
                           context="network analysis", 
                           user_input="show version")
```

## 🔧 Architecture / 系统架构

### Data Flow / 数据流
```
User Input → Language Detection → Intent Analysis → Command Selection → Execution → Response
用户输入 → 语言检测 → 意图分析 → 命令选择 → 执行 → 响应
```

### Integration / 集成方式
- **RAG Knowledge Base** / RAG知识库: Vector embeddings + FAISS search / 向量嵌入 + FAISS搜索
- **LLM Processing** / LLM处理: Ollama + DeepSeek models / Ollama + DeepSeek模型
- **Multi-Language** / 多语言: Character-based detection + template switching / 字符检测 + 模板切换

## 📊 Performance / 性能指标

- **Language Detection** / 语言检测: <1ms response time / <1毫秒响应时间
- **RAG Search** / RAG搜索: GPU-accelerated BGE-M3 embeddings / GPU加速BGE-M3嵌入
- **Configuration Handling** / 配置处理: Up to 10MB+ files / 支持10MB+文件
- **Multi-Language Support** / 多语言支持: English + Chinese seamless switching / 英中文无缝切换
