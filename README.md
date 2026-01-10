# GNS3 Copilot

[![CI - QA & Testing](https://github.com/yueguobin/gns3-copilot/actions/workflows/ci.yaml/badge.svg)](https://github.com/yueguobin/gns3-copilot/actions/workflows/ci.yaml)
[![CD - Production Release](https://github.com/yueguobin/gns3-copilot/actions/workflows/cd.yaml/badge.svg)](https://github.com/yueguobin/gns3-copilot/actions/workflows/cd.yaml)
[![codecov](https://codecov.io/gh/yueguobin/gns3-copilot/branch/Development/graph/badge.svg?token=7FDUCM547W)](https://codecov.io/gh/yueguobin/gns3-copilot)
[![PyPI version](https://img.shields.io/pypi/v/gns3-copilot)](https://pypi.org/project/gns3-copilot/)
[![PyPI downloads](https://img.shields.io/pypi/dm/gns3-copilot)](https://pypi.org/project/gns3-copilot/)
![License](https://img.shields.io/badge/license-MIT-green.svg) 
[![platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macOS-lightgrey)](https://shields.io/)

---

<div align="center">

[🇺🇸 English](README.md) | [🇨🇳 中文](README_ZH.md)

</div>

---

An AI-powered network automation assistant designed specifically for GNS3 network simulator, providing intelligent network device management and automated operations.

## Project Overview

GNS3 Copilot is a powerful network automation tool that integrates multiple AI models and network automation frameworks. It can interact with users through natural language and perform tasks such as network device configuration, topology management, and fault diagnosis.

<img src="https://raw.githubusercontent.com/yueguobin/gns3-copilot/refs/heads/master/demo.gif" alt="GNS3 Copilot Function demonstration" width="1280"/>

## Installation Guide

### Environment Requirements

- Python 3.10+
- GNS3 Server (running on http://localhost:3080 or remote host)
- Supported operating systems: Windows, macOS, Linux

### Installation Steps

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows
```

2. **Install GNS3 Copilot**
```bash
pip install gns3-copilot
```
or
```bash
pip install git+https://github.com/yueguobin/gns3-copilot
```

3. **Start GNS3 Server**
Ensure GNS3 Server is running and can be accessed via its API interface: `http://x.x.x.x:3080`

4. **Launch the application**
```bash
gns3-copilot
```

## Usage Guide

### Configure on Settings Page

GNS3 Copilot configuration is managed through a Streamlit interface, with all settings saved in the `.env` file in the project root directory. If the `.env` file doesn't exist on first run, the system will automatically create it.

#### 🔧 Main Configuration Content

##### 1. GNS3 Server Configuration
- **GNS3 Server Host**: GNS3 server host address (e.g., 127.0.0.1)
- **GNS3 Server URL**: Complete GNS3 server URL (e.g., http://127.0.0.1:3080)
- **API Version**: GNS3 API version (supports v2 and v3)
- **GNS3 Server Username**: GNS3 server username (required only for API v3)
- **GNS3 Server Password**: GNS3 server password (required only for API v3)

##### 2. LLM Model Configuration

**🌟 Recommended Models:**
- **Best:** `deepseek-chat` (via DeepSeek API) or `deepseek/deepseek-v3.2` (via OpenRouter)
- **Other Recommended:** `x-ai/grok-3`, `anthropic/claude-sonnet-4`, `z-ai/glm-4.7`

**Note:** These models have been tested and verified to provide excellent performance for network automation tasks.

- **Model Provider**: Model provider (supports: openai, anthropic, deepseek, xai, openrouter, etc.)
- **Model Name**: Specific model name (e.g., deepseek-chat, gpt-4o-mini, etc.)
- **Model API Key**: Model API key
- **Base URL**: Base URL for model service (required when using third-party platforms like OpenRouter)
- **Temperature**: Model temperature parameter (controls output randomness, range 0.0-1.0)

##### 3. Other Settings
- **Linux Console Username**: Linux console username (for Debian devices in GNS3)
- **Linux Console Password**: Linux console password

## Documentation

See [docs/](docs/) directory for detailed documentation including user guides, development guides, and technical documentation.

## 🤝 Contributing

We welcome contributions from the community! To keep the project stable, please follow our branching strategy:

- **Target Branch**: Always submit your Pull Requests to the `Development` branch (not `master`).

- **Feature Branches**: Create a new branch for each feature or bug fix: `git checkout -b feature/your-feature-name Development`.

- **Workflow**: Fork -> Branch -> Commit -> Push -> Pull Request to `Development`.

## 🧠 Practical Insights

From our extensive testing with gns3-copilot, here are some hard-earned lessons on how to effectively use AI as your network co-pilot:

- **The Power of "Why", Not Just "How"**: Don't just ask for the config. Ask the AI to build a Diagnostic Tree. It's a 24/7 mentor that never gets tired of your "Active" BGP status.

- **Mind the Gap (Vendor Specifics)**: While LLMs excel at standard RFC protocols (OSPF, BGP), they might hallucinate when it comes to Proprietary Protocols or bleeding-edge features. Always verify vendor-specific syntax.

- **Modular Approach for Complex Topologies**: For networks with 20+ nodes, break down your requests. AI works best when focusing on specific segments rather than trying to memorize the entire routing table at once.

- **Simulation != Reality**: GNS3 is a perfect sandbox, but it doesn't simulate faulty transceivers or hardware bugs. Use the Copilot to master logic, but keep your hands on the "real world" troubleshooting tools.

## Security Considerations

1. **API Key Protection**:
   - Do not commit `.env` file to version control
   - Regularly rotate API keys
   - Use principle of least privilege

## License

This project uses MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgements

This project was inspired by the following resources, which provided the foundation for Python programming, network automation, and AI applications:

- **《网络工程师的 Python 之路》** - Network engineering automation with Python
- **《网络工程师的 AI 之路》** - AI applications for network engineering

Special thanks to these resources for their technical inspiration and guidance.

## Contact

- Project Homepage: https://github.com/yueguobin/gns3-copilot
- Issue Reporting: https://github.com/yueguobin/gns3-copilot/issues

---
