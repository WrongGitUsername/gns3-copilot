# Contributing to GNS3 Copilot

Thank you for your interest in contributing to GNS3 Copilot! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

1. **Search Existing Issues**: Before creating a new issue, search the existing issues to avoid duplicates.
2. **Use Issue Templates**: Use the appropriate issue template when reporting bugs or requesting features.
3. **Provide Detailed Information**:
   - Include steps to reproduce
   - Provide error messages and logs
   - Include your environment details (OS, Python version, GNS3 version)
   - Add screenshots if applicable

### Feature Requests

1. **Describe the Use Case**: Explain what problem the feature solves.
2. **Provide Implementation Ideas**: If you have ideas on how to implement it, please share.
3. **Consider Compatibility**: Think about how the feature affects existing functionality.

### Code Contributions

#### Prerequisites

- Python 3.8 or higher
- Git
- Familiarity with network automation concepts
- Understanding of GNS3, LangChain, and Chainlit (helpful but not required)

#### Development Setup

1. **Fork the Repository**:
   ```bash
   # Fork on GitHub, then clone your fork
   git clone https://github.com/your-username/gns3-copilot.git
   cd gns3-copilot
   ```

2. **Create a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   # Install development dependencies
   pip install pylint pytest black mypy
   ```

4. **Create a Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

#### Code Style Guidelines

We use the following tools for code quality:

- **Black**: Code formatting
- **Pylint**: Code linting
- **MyPy**: Type checking

```bash
# Format code
black .

# Lint code
pylint **/*.py

# Type check
mypy **/*.py
```

#### Code Structure

```
gns3-copilot/
├── tools/                  # Core tool implementations
├── process_analyzer/       # Process analysis module
├── prompts/               # AI prompt templates
├── docs/                  # Documentation
└── tests/                 # Test files (to be added)
```

#### Adding New Tools

1. **Create Tool File**: Add new tool in `tools/` directory
2. **Inherit from BaseTool**: Use LangChain's BaseTool class
3. **Add Logging**: Use the centralized logging configuration
4. **Update Documentation**: Add tool to API reference
5. **Add Tests**: Create comprehensive tests

Example tool structure:

```python
"""
Tool description here
"""
import logging
from langchain_core.tools import BaseTool
from .logging_config import setup_tool_logger

logger = setup_tool_logger("tool_name")

class NewTool(BaseTool):
    name: str = "tool_name"
    description: str = """
    Detailed tool description for the AI agent.
    """
    
    def _run(self, tool_input, run_manager=None) -> dict:
        """Implement tool logic here"""
        try:
            # Tool implementation
            result = {"success": True, "data": "..."}
            logger.info("Tool executed successfully")
            return result
        except Exception as e:
            logger.error(f"Tool failed: {str(e)}")
            return {"error": str(e)}
```

#### Testing

```bash
# Run tests (when implemented)
pytest tests/

# Run with coverage
pytest tests/ --cov=tools --cov=process_analyzer
```

#### Submitting Changes

1. **Test Your Changes**: Ensure all tests pass and functionality works
2. **Update Documentation**: Update relevant documentation files
3. **Commit Changes**:
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```
4. **Push and Create PR**:
   ```bash
   git push origin feature/your-feature-name
   # Create Pull Request on GitHub
   ```

#### Commit Message Format

Use conventional commit messages:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add support for BGP configuration
fix: resolve timeout issue with device connections
docs: update API reference for new tools
```

## 🏗 Architecture Overview

### Core Components

1. **Tools**: LangChain-based tools for network operations
2. **Process Analyzer**: Session documentation and analysis
3. **Web Interface**: Chainlit-based conversational UI
4. **AI Agent**: LangChain ReAct agent with DeepSeek LLM

### Design Principles

- **Modularity**: Each tool is self-contained
- **Extensibility**: Easy to add new tools and features
- **Error Handling**: Comprehensive error handling and recovery
- **Documentation**: Complete documentation for all components
- **Testing**: Full test coverage for reliability

## 📋 Development Checklist

### Before Submitting PR

- [ ] Code follows style guidelines (Black, Pylint, MyPy)
- [ ] All tests pass
- [ ] Documentation is updated
- [ ] Error handling is implemented
- [ ] Logging is added
- [ ] API reference is updated
- [ ] Examples are provided (if applicable)

### Code Review Process

1. **Automated Checks**: CI/CD pipeline runs tests and linting
2. **Manual Review**: Maintainers review code for:
   - Functionality and correctness
   - Code quality and style
   - Documentation completeness
   - Security considerations
   - Performance impact

3. **Approval**: At least one maintainer approval required

## 🐛 Bug Fix Guidelines

### Reproducible Issues

1. **Isolate the Problem**: Create minimal reproduction case
2. **Add Tests**: Write tests that fail before the fix
3. **Implement Fix**: Make minimal changes to fix the issue
4. **Verify Fix**: Ensure tests pass and issue is resolved

### Debugging Tips

- Check log files in `log/` directory
- Use debug mode: `logging.basicConfig(level=logging.DEBUG)`
- Test with different GNS3 project configurations
- Verify network connectivity and firewall settings

## 📚 Documentation Contributions

### Types of Documentation

1. **API Documentation**: Auto-generated from docstrings
2. **User Guides**: Step-by-step instructions
3. **Developer Guides**: Technical implementation details
4. **Examples**: Code examples and use cases

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots where helpful
- Use consistent formatting
- Include troubleshooting information

## 🌟 Recognition

Contributors are recognized in:

- **README.md**: Contributors section
- **Release Notes**: Feature contributions
- **Git History**: Commit attribution
- **Community**: Special recognition for significant contributions

## 📞 Getting Help

### Communication Channels

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For general questions and discussions
- **Documentation**: Check existing documentation first

### Maintainers

Current maintainers can be found in the repository's `CODEOWNERS` file.

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🔄 Release Process

### Version Management

- **Semantic Versioning**: MAJOR.MINOR.PATCH
- **Release Notes**: Detailed changelog for each release
- **Tagging**: Git tags for each release version

### Release Checklist

- [ ] All tests pass
- [ ] Documentation is updated
- [ ] CHANGELOG.md is updated
- [ ] Version is bumped
- [ ] Release tag is created
- [ ] GitHub Release is published

---

Thank you for contributing to GNS3 Copilot! Your contributions help make this project better for everyone.
