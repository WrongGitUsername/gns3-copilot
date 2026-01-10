# GNS3 Copilot Documentation

This directory contains all documentation for the GNS3 Copilot project.

## Directory Structure

```
docs/
├── README.md                                # This file - documentation index
├── project-announcement.md                  # Project announcement and roadmap
├── architecture/                            # Architecture documentation
│   ├── README.md                            # Architecture index
│   ├── README_ZH.md                         # Architecture index (Chinese)
│   ├── system-architecture.md               # System architecture overview
│   ├── system-architecture_ZH.md            # System architecture overview (Chinese)
│   ├── core-framework-design.md             # Core framework design
│   ├── core-framework-design_ZH.md          # Core framework design (Chinese)
│   └── images/                             # Architecture diagrams
│       ├── gns3_copilot_architecture.svg
│       ├── framework-data-flow.svg
│       ├── langchain-tools.svg
│       ├── langgraph-agent.svg
│       ├── multi-agent.svg
│       ├── config-first-party.jpeg
│       ├── config-third-party.jpeg
│       └── gns3-select-project.jpeg
├── user/                                    # User-facing documentation
│   ├── FAQ.md                               # Frequently asked questions
│   ├── FAQ_ZH.md                            # FAQ (Chinese)
│   ├── llm-quick-configuration-guide.md     # LLM quick setup guide
│   ├── llm-quick-configuration-guide_zh.md  # LLM quick setup guide (Chinese)
│   ├── checkpoint-import-export-guide.md  # Checkpoint import/export guide
│   └── checkpoint-import-export-guide_ZH.md # Checkpoint import/export guide (Chinese)
├── development/                             # Development documentation
│   ├── testing/                             # Testing guides and reports
│   │   ├── manual_testing_guide.md          # Manual testing instructions
│   │   ├── manual_testing_guide_zh.md       # Manual testing instructions (Chinese)
│   │   ├── TEST_COVERAGE_REPORT.md          # Test coverage statistics
│   │   └── TEST_COVERAGE_REPORT_ZH.md       # Test coverage statistics (Chinese)
│   ├── automation/                          # Automation tools documentation
│   │   ├── auto-commit-usage-guide.md       # Auto commit script guide
│   │   ├── auto-commit-usage-guide_zh.md    # Auto commit script guide (Chinese)
│   │   ├── auto-doc-automation-guide.md     # Auto documentation guide
│   │   ├── auto-doc-automation-guide_zh.md  # Auto documentation guide (Chinese)
│   │   ├── doc-update-improvements.md       # Documentation improvements
│   │   └── doc-update-improvements_zh.md    # Documentation improvements (Chinese)
│   └── evolution/                           # Project evolution planning
│       ├── GNS3-Copilot Backend Evolution Plan.md    # Backend evolution roadmap
│       └── GNS3-Copilot-Backend-Evolution-Plan_ZH.md # Backend evolution roadmap (Chinese)
└── technical/                               # Technical documentation
    ├── gns3-drawing-svg-format-guide.md     # GNS3 drawing format guide
    └── gns3-drawing-svg-format-guide_zh.md  # GNS3 drawing format guide (Chinese)
```

## Quick Start

### For Users

If you're looking to use GNS3 Copilot, start with:
- [Project Announcement](project-announcement.md) - Project overview, features, and roadmap
- [FAQ](user/FAQ.md) - Common questions and troubleshooting
- [LLM Quick Configuration Guide](user/llm-quick-configuration-guide.md) - Setting up your LLM provider

### For Developers

If you want to contribute or understand the codebase:
- [Manual Testing Guide](development/testing/manual_testing_guide.md) - How to test the application
- [Test Coverage Report](development/testing/TEST_COVERAGE_REPORT.md) - Test statistics
- [Auto Commit Usage Guide](development/automation/auto-commit-usage-guide.md) - Automated commit messages
- [Backend Evolution Plan](development/evolution/GNS3-Copilot%20Backend%20Evolution%20Plan.md) - Project roadmap

### For Technical Details

If you need technical specifications:
- [System Architecture](architecture/system-architecture.md) - System architecture overview (7-layer design)
- [Core Framework Design](architecture/core-framework-design.md) - Detailed LangGraph and LangChain framework design
- [GNS3 Drawing SVG Format Guide](technical/gns3-drawing-svg-format-guide.md) - Drawing format specification

### For Architecture Documentation

If you want to understand the system architecture:
- [Architecture Index](architecture/README.md) - Complete architecture documentation
- [System Architecture (中文)](architecture/system-architecture_ZH.md) - System architecture in Chinese
- [Core Framework Design (中文)](architecture/core-framework-design_ZH.md) - Framework design in Chinese

## Documentation Language

Most documentation is available in both English and Chinese (simplified). Chinese versions are suffixed with `_ZH.md`.

## Related Resources

- [Architecture Documentation](architecture/) - System architecture diagrams and design docs
- [Source Code](../src/gns3_copilot/) - Application source code
- [Test Files](../tests/) - Test suite and test files
