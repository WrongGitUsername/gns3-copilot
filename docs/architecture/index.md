# Architecture Documentation

This section contains comprehensive documentation about GNS3 Copilot's system architecture and framework design.

## Available Documentation

### System Architecture
- [System Architecture (English)](system-architecture.md) - Complete system architecture overview
- [系统架构 (中文)](system-architecture_ZH.md) - 完整系统架构概览

### Core Framework Design
- [Core Framework Design (English)](core-framework-design.md) - Detailed framework design documentation
- [核心框架设计 (中文)](core-framework-design_ZH.md) - 详细框架设计文档

## Architecture Overview

GNS3 Copilot is built using a modular architecture with the following key components:

```
┌─────────────────────────────────────────────────────────────┐
│                      Presentation Layer                      │
│                   (Streamlit Web UI)                        │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    Agent Layer (LangGraph)                   │
│  - Intent Recognition                                        │
│  - Tool Selection & Invocation                              │
│  - Conversation Management                                   │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                     Tool Integration Layer                   │
│  - GNS3 API Tools                                            │
│  - Configuration Tools (Nornir/Netmiko)                      │
│  - Display Tools                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                    GNS3 Client Layer                        │
│  - GNS3 Server Communication                                 │
│  - Project Management                                        │
│  - Topology Operations                                       │
└───────────────────────┬─────────────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────────────┐
│                      GNS3 Server API                         │
└─────────────────────────────────────────────────────────────┘
```

## Key Technologies

- **Frontend UI**: Streamlit
- **AI Framework**: LangGraph + LangChain
- **Network Automation**: Nornir + Netmiko + Telnetlib3
- **GNS3 Integration**: gns3fy (custom enhanced)
- **Data Persistence**: SQLite
- **LLM Support**: OpenAI, DeepSeek, Anthropic, XAI, OpenRouter, etc.