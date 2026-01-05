# FAQ - GNS3 Copilot Frequently Asked Questions

This document collects common questions and solutions encountered while using GNS3 Copilot.

---

## Chat page cannot get new address after modifying GNS3 Server configuration

### Problem Description

After modifying the GNS3 Server URL or other configuration in the Settings page and clicking save, when switching to the Chat page, the topology iframe displayed by the Show button still uses the old GNS3 Server address instead of the newly configured address. This also applies to LLM model configuration changes.

### Root Cause Analysis

This is caused by Streamlit's Widget behavior mechanism:

1. **Widgets do not maintain state across pages**
   - Even with the same key, widgets on different pages are considered different instances
   - The widget key (e.g., `key="GNS3_SERVER_URL"`) from the Settings page is automatically deleted by Streamlit after switching pages

2. **Widget state only persists when executed**
   - If a widget is not called during a run, all its information (including the key in session_state) will be deleted

3. **Configuration loading mechanism**
   - The `load_config_from_env()` function uses the `_config_loaded` flag to avoid repeated loading
   - After first load, it's set to `True`, and subsequent page switches won't reload
   - After switching pages, the widget key is deleted, but `_config_loaded` remains `True`
   - Result: Chat page cannot read the new configuration value

### Complete Problem Flow

```
1. First launch
   ├─ load_config_from_env() executes
   ├─ Loads configuration from .env to session_state
   └─ Sets _config_loaded = True

2. User modifies configuration in Settings page
   ├─ widget overwrites values in session_state
   ├─ Clicks save button
   ├─ save_config_to_env() saves to .env file
   └─ Executes st.rerun()

3. Switch to Chat page
   ├─ app.py re-executes
   ├─ Settings page widgets no longer execute
   ├─ Streamlit deletes widget keys (GNS3_SERVER_URL, etc.)
   ├─ load_config_from_env() checks _config_loaded = True
   ├─ Skips configuration loading
   └─ Chat page reads new config using default values
```

### Solution

**Current Approach**: Restart the application

After modifying GNS3 Server configuration or LLM model settings, you must **restart the application** for the changes to take effect. Restarting will:

1. Clear session_state (including `_config_loaded` flag)
2. Re-execute app.py from the beginning
3. `load_config_from_env()` reloads configuration from .env file
4. Chat page gets the latest configuration values

**Operation Steps**:
```
1. Modify configuration and save in Settings page
2. Stop the gns3-copilot process
3. Restart the application
4. Configuration is now effective
```

**Important Notes**:
- **LLM model configuration changes require restarting the application**
- **GNS3 Server configuration changes require restarting the application**
- Simply refreshing the browser page (F5) is NOT sufficient for configuration changes to take effect

### Working Recommendations

- After initially configuring the GNS3 Server address and LLM model, verify the configuration works correctly before proceeding
- If configuration changes are needed, restart the application to ensure all changes take effect
- Test the configuration after each restart to confirm it's working as expected


### Related Code Locations

- Configuration loading logic: `src/gns3_copilot/ui_model/utils/config_manager.py`
  - `load_config_from_env()` - Load configuration
  - `save_config_to_env()` - Save configuration

- Settings page: `src/gns3_copilot/ui_model/settings.py`
  - Configuration input boxes (using widget keys)

- Chat page: `src/gns3_copilot/ui_model/chat.py`
  - `build_topology_iframe_url()` - Build GNS3 topology iframe URL
  - Read GNS3_SERVER_URL and other session_state configurations

### References

- [Streamlit Widget Behavior](https://docs.streamlit.io/library/advanced-features/widget-behavior)
- Streamlit official documentation on Widget state management

---

## Project Background and Architecture

### What's the difference between GNS3 Copilot and gns3-mcp?

Both projects are dedicated to combining AI with GNS3, but they take different technical approaches:

- **gns3-mcp**: Based on MCP (Model Context Protocol) server, using standard protocol with stronger interoperability
- **gns3-copilot**: Based on Streamlit + LangGraph, focused on multi-agent workflows

### Why use multi-agent architecture?

GNS3 Copilot adopts a multi-agent system architecture with the following roles:

- **Planning Agent**: Identifies user intent and formulates detailed task plans
- **Execution Agent**: Executes specific device operations step-by-step according to the plan
- **Supervision Agent**: Continuously monitors and evaluates execution results, requesting retries or notifying the expert agent when issues are found
- **Expert Agent**: Addresses complex problems, providing guidance, correcting plans, or proposing solutions

This closed-loop structure ensures reliability and self-correction capabilities.

### Why migrate from LangChain to LangGraph?

Initially used LangChain with ReAct prompting, but as the project grew, encountered these issues:

- **Context window bloat**: Leading to "LLM inattentiveness" and unreliable tool selection
- **Iteration limits**: LangChain/LangGraph inherently has `recursion_limit` and `max_iterations` constraints

After migrating to LangGraph, achieved:
- Dynamic prompting
- Hierarchical multi-agent workflows
- Proper state persistence
- Solving context length issues at the architecture level

### Why not use MCP?

Considered wrapping tools as an MCP agent to eliminate UI concerns, allowing any MCP-compatible client to be used. However, to experiment with LangGraph's multi-agent and StateManager features, temporarily put this idea on hold and built the UI using Streamlit instead.

---

## Technical Implementation

### Why fork gns3fy?

gns3fy is the most popular Python client for the GNS3 Server API, but it targets GNS3 Server 2.2. That repository has been inactive for over two years.

Submitted a small PR to be compatible with newer Pydantic versions, but never received a response. This eventually led to forking and extending the library.

Using the forked gns3fy as the foundation, built a collection of high-level tools:
- Topology exporter
- Node/link creation
- Dynamic console port lookup
- And more

All tools are deliberately designed to accept and return cleanly structured JSON objects and arrays—the format that works most reliably with modern LLMs.

### Why use Nornir instead of directly using Netmiko?

Initially used Netmiko directly to configure devices. To gain massive concurrency, migrated everything to Nornir with the nornir-netmiko plugin.

**Advantages**:
- **Token Savings**: Configuring 5 devices sequentially requires at least 5 llm_calls, each carrying the history of previous messages. With Nornir, all 5 devices' configurations can be accomplished within a single tool invocation
- **Time Efficiency**: Configuring devices one by one is too slow. Nornir can configure multiple devices simultaneously
- **Simplified Interaction**: LLM only needs to supply a simple JSON payload containing target node(s) and command list

### How to handle multi-device configuration?

When a device, like R-1, is added in GNS3, the GNS3 Server assigns a console port to it, for example, 5000.

When right-clicking this device in the Qt or web interface and selecting console to open a configuration window, what happens behind the scenes is essentially `telnet [gns3server address] 5000`.

Using Nornir's `nornir_netmiko` plugin can:
1. Parse console port via GNS3 API
2. Spawn parallel Netmiko/telnet sessions
3. Execute commands simultaneously
4. Return structured JSON results

### Why is JSON format important for LLMs?

The JSON format is indeed difficult to read, but:
- Once rendered in the UI (Streamlit), it's still readable
- Modern LLMs are best at handling structured data
- Each tool has detailed class docstrings, and LLMs rely on these docstrings to understand how to use the tool

Pro tip: Provide a few examples to the LLM, and it tends to follow your examples for its operation.

---

## LLM and Prompt Engineering

### Which LLM models are used?

Primarily use **DeepSeek** because it's:
- Very affordable
- Model capabilities meet requirements

Other experiences:
- **Gemini Flash**: Cheap but limited functionality
- **Grok Fast**: Cheap but limited functionality
- **MiniMax M2**: Surprisingly good
- **ChatGPT Network Engineer**: Fine-tuned model, much more professional at handling networking problems than general models like ChatGPT, Grok, or Gemini

Registered with OpenRouter just to verify API interface functionality, ended up spending $13 USD (approximately ¥100 RMB) within just one or two days.

### What impacts agent performance the most?

**Agent architecture, prompts, and capabilities** have greater impact than the model itself.

For example, Claude Code vs Warp (both using Sonnet 4.5):
- Warp works better with MCP resources but struggles to use tools properly
- Claude Code ignores resources altogether, requiring writing wrappers for them

### Do LLMs sometimes produce incorrect output?

Using LLMs is like opening a mystery box... LLMs simply compute an output that appears reasonable to humans based on human input.

Some interesting test cases:

**Example 1: Subnet mask and inverse mask relationship**
```
Question: Are the subnet mask and the inverse mask (wildcard mask) 
100% in a sum-to-255 relationship?
That is, if the subnet mask is 255.255.255.0 and the inverse mask 
is written as 0.0.0.255, is this sum-to-255 relationship 100% valid?
```

**Example 2: Configuration error**
```
Question: Why does this command sequence throw the error 
'Bad mask /27 for address 192.168.10.10'?

R1#conf t 
R1(config)#int fa0/0 
R1(config-if)#ip add 192.168.10.10 255.255.255.224 
Bad mask /27 for address 192.168.10.10
```

---

## Human-in-the-Loop

### How to implement human intervention?

Current concept: Human-in-the-Loop can be partially realized. Currently, however, it still requires humans to define specific operations or points at which human intervention should occur.

Possible implementation approach:
- Add a button allowing humans to stop and intervene whenever they observe something going wrong
- Modify the task and then resume work

Goal: To be able to follow the agent's actions without interfering too much—like watching someone behind their back, seeing their screen and actions in real-time and being able to ask for explanations or even change something. Current agents are not even close to this level.

---

## Documentation and Knowledge

### Is RAG used to integrate with vendor documentation?

This is the network engineer's competitive "moat." Every vendor possesses its own proprietary technologies and specialized documentation. General-purpose large language models cannot venture into this area.

**Challenges**:
- If RAG is to be implemented, raw data needs to be meticulously organized and chunked to achieve satisfactory results, which represents a massive amount of work
- Niche vendor simulators receive virtually no useful assistance from LLMs

**Current Status**:
- For learning, publicly available materials are often sufficient. LLM training datasets naturally wouldn't omit relevant documentation from networking giant Cisco
- In China, most people start learning with vendors like Huawei, H3C, and Ruijie

**Ideal Solution**:
- Every equipment vendor launches a "Document-based Knowledge Service (MCP)"—but this is likely unrealistic
- Most realistic solution: Integrate a search service tool, like Google Search API

### How to manage device credentials?

Load Linux username and password via environment variables. The `linux_tools_nornir` tool only needs to focus on the list of commands and device names.

The comments in `src/gns3_copilot/ui_model/settings.py` have already listed the information included in the .env file.

Plan to add more environment variable fields later. If any Security-related experiments are conducted, usernames and passwords for those specific devices will be necessary.

---

## Topology Management

### Why only implement CR (Create and Read) operations?

Topology management only implements the CR (Create and Read) operations of CRUD, because I don't want the LLM to destroy or modify the topology I have already set up.

### Why have a device startup tool but want to remove it?

The `gns3_start_node.py` tool may need to be removed because:
- When processing problems, the LLM will sometimes inexplicably assume a device has not started and proceed to execute the `gns3_start_node.py` tool
- There's no way to verify whether the device has truly started
- Implemented a built-in timer waiting function inside `gns3_start_node.py`: planned startup time for each device is about 120 seconds, with an additional 20% waiting time for every extra device

### Which devices does topology management support?

`config_tools_nornir.py` and `display_tools_nornir.py` accept `platform` and `device_type` as tool parameters. This allows leveraging all device models supported by `nornir_netmiko`.

---

## Additional Resources

### Related Documentation

- [GNS3-Copilot Architecture](../Architecture/gns3_copilot_architecture.md)
- [Core Framework Detailed Design](../Architecture/Core%20Framework%20Detailed%20Design.md)

### Flowcharts

You can view flowcharts in the [Architecture](../Architecture/) directory. The markdown documents might not be completely accurate or complete, as they were generated by the LLM based on the code. However, the SVG images have been modified by me and are generally correct.

### Prompt Templates

The main prompt is located in `src/gns3_copilot/prompt/react_prompt.py`.

### Related Projects

- [gns3-mcp](https://github.com/ChistokhinSV/gns3-mcp) - Another GNS3 + LLM project, based on MCP protocol

---

## References and Acknowledgments

### Learning Resources

- Powered by 《网络工程师的 Python 之路》
- Powered by 《网络工程师的 AI 之路》

### Streamlit Related

- [Streamlit Widget Behavior](https://docs.streamlit.io/library/advanced-features/widget-behavior)
- Streamlit official documentation on Widget state management
