# 🚀 Project Announcement: GNS3 Copilot — Building the AI-Powered Assistant for Network Labs

---

Hi everyone! 👋

I'm excited to officially announce **GNS3 Copilot**, an open-source project I've been working on for the past few months. My goal is to transform how we interact with network labs by bringing the power of LLMs and AI Agents to the networking world.

## 💡 The Vision

The vision is simple: Let engineers manage complex network topologies using natural language. Whether it's creating nodes, connecting links, configuring OSPF, or troubleshooting connectivity, GNS3 Copilot acts as your intelligent pair-engineer.

---

## Current Status (Single-Agent Prototype)

We have a working prototype that already supports:

### Natural Language Interaction
Powered by a LangGraph-based agent.

### Tool-Enabled GNS3 API Integration
A comprehensive suite of tools built on top of the GNS3 REST API, allowing the LLM to perform Function Calling to dynamically create projects, manage nodes, and configure links based on real-time intent.

### Streamlit Web UI
A clean interface for real-time chat and execution feedback.

---

## Lessons from the Lab: Why we need more than one Agent

In building the initial prototype, I spent a month "living" in LLM + GNS3. These Practical Insights directly informed our move toward a Multi-Agent architecture:

### The "Endless Patience" Factor
LLMs are the ultimate 24/7 mentors. They never get tired of your "Active" BGP status. But as a Single Agent, they can sometimes get lost in the "trees" and forget the "forest."

### The Hallucination Barrier
While AI knows standard RFCs (OSPF/BGP) inside out, it can struggle with proprietary vendor logic or complex redistribution. I learned that we shouldn't ask AI for the "answer," but for a Diagnostic Tree.

### The "Spatial" Limit
In topologies with 20+ nodes, a single LLM session often hits a "logic ceiling." It can't "see" the whole map at once, which is why we are moving to a Modular Planning approach.

### Safety in Simulation
The best part of GNS3 + AI is the freedom to fail. I've realized that letting the AI "break" a lab is the fastest way for an engineer to learn.

---

## The Next Evolution: Multi-Agent System (Planned)

To address the limitations discovered above, we are evolving GNS3 Copilot into a sophisticated Multi-Agent System.

As the project evolves, we are moving towards a sophisticated Multi-Agent System Architecture to ensure reliability and handle complex networking tasks.

### 1. Multi-Agent Role Assignment

We employ distinct agents, each specializing in a specific function:

| Agent | Responsibility |
|-------|----------------|
| **Planning Agent** | Identifies user intent and formulates a detailed step-by-step task plan. |
| **Execution Agent** | Executes specific device operations according to the plan. |
| **Supervision Agent** | Continuously monitors results. If issues occur, it triggers a Retry or calls the Expert Agent. |
| **Expert Agent** | Addresses complex failures, provides high-level guidance, and corrects the original plan. |

### 2. The Closed-Loop Workflow

To ensure self-correction and high success rates, the system operates in a rigorous loop:

1. **User Input**: The system receives a high-level request (e.g., "Set up a dual-stack BGP core").
2. **Planning**: The Planning Agent breaks this down into API calls and configuration commands.
3. **Execution**: The Execution Agent interacts with GNS3/EVE-NG devices.
4. **Monitoring**: The Supervision Agent verifies the state (e.g., "Is the BGP session up?").
5. **Intervention**: If a link stays 'Down', the Expert Agent analyzes the logs, corrects the config, and loops back to the execution phase.
6. **Final Delivery**: Once verified, the completed work is presented to the user.

---

## The Roadmap

### Phase 1: Core Experience
- Human-in-the-Loop (HITL) confirmation
- Syntax highlighting

### Phase 2: Seamless Integration
- Split-screen UI (Chat + GNS3 Web UI) ✅

### Phase 3: Multi-Platform Support
- Adding **EVE-NG, Cisco CML, and Containerlab.** 🚫

### Phase 4: Ecosystem Expansion (MCP)
- Packaging as a Model Context Protocol (MCP) server for integration with Claude Desktop & Gemini CLI.

---

## 🤝 Join the Journey!

This is an open-source initiative, and I would love to hear from the community.

### Feedback
What features would save you the most time in the lab?

### Contributions
Whether it's code, documentation, or testing, all hands are welcome!

### Support
If you find this project interesting, please give it a ⭐ **Star the Repo** to follow progress.

---

Let's make network labs smarter, faster, and more enjoyable together! 🚀