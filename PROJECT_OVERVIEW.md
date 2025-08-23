# GNS3 Intelligent Agent / GNS3 智能代理

## 🌟 English Overview

### Project Description

**GNS3 Intelligent Agent v6.0** is an advanced network device management system powered by AI technologies. This intelligent agent combines Large Language Models (LLM), Retrieval-Augmented Generation (RAG), and multi-language support to provide a comprehensive solution for GNS3 network environment management and analysis.

### 🎯 Key Features

#### 🧠 AI-Powered Intelligence
- **LLM Integration**: Support for multiple models (DeepSeek, Ollama, OpenAI-compatible APIs)
- **RAG Enhancement**: Vector knowledge base with BGE-M3 embeddings and FAISS search
- **Intelligent Command Selection**: Context-aware network command recommendation
- **Natural Language Processing**: Understands complex network management queries

#### 🌍 Multi-Language Support
- **English-First Strategy**: Default English interface with seamless Chinese switching
- **Intelligent Language Detection**: Automatic language recognition based on user input
- **Bilingual Templates**: Professional dual-language prompts and responses
- **Technical Term Consistency**: Network terminology remains in English for accuracy

#### 📚 Advanced Knowledge Management
- **RAG Knowledge Base**: Vectorized network troubleshooting documentation
- **Multiple Knowledge Sources**: RAG, basic command library, keyword search
- **Document Processing**: Support for PDF, TXT, MD, DOCX formats
- **GPU-Accelerated Embeddings**: High-performance vector search with FAISS

#### 🛠️ Comprehensive Network Management
- **Device Configuration Retrieval**: Batch configuration collection with large file support
- **Topology Analysis**: Network structure visualization and analysis
- **Interface Connection Mapping**: Device interconnection discovery
- **Project Information Management**: GNS3 project status monitoring

#### 🔧 Enterprise-Grade Features
- **Modular Architecture**: Clean separation of concerns and extensible design
- **Error Handling**: Robust error recovery and user-friendly feedback
- **Configuration Management**: Flexible system configuration through INI files
- **Performance Optimization**: Optimized for large network environments

### 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Input    │ -> │ Language Adapter│ -> │ Intent Analysis │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │
          v                       v                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Command Selection│ <- │  RAG Knowledge  │ <- │ LLM Processing  │
└─────────────────┘    │     Base        │    └─────────────────┘
          │            └─────────────────┘                │
          v                       │                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ GNS3 Execution  │    │ Vector Search   │    │ Response Format │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 📦 Installation & Setup

#### Prerequisites
- Python 3.8+
- CUDA-capable GPU (recommended for RAG)
- GNS3 server running
- Network devices accessible via Telnet

#### Quick Start
```bash
# Clone and setup
git clone <repository>
cd GNS3/tools

# Install dependencies
pip install -r requirements.txt

# Initialize RAG system
python setup_rag.py --all

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Run the agent
python main.py
```

#### Configuration
1. **Environment Variables**: Set GNS3 server URL, Telnet host, API keys
2. **RAG Configuration**: Customize embedding model, vector store settings
3. **Knowledge Base**: Add network documentation to `knowledge_base/` directory

### 💻 Usage Examples

```bash
# Start interactive session
python main.py

# Example queries (English)
> "show OSPF neighbor status"
> "analyze R1 to R6 routing configuration"
> "list all device interfaces"

# Example queries (Chinese - auto-detected)
> "查看OSPF邻居状态"
> "分析R1到R6的路由配置"
> "列出所有设备接口"
```

### 🔗 Integration

- **GNS3 API**: Full integration with GNS3 REST API
- **Network Devices**: Telnet-based device configuration retrieval
- **External LLMs**: Support for various LLM providers
- **Knowledge Sources**: Flexible document ingestion pipeline

---

## 🌟 中文概述

### 项目描述

**GNS3智能代理 v6.0** 是一个基于人工智能技术的高级网络设备管理系统。该智能代理结合了大语言模型(LLM)、检索增强生成(RAG)和多语言支持，为GNS3网络环境管理和分析提供全面的解决方案。

### 🎯 核心特性

#### 🧠 AI驱动的智能化
- **LLM集成**: 支持多种模型（DeepSeek、Ollama、OpenAI兼容API）
- **RAG增强**: 使用BGE-M3嵌入和FAISS搜索的向量知识库
- **智能命令选择**: 基于上下文的网络命令推荐
- **自然语言处理**: 理解复杂的网络管理查询

#### 🌍 多语言支持
- **英文优先策略**: 默认英文界面，无缝中文切换
- **智能语言检测**: 基于用户输入的自动语言识别
- **双语模板**: 专业的双语提示和响应
- **技术术语一致性**: 网络术语保持英文以确保准确性

#### 📚 高级知识管理
- **RAG知识库**: 向量化的网络排错文档
- **多知识源**: RAG、基础命令库、关键词搜索
- **文档处理**: 支持PDF、TXT、MD、DOCX格式
- **GPU加速嵌入**: 使用FAISS的高性能向量搜索

#### 🛠️ 全面的网络管理
- **设备配置获取**: 支持大文件的批量配置收集
- **拓扑分析**: 网络结构可视化和分析
- **接口连接映射**: 设备互联发现
- **项目信息管理**: GNS3项目状态监控

#### 🔧 企业级特性
- **模块化架构**: 清晰的关注点分离和可扩展设计
- **错误处理**: 健壮的错误恢复和用户友好的反馈
- **配置管理**: 通过INI文件的灵活系统配置
- **性能优化**: 针对大型网络环境优化

### 🏗️ 系统架构

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    用户输入     │ -> │    语言适配器    │ -> │    意图分析     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │
          v                       v                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│    命令选择     │ <- │   RAG知识库     │ <- │   LLM处理      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
          │                       │                       │
          v                       v                       v
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   GNS3执行     │    │    向量搜索     │    │   响应格式化    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 📦 安装配置

#### 环境要求
- Python 3.8+
- 支持CUDA的GPU（推荐用于RAG）
- 运行中的GNS3服务器
- 通过Telnet可访问的网络设备

#### 快速开始
```bash
# 克隆和设置
git clone <repository>
cd GNS3/tools

# 安装依赖
pip install -r requirements.txt

# 初始化RAG系统
python setup_rag.py --all

# 配置环境
cp .env.example .env
# 编辑.env文件设置您的配置

# 运行代理
python main.py
```

#### 配置说明
1. **环境变量**: 设置GNS3服务器URL、Telnet主机、API密钥
2. **RAG配置**: 自定义嵌入模型、向量存储设置
3. **知识库**: 将网络文档添加到 `knowledge_base/` 目录

### 💻 使用示例

```bash
# 启动交互式会话
python main.py

# 英文查询示例
> "show OSPF neighbor status"
> "analyze R1 to R6 routing configuration"
> "list all device interfaces"

# 中文查询示例（自动检测）
> "查看OSPF邻居状态"
> "分析R1到R6的路由配置"
> "列出所有设备接口"
```

### 🔗 系统集成

- **GNS3 API**: 与GNS3 REST API完全集成
- **网络设备**: 基于Telnet的设备配置获取
- **外部LLM**: 支持各种LLM提供商
- **知识源**: 灵活的文档摄取流水线

---

## 📁 Project Structure / 项目结构

```
GNS3/tools/
├── 📄 main.py                    # Main application entry / 主应用程序入口
├── 📄 requirements.txt           # Dependencies / 依赖项
├── 📄 setup_rag.py              # RAG setup script / RAG设置脚本
├── 📄 rag_config.ini            # RAG configuration / RAG配置
├── 📄 .env                      # Environment variables / 环境变量
├── 📂 core/                     # Core modules / 核心模块
│   ├── 🧠 intelligent_processor.py     # AI request processor / AI请求处理器
│   ├── 🌍 language_adapter.py          # Multi-language support / 多语言支持
│   ├── 📚 network_rag_kb.py           # RAG knowledge base / RAG知识库
│   ├── 🔧 rag_enhanced_executor.py    # RAG command executor / RAG命令执行器
│   ├── 🤖 llm_manager.py              # LLM model manager / LLM模型管理器
│   ├── 🛠️ gns3_agent_tools.py         # GNS3 integration / GNS3集成
│   └── 📊 get_*.py                    # Data collection modules / 数据收集模块
├── 📂 knowledge_base/           # RAG documents / RAG文档
├── 📂 vector_store/            # FAISS vector database / FAISS向量数据库
├── 📂 device_configs/          # Collected configurations / 收集的配置
└── 📂 analysis_reports/        # AI analysis reports / AI分析报告
```

## 🚀 Technology Stack / 技术栈

### AI & ML Technologies
- **🧠 LangChain**: LLM orchestration framework
- **🤖 Multiple LLM Support**: DeepSeek, Ollama, OpenAI
- **📚 BGE-M3**: Multilingual embedding model
- **🔍 FAISS**: High-performance vector search
- **🌍 Sentence Transformers**: Text embedding pipeline

### Network & Integration
- **🌐 GNS3**: Network simulation platform
- **🔌 Telnet**: Device configuration access
- **📡 REST API**: GNS3 server integration
- **🐍 Python**: Core development language

### Development & Deployment
- **🏗️ Modular Architecture**: Clean, maintainable codebase
- **⚙️ Configuration Management**: INI-based settings
- **🛡️ Error Handling**: Robust exception management
- **📊 Logging**: Comprehensive activity tracking

---

## 📈 Performance & Scalability / 性能与扩展性

### Performance Metrics / 性能指标
- **Language Detection**: <1ms response time / 语言检测：<1毫秒响应时间
- **RAG Search**: GPU-accelerated with BGE-M3 / RAG搜索：BGE-M3 GPU加速
- **Configuration Handling**: Up to 10MB+ files / 配置处理：支持10MB+文件
- **Concurrent Operations**: Multi-device batch processing / 并发操作：多设备批处理

### Scalability Features / 扩展特性
- **Horizontal Scaling**: Multiple GNS3 server support / 水平扩展：多GNS3服务器支持
- **Knowledge Base Growth**: Dynamic document addition / 知识库增长：动态文档添加
- **Model Flexibility**: Easy LLM model switching / 模型灵活性：轻松切换LLM模型
- **Custom Extensions**: Plugin-ready architecture / 自定义扩展：支持插件的架构

---

## 🤝 Contributing / 贡献

We welcome contributions! Please see our contribution guidelines.

欢迎贡献！请查看我们的贡献指南。

## 📄 License / 许可证

This project is licensed under the MIT License.

本项目基于MIT许可证开源。

---

## 📞 Support / 支持

For technical support and questions, please create an issue in our repository.

如需技术支持和问题咨询，请在我们的仓库中创建issue。
