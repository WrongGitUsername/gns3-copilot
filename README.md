# 🌟 GNS3 ## 📚 Documentation

**📂 All documentation has been organized in the [`docs/`](./docs/) directory!**

| Document | Description |
|----------|-------------|
| **[📚 docs/README.md](docs/README.md)** | **📖 Documentation Center** - Start here! |
| **[🚀 docs/getting-started/QUICK_DEPLOY.md](docs/getting-started/QUICK_DEPLOY.md)** | 5-minute deployment guide |
| **[🌐 docs/getting-started/README_ZH.md](docs/getting-started/README_ZH.md)** | 中文文档 |
| **[🌍 docs/getting-started/README_EN.md](docs/getting-started/README_EN.md)** | English Documentation |
| **[📖 docs/development/PROJECT_OVERVIEW.md](docs/development/PROJECT_OVERVIEW.md)** | Complete project introduction |
| **[🔧 docs/development/TECHNICAL_SPECS.md](docs/development/TECHNICAL_SPECS.md)** | Technical specifications |
| **[⚡ docs/features/README_RAG.md](docs/features/README_RAG.md)** | RAG functionality guide |
| **[📊 docs/updates/COMMANDS_EXPANSION_REPORT.md](docs/updates/COMMANDS_EXPANSION_REPORT.md)** | Latest command expansion report |gent

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green.svg)](https://langchain.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **English** | [中文文档](README_ZH.md)

An AI-powered network device management system for GNS3 environments, featuring Large Language Models (LLM), Retrieval-Augmented Generation (RAG), and intelligent multi-language support.

## 📚 Documentation

**📂 All documentation has been moved to the [`docs/`](./docs/) directory!**

| Document | Description |
|----------|-------------|
| **[� docs/README.md](docs/README.md)** | **📖 Documentation Center** - Start here! |
| **[�🚀 docs/QUICK_DEPLOY.md](docs/QUICK_DEPLOY.md)** | 5-minute deployment guide |
| **[📖 docs/PROJECT_OVERVIEW.md](docs/PROJECT_OVERVIEW.md)** | Complete project introduction |
| **[🔧 docs/TECHNICAL_SPECS.md](docs/TECHNICAL_SPECS.md)** | Technical specifications |
| **[📊 docs/COMMANDS_EXPANSION_REPORT.md](docs/COMMANDS_EXPANSION_REPORT.md)** | Latest command expansion report |
| **[🌐 docs/README_ZH.md](docs/README_ZH.md)** | 中文文档 |
| **[🌍 docs/README_EN.md](docs/README_EN.md)** | English Documentation |

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🧠 **AI-Powered** | LLM integration with DeepSeek, Ollama, OpenAI |
| 📚 **RAG Enhanced** | Vector knowledge base with BGE-M3 + FAISS |
| 🌍 **Multi-Language** | Perfect dual-language support with auto-detection |
| 🔍 **Smart Connectivity** | Intelligent device IP discovery & connectivity analysis |
| 🛠️ **Network Management** | Complete GNS3 device configuration & analysis |
| 🎯 **Command Validation** | Advanced command verification & execution safety |
| ⚡ **High Performance** | GPU acceleration & concurrent processing |

## 🎬 Demo Video

<div align="center">

[![GNS3 Copilot Demo](https://img.youtube.com/vi/YNi7KF_a_k0/maxresdefault.jpg)](https://youtu.be/YNi7KF_a_k0)

**🎥 [▶️ CLICK TO WATCH DEMO VIDEO](https://youtu.be/YNi7KF_a_k0) 🎥**

*Note: Video opens in YouTube (GitHub doesn't support embedded video playback)*

</div>

**🎥 Watch the live demo** to see GNS3 Copilot in action! This video showcases:
- Real-time network device management
- AI-powered command analysis  
- Smart connectivity testing
- Bilingual interface demonstration

## 🚀 Quick Start

```bash
# 1. Clone repository
git clone <your-repo-url>
cd gns3-copilot

# 2. Setup environment
pip install -r requirements.txt
python setup_rag.py --all

# 3. Configure
cp .env.example .env
# Edit .env with your settings

# 4. Run
python main.py
```

## 💬 Usage Examples

### Smart Connectivity Analysis
```
🙋 You: ping from R1 to R2
🤖 Assistant: Analyzing connectivity request...
✅ Found project: network_ai
🔍 Discovering device IPs from configurations...
   R1: 192.168.1.1 | R2: 192.168.1.2
🔧 Executing: ping 192.168.1.2 source 192.168.1.1
📊 Analysis: Connectivity test successful
```

### Network Commands
```
🙋 You: show OSPF neighbor status on R3
🤖 Assistant: Analyzing request...
✅ Found device: R3 (Console: 5004)
🔧 Executing: show ip ospf neighbor
📋 OSPF neighbors found and analyzed
```

### Multi-Device Operations
```
🙋 You: collect configuration from all devices
🤖 Assistant: Starting batch collection...
✅ Devices: R1(5000), R2(5002), R3(5004), R4(5006), R5(5008), R6(5010)
🔧 Executing: show running-config
📁 Configurations saved to device_configs/
```

## 📁 Project Structure

```
📦 gns3-copilot/
├── 🎯 main.py                          # Main application
├── ⚙️ setup_rag.py                     # RAG setup
├── 📋 requirements.txt                  # Dependencies
├── 📂 core/                            # Core modules
│   ├── 🧠 intelligent_processor.py     # AI request analysis
│   ├── 🌍 language_adapter.py          # Dual-language support
│   ├── 📚 network_rag_kb.py            # RAG knowledge base
│   ├── 🔧 rag_enhanced_executor.py     # Enhanced command execution
│   ├── 🎯 intelligent_command_executor.py # Smart command processing
│   ├── ⚡ concurrent_command_executor.py  # Batch processing
│   └── 🔍 get_all_devices_config.py    # Device discovery
├── 📚 knowledge_base/                  # RAG documents
├── 🗄️ vector_store/                   # Vector database
├── 📊 analysis_reports/                # Analysis output
├── 🗂️ device_configs/                 # Device configurations
├── 📚 docs/                           # 📖 **Documentation Center**
│   ├── README.md                      # Documentation index
│   ├── QUICK_DEPLOY.md               # Quick deployment
│   ├── PROJECT_OVERVIEW.md           # Project overview
│   ├── TECHNICAL_SPECS.md            # Technical specs
│   ├── COMMANDS_EXPANSION_REPORT.md  # Latest updates
│   └── ...                           # More documentation
└── 🧪 tests/                          # Test files
    ├── test_connectivity_analysis.py   # Connectivity testing
    ├── test_english_connectivity.py    # English mode testing
    └── test_enhanced_executor.py       # Enhanced features testing
```

> 📝 **For detailed documentation, visit the [`docs/`](./docs/) directory!**

## 🏗️ Architecture

```mermaid
graph TD
    A[User Input] --> B[Language Detector]
    B --> C[Intelligent Processor]
    C --> D[Command Validator]
    D --> E[Device Discovery]
    E --> F[RAG Knowledge Base]
    F --> G[Enhanced Executor]
    G --> H[GNS3 Integration]
    H --> I[Connectivity Analysis]
    I --> J[Multi-language Output]
    
    subgraph "Core Features"
        K[IP Discovery]
        L[Batch Processing]
        M[Config Analysis]
        N[Smart Validation]
    end
    
    G --> K
    G --> L
    G --> M
    G --> N
```

## 🔧 Configuration

### Environment Variables
```bash
# GNS3 Settings
GNS3_SERVER_URL=http://192.168.101.1:3080
TELNET_HOST=192.168.102.1

# LLM Settings
DEEPSEEK_API_KEY=your_deepseek_key
OLLAMA_BASE_URL=http://localhost:11434

# RAG Settings
USE_RAG=true
VECTOR_STORE_PATH=./vector_store
```

### RAG Configuration
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

## 📚 Knowledge Base

Support for multiple document formats:

- **📄 PDF**: Network troubleshooting guides
- **📝 TXT**: Command references
- **📓 MD**: Technical documentation
- **📋 DOCX**: Configuration examples

Simply add documents to `knowledge_base/` directory and restart the system.

## 🎯 Use Cases

### Network Operations
- Device configuration analysis
- Troubleshooting assistance
- Topology discovery
- Batch configuration collection

### Education & Training
- Interactive network learning
- Command suggestion
- Configuration explanation
- Best practices guidance

### Development & Testing
- Network automation scripting
- Configuration validation
- Performance analysis
- Integration testing

## 🛡️ Security & Performance

### Security Features
- **🔐 API Key Protection**: Secure credential management
- **🛡️ Input Validation**: Sanitized user inputs
- **🚫 Access Control**: Role-based permissions
- **📋 Audit Logging**: Complete operation tracking

### Performance Optimization
- **⚡ GPU Acceleration**: CUDA-optimized embeddings
- **🗄️ Vector Caching**: Fast similarity search
- **📈 Batch Processing**: Efficient multi-device operations
- **💾 Memory Management**: Optimized for large configurations

## 📖 Documentation

- **[📋 Complete Project Overview](PROJECT_OVERVIEW.md)** - Detailed feature documentation
- **[🌍 Multi-Language Guide](README_LANGUAGE.md)** - Language system documentation
- **[🧠 RAG System Guide](README_RAG.md)** - RAG configuration and usage
- **[💻 Core Modules](core/README.md)** - Technical module documentation

## 🤝 Contributing

We welcome contributions from the community!

1. **Fork** the repository
2. **Create** a feature branch
3. **Commit** your changes
4. **Push** to the branch
5. **Create** a Pull Request

## 📞 Support

- **🐛 Issues**: [GitHub Issues](../../issues) - Bug reports and feature requests
- **💬 Discussions**: [GitHub Discussions](../../discussions) - Community support
- **📧 Contact**: Technical support

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**🌟 Star this repository if you find it helpful! 🌟**

Made with ❤️ by the GNS3 Community

</div>
