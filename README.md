# GNS3 Copilot

[![CI - QA & Testing](https://github.com/yueguobin/gns3-copilot/actions/workflows/ci.yaml/badge.svg)](https://github.com/yueguobin/gns3-copilot/actions/workflows/ci.yaml)
[![CD - Production Release](https://github.com/yueguobin/gns3-copilot/actions/workflows/cd.yaml/badge.svg)](https://github.com/yueguobin/gns3-copilot/actions/workflows/cd.yaml)
[![codecov](https://codecov.io/gh/yueguobin/gns3-copilot/branch/Development/graph/badge.svg?token=7FDUCM547W)](https://codecov.io/gh/yueguobin/gns3-copilot)
[![PyPI version](https://img.shields.io/pypi/v/gns3-copilot)](https://pypi.org/project/gns3-copilot/)
[![PyPI downloads](https://img.shields.io/pypi/dm/gns3-copilot)](https://pypi.org/project/gns3-copilot/)
![License](https://img.shields.io/badge/license-MIT-green.svg) 
[![platform](https://img.shields.io/badge/platform-linux%20%7C%20windows%20%7C%20macOS-lightgrey)](https://shields.io/)


<div align="center">

[🇺🇸 English](README.md) | [🇨🇳 中文](README_ZH.md)

</div>


An AI-powered network automation assistant designed specifically for GNS3 network simulator, providing intelligent network device management and automated operations.

## Project Overview

GNS3 Copilot is a powerful network automation tool that integrates multiple AI models and network automation frameworks. It can interact with users through natural language and perform tasks such as network device configuration, topology management, and fault diagnosis.

<img src="https://raw.githubusercontent.com/yueguobin/gns3-copilot/refs/heads/Development/docs/media/demo.gif" alt="GNS3 Copilot Function demonstration" width="1280"/>

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

GNS3 Copilot configuration is managed through a Streamlit interface, with all settings persisted in a SQLite database for reliable data storage.

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

##### 3. Calibre & Reading Settings
- **Calibre Server URL**: URL for Calibre Content Server (e.g., http://localhost:8080)
  - Start Calibre Content Server via Calibre GUI: Preferences → Sharing over the net → Start Server
  - Or start from command line: `calibre-server --port 8080`

##### 4. Other Settings
- **Linux Console Username**: Linux console username (for Debian devices in GNS3)
- **Linux Console Password**: Linux console password

## 📚 Reading & Notes

GNS3 Copilot includes a dedicated reading interface integrated with Calibre Content Server:

- **Calibre Ebook Viewer**: Embedded iframe viewer to access and read ebooks from your Calibre library
- **Multi-Note Management**: Create, select, and delete reading notes for organizing your thoughts
- **Markdown Notes**: All notes are saved as Markdown files with download functionality
- **🤖 AI-Powered Note Organization**: Use AI to automatically refine and organize your notes
  - Click the "AI Organize" button to let the AI format and structure your notes
  - Compare original vs organized content side-by-side before accepting
  - Reorganize as needed until satisfied with the result

To access the reading interface:
1. Configure Calibre Server URL in Settings
2. Start Calibre Content Server (port 8080 by default)
3. Navigate to the Reading page in the application


<img src="https://raw.githubusercontent.com/yueguobin/gns3-copilot/refs/heads/Development/docs/media/reading_and_notes.gif" alt="GNS3 Copilot Function demonstration" width="1280"/>

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
   - API keys are stored in SQLite database (currently in plaintext)
   - Regularly rotate API keys
   - Use principle of least privilege
   - Do not commit the database file to version control

2. **Database Security**:
   - **Important**: The database currently stores passwords and API keys in plaintext
   - The configuration database is stored locally on your machine
   - Ensure proper file permissions are set on the database directory
   - Backup the database regularly to prevent data loss
   - Restrict access to the database file to authorized users only

3. **Environment Security**:
   - Run GNS3 Copilot in a trusted environment
   - Consider using encrypted filesystems for storing sensitive data
   - Be cautious when sharing database backups

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
