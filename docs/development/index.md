# Development Guide

This section contains development resources for contributors and developers working on GNS3 Copilot.

## Getting Started

If you're new to contributing to GNS3 Copilot, please refer to:

1. **[Testing Guide](testing/manual_testing_guide.md)** - Manual testing procedures
2. **[Auto Commit Guide](automation/auto-commit-usage-guide.md)** - Automated commit workflow
3. **[Auto Documentation Guide](automation/auto-doc-automation-guide.md)** - Documentation automation

## Branching Strategy

We use the following branching strategy:

```
master (Production)
    ↑
Development (Main Development Branch)
    ↑
feature/* (Feature Branches)
```

- **master**: Stable production releases
- **Development**: Main development branch - merge all PRs here
- **feature/***: Feature branches created from Development

## Available Documentation

### Testing
- [Manual Testing Guide (English)](testing/manual_testing_guide.md) - Manual testing procedures
- [手动测试指南 (中文)](testing/manual_testing_guide_zh.md) - 手动测试程序
- [Test Coverage Report (English)](testing/TEST_COVERAGE_REPORT.md) - Code coverage statistics
- [测试覆盖率报告 (中文)](testing/TEST_COVERAGE_REPORT_ZH.md) - 代码覆盖率统计

### Automation
#### Auto Commit
- [Auto Commit Usage Guide (English)](automation/auto-commit-usage-guide.md) - Using automated commit workflow
- [自动提交使用指南 (中文)](automation/auto-commit-usage-guide_zh.md) - 使用自动提交工作流

#### Auto Documentation
- [Auto Documentation Guide (English)](automation/auto-doc-automation-guide.md) - Documentation automation process
- [自动文档指南 (中文)](automation/auto-doc-automation-guide_zh.md) - 文档自动化流程

#### Documentation Improvements
- [Documentation Improvements (English)](automation/doc-update-improvements.md) - Documentation update improvements
- [文档更新改进 (中文)](automation/doc-update-improvements_zh.md) - 文档更新改进

### Evolution
- [Backend Evolution Plan (English)](evolution/GNS3-Copilot%20Backend%20Evolution%20Plan.md) - Future development roadmap
- [后端演进计划 (中文)](evolution/GNS3-Copilot-Backend-Evolution-Plan_ZH.md) - 未来开发路线图

## Development Commands

```bash
# Install development dependencies
pip install -e ".[dev,docs]"

# Run tests
pytest

# Run tests with coverage
pytest --cov=gns3_copilot --cov-report=html

# Code linting
ruff check src/

# Code formatting
ruff format src/

# Type checking
mypy src/

# Security check
safety scan

# Build documentation locally
mkdocs serve
```

## Code Style Guidelines

We follow these code style standards:

- **PEP 8** - Python code style
- **Type Hints** - Public functions must have type annotations
- **Docstrings** - Google or NumPy style docstrings
- **Line Length** - Maximum 88 characters (Black formatting)

## Submitting Changes

1. Create a feature branch from Development:
   ```bash
   git checkout -b feature/your-feature Development
   ```

2. Make your changes and commit them

3. Push your branch:
   ```bash
   git push origin feature/your-feature
   ```

4. Create a Pull Request to the **Development** branch

5. Ensure all CI checks pass before requesting review

## CI/CD Pipeline

Our CI/CD pipeline includes:

- **Linting** - Ruff code style checking
- **Type Checking** - Mypy static type checking
- **Security Scanning** - Safety dependency scanning
- **Testing** - Pytest with coverage reporting
- **Documentation** - Auto-updating documentation on PR
- **Release** - Automated PyPI publishing on version tags