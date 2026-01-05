# GNS3 Copilot Architecture Documentation

This directory contains the system architecture and framework design documentation for GNS3 Copilot.

## Document Index

### Core Architecture Documents

- **[System Architecture](system-architecture.md)** - Comprehensive overview of the GNS3 Copilot system architecture, including all layers and their interactions
- **[Core Framework Design](core-framework-design.md)** - Detailed design of the LangGraph agent framework, LangChain tool integration, and data flow architecture

## Architecture Diagrams

All architecture diagrams and flowcharts are located in the [images/](images/) directory:

### Mermaid/SVG Diagrams
- `gns3_copilot_architecture.svg` - Complete system architecture diagram
- `framework-data-flow.svg` - Data flow between components
- `langchain-tools.svg` - LangChain tool integration framework
- `langgraph-agent.svg` - LangGraph intelligent agent framework
- `multi-agent.svg` - Multi-agent system architecture

### Screenshot Images
- `config-first-party.jpeg` - First-party provider configuration
- `config-third-party.jpeg` - Third-party provider configuration
- `gns3-select-project.jpeg` - GNS3 project selection interface

## Architecture Overview

GNS3 Copilot follows a **7-layer architecture**:

1. **Presentation Layer** - Streamlit web interface
2. **LangGraph Agent Framework** - AI orchestration and state management
3. **Tool Integration Layer** - Network automation tools
4. **Network Automation Framework** - Nornir-based concurrent execution
5. **GNS3 Integration Framework** - Custom GNS3 API client
6. **Data Persistence Layer** - SQLite databases and logging
7. **Infrastructure Layer** - GNS3 server and network devices

## Key Frameworks

- **LangGraph** - State machine workflow and agent orchestration
- **LangChain** - Tool integration and LLM abstraction
- **Nornir** - High-performance concurrent network automation
- **Streamlit** - Web UI framework

## Quick Reference

### System Components
- **Agent**: Multi-agent system with Planning, Execution, Supervision, and Expert agents
- **Tools**: 9 specialized tools for GNS3 management and network automation
- **State Management**: SQLite-based checkpointing for conversation persistence
- **Execution**: Concurrent device operations via Nornir thread pools

### Data Flow
1. User input → Streamlit UI
2. LangGraph StateGraph processes input
3. LLM decides which tools to call
4. Tools execute network operations via Nornir/GNS3 client
5. Results flow back through agent to UI
6. Conversation state persisted via SQLite checkpoints

## Related Documentation

- [FAQ](../user/FAQ.md) - Common questions about the system
- [Testing Guide](../development/testing/manual_testing_guide.md) - How to test the architecture
- [Backend Evolution Plan](../development/evolution/GNS3-Copilot%20Backend%20Evolution%20Plan.md) - Future roadmap
