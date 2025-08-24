# 🌟 GNS3 Intelligent Agent / GNS3 智能代理

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **English** | [中文文档](PROJECT_OVERVIEW.md#中文概述)

An AI-powered network device management system for GNS3 environments, featuring Large Language Models (LLM), Retrieval-Augmented Generation (RAG), and intelligent multi-language support.

一个基于AI的GNS3网络设备管理系统，集成大语言模型(LLM)、检索增强生成(RAG)和智能多语言支持。

## 📚 Documentation / 文档导航

| Document | Description | 文档说明 |
|----------|-------------|----------|
| **[🚀 QUICK_DEPLOY.md](QUICK_DEPLOY.md)** | 5-minute deployment guide | 5分钟快速部署指南 |
| **[📖 PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)** | Complete project introduction | 完整项目介绍 |
| **[🔧 TECHNICAL_SPECS.md](TECHNICAL_SPECS.md)** | Technical specifications | 技术规格文档 |
| **[🆕 ENHANCEMENTS_LOG.md](ENHANCEMENTS_LOG.md)** | Latest feature enhancements | 最新功能增强记录 |
| **[🧪 tests/README.md](tests/README.md)** | Testing documentation | 测试文档说明 |
| **[📝 README.md](README.md)** | This file - Quick reference | 本文件 - 快速参考 |

## ✨ Quick Features / 核心特性

| Feature | Description | 特性描述 |
|---------|-------------|----------|
| 🧠 **AI-Powered** | LLM integration with DeepSeek, Ollama, OpenAI | LLM集成：DeepSeek、Ollama、OpenAI |
| 📚 **RAG Enhanced** | Vector knowledge base with BGE-M3 + FAISS | RAG增强：BGE-M3嵌入 + FAISS搜索 |
| 🌍 **Multi-Language** | Perfect dual-language support with auto-detection | 完美双语支持与自动检测 |
| 🔍 **Smart Connectivity** | Intelligent device IP discovery & connectivity analysis | 智能设备IP发现与连通性分析 |
| 🛠️ **Network Management** | Complete GNS3 device configuration & analysis | 完整的GNS3设备配置和分析 |
| 🎯 **Command Validation** | Advanced command verification & execution safety | 高级命令验证与执行安全 |
| ⚡ **High Performance** | GPU acceleration & concurrent processing | GPU加速和并发处理 |

## 🚀 Quick Start / 快速开始

```bash
# 1. Clone repository / 克隆仓库
git clone <your-repo-url>
cd GNS3/tools

# 2. Setup environment / 设置环境
pip install -r requirements.txt
python setup_rag.py --all

# 3. Configure / 配置
cp .env.example .env
# Edit .env with your settings / 编辑.env设置

# 4. Run / 运行
python main.py
```

## 💬 Usage Examples / 使用示例

### Smart Connectivity Analysis / 智能连通性分析
```
🙋 You: ping from R1 to R2
🤖 Assistant: Analyzing connectivity request...
✅ Found project: network_ai
🔍 Discovering device IPs from configurations...
   R1: 192.168.1.1 | R2: 192.168.1.2
🔧 Executing: ping 192.168.1.2 source 192.168.1.1
📊 Analysis: Connectivity test successful
```

### English Network Commands / 英文网络命令
```
🙋 You: show OSPF neighbor status on R3
🤖 Assistant: Analyzing request...
✅ Found device: R3 (Console: 5004)
🔧 Executing: show ip ospf neighbor
📋 OSPF neighbors found and analyzed
```

### Chinese Queries / 中文查询
```
🙋 您: 检查所有路由器的路由表
🤖 助手: 正在分析请求...
✅ 找到 6 台设备: R1-R6
🔧 批量执行: show ip route
📊 路由表分析完成
```

### Multi-Device Operations / 多设备操作
```
🙋 You: collect configuration from all devices
🤖 Assistant: Starting batch collection...
✅ Devices: R1(5000), R2(5002), R3(5004), R4(5006), R5(5008), R6(5010)
🔧 Executing: show running-config
📁 Configurations saved to device_configs/
```

## 📁 Project Structure / 项目结构

```
📦 GNS3/gns3-copilot/
├── 🎯 main.py                          # Main application / 主程序
├── ⚙️ setup_rag.py                     # RAG setup / RAG设置
├── 📋 requirements.txt                  # Dependencies / 依赖
├── 📂 core/                            # Core modules / 核心模块
│   ├── 🧠 intelligent_processor.py     # AI request analysis / AI请求分析
│   ├── 🌍 language_adapter.py          # Dual-language support / 双语支持
│   ├── 📚 network_rag_kb.py            # RAG knowledge base / RAG知识库
│   ├── 🔧 rag_enhanced_executor.py     # Enhanced command execution / 增强命令执行
│   ├── 🎯 intelligent_command_executor.py # Smart command processing / 智能命令处理
│   ├── ⚡ concurrent_command_executor.py  # Batch processing / 批量处理
│   └── � get_all_devices_config.py    # Device discovery / 设备发现
├── �📚 knowledge_base/                  # RAG documents / RAG文档
├── 🗄️ vector_store/                   # Vector database / 向量数据库
├── 📊 analysis_reports/                # Analysis output / 分析输出
├── 🗂️ device_configs/                 # Device configurations / 设备配置
└── 🧪 tests/                          # Test files / 测试文件
    ├── test_connectivity_analysis.py   # Connectivity testing / 连通性测试
    ├── test_english_connectivity.py    # English mode testing / 英文模式测试
    └── test_enhanced_executor.py       # Enhanced features testing / 增强功能测试
```

## 🏗️ Architecture / 系统架构

```mermaid
graph TD
    A[User Input / 用户输入] --> B[Language Detector / 语言检测器]
    B --> C[Intelligent Processor / 智能处理器]
    C --> D[Command Validator / 命令验证器]
    D --> E[Device Discovery / 设备发现]
    E --> F[RAG Knowledge Base / RAG知识库]
    F --> G[Enhanced Executor / 增强执行器]
    G --> H[GNS3 Integration / GNS3集成]
    H --> I[Connectivity Analysis / 连通性分析]
    I --> J[Multi-language Output / 多语言输出]
    
    subgraph "Core Features / 核心功能"
        K[IP Discovery / IP发现]
        L[Batch Processing / 批量处理]
        M[Config Analysis / 配置分析]
        N[Smart Validation / 智能验证]
    end
    
    G --> K
    G --> L
    G --> M
    G --> N
```

## 🔧 Configuration / 配置

### Environment Variables / 环境变量
```bash
# GNS3 Settings / GNS3设置
GNS3_SERVER_URL=http://192.168.101.1:3080
TELNET_HOST=192.168.102.1

# LLM Settings / LLM设置
DEEPSEEK_API_KEY=your_deepseek_key
OLLAMA_BASE_URL=http://localhost:11434

# RAG Settings / RAG设置
USE_RAG=true
VECTOR_STORE_PATH=./vector_store
```

### RAG Configuration / RAG配置
```ini
[embeddings]
model_name = BAAI/bge-m3
device = cuda
max_length = 8192

[vector_store]
chunk_size = 1000
chunk_overlap = 200
search_k = 5
```

## 📚 Knowledge Base / 知识库

Support for multiple document formats / 支持多种文档格式:

- **📄 PDF**: Network troubleshooting guides / 网络排错指南
- **📝 TXT**: Command references / 命令参考
- **📓 MD**: Technical documentation / 技术文档
- **📋 DOCX**: Configuration examples / 配置示例

Simply add documents to `knowledge_base/` directory and restart the system.

只需将文档添加到 `knowledge_base/` 目录并重启系统。

## 🎯 Use Cases / 使用场景

### Network Operations / 网络运维
- Device configuration analysis / 设备配置分析
- Troubleshooting assistance / 故障排除协助
- Topology discovery / 拓扑发现
- Batch configuration collection / 批量配置收集

### Education & Training / 教育培训
- Interactive network learning / 交互式网络学习
- Command suggestion / 命令建议
- Configuration explanation / 配置解释
- Best practices guidance / 最佳实践指导

### Development & Testing / 开发测试
- Network automation scripting / 网络自动化脚本
- Configuration validation / 配置验证
- Performance analysis / 性能分析
- Integration testing / 集成测试

## 🛡️ Security & Performance / 安全与性能

### Security Features / 安全特性
- **🔐 API Key Protection**: Secure credential management / 安全凭证管理
- **🛡️ Input Validation**: Sanitized user inputs / 用户输入验证
- **🚫 Access Control**: Role-based permissions / 基于角色的权限
- **📋 Audit Logging**: Complete operation tracking / 完整操作跟踪

### Performance Optimization / 性能优化
- **⚡ GPU Acceleration**: CUDA-optimized embeddings / CUDA优化嵌入
- **🗄️ Vector Caching**: Fast similarity search / 快速相似度搜索
- **📈 Batch Processing**: Efficient multi-device operations / 高效多设备操作
- **💾 Memory Management**: Optimized for large configurations / 大配置优化

## 📖 Documentation / 文档

- **[📋 Complete Project Overview](PROJECT_OVERVIEW.md)** - Detailed feature documentation / 详细功能文档
- **[🌍 Multi-Language Guide](README_LANGUAGE.md)** - Language system documentation / 语言系统文档
- **[🧠 RAG System Guide](README_RAG.md)** - RAG configuration and usage / RAG配置和使用
- **[💻 Core Modules](core/README.md)** - Technical module documentation / 技术模块文档

## 🤝 Contributing / 贡献

We welcome contributions from the community! / 欢迎社区贡献！

1. **Fork** the repository / Fork仓库
2. **Create** a feature branch / 创建功能分支
3. **Commit** your changes / 提交更改
4. **Push** to the branch / 推送到分支
5. **Create** a Pull Request / 创建Pull Request

## 📞 Support / 技术支持

- **🐛 Issues**: [GitHub Issues](../../issues) - Bug reports and feature requests / 错误报告和功能请求
- **💬 Discussions**: [GitHub Discussions](../../discussions) - Community support / 社区支持
- **📧 Contact**: Technical support / 技术支持

## 📄 License / 许可证

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

本项目基于 **MIT许可证** 开源 - 详见 [LICENSE](LICENSE) 文件。

---

<div align="center">

**🌟 Star this repository if you find it helpful! / 如果这个项目对您有帮助，请给个Star！🌟**

Made with ❤️ by the GNS3 Community / 由GNS3社区用❤️制作

</div>
