# GNS3 Copilot Process Analyzer Module

Captures complete execution processes (Thought/Action/Action Input/Observation/Final Answer) with error handling and recovery.

## 🚀 Features

- **Complete Process Capture**: Records full ReAct execution cycles
- **Error Recovery**: Automatic interruption handling and emergency save
- **Documentation Generation**: Technical analysis and summary reports
- **LangChain Integration**: Seamless callback handler integration

## 📁 Structure

```
process_analyzer/
├── __init__.py                    # Module exports
├── process_callback.py            # Core callback handler
├── langchain_callback.py          # LangChain integration
├── documentation_generator.py     # Report generation
└── README.md                     # This file
```

## 🔧 Quick Start

### Basic Usage

```python
from process_analyzer import LearningDocumentationCallback

# Initialize
learning_cb = LearningDocumentationCallback()

# Start session
session_id = learning_cb.start_new_session("Configure OSPF")

# Record complete step
learning_cb.record_complete_step(
    thought="Need to configure OSPF",
    tool_name="execute_multiple_device_config_commands",
    action_input=[{"device_name": "R1", "config_commands": ["router ospf 1"]}]
)

# Add observation
learning_cb.add_observation_to_current_step("OSPF configured successfully")

# Complete session
learning_cb.record_final_answer("OSPF configuration completed")
session_data = learning_cb.finalize_session()
generated_files = learning_cb.save_session_to_file(session_data)
```

### LangChain Integration

```python
from process_analyzer import LearningLangChainCallback, LearningDocumentationCallback

learning_cb = LearningDocumentationCallback()
langchain_cb = LearningLangChainCallback(learning_cb)

# Use with LangChain agent
agent.run("Configure OSPF", callbacks=[langchain_cb])
```

## 📊 Generated Reports

- **Technical Analysis**: Detailed execution process with tool usage statistics
- **Summary Report**: Quick overview of key points and results

## 🛠️ Error Handling

- **Automatic Interruption Detection**: Handles KeyboardInterrupt, connection errors, timeouts
- **Emergency Save**: Automatically saves progress during interruptions
- **Error Classification**: Distinguishes ReAct parsing, tool execution, and general errors

## 📄 API Reference

### LearningDocumentationCallback

- `start_new_session(user_input)`: Start new session
- `record_complete_step(thought, tool_name, action_input)`: Record ReAct step
- `add_observation_to_current_step(observation)`: Add tool result
- `record_final_answer(answer)`: Record final answer
- `finalize_session()`: Complete and return session data
- `emergency_save(reason)`: Save during interruption

### LearningLangChainCallback

LangChain callback handler that automatically captures:
- Agent actions and thoughts
- Tool execution results
- Final answers
- Errors and interruptions

## 🔍 Integration Example

```python
# In gns3_copilot.py
from process_analyzer import LearningLangChainCallback, LearningDocumentationCallback

learning_cb = LearningDocumentationCallback()
langchain_cb = LearningLangChainCallback(learning_cb)

@cl.on_message
async def main(message: cl.Message):
    await process_agent_message(message, callbacks=[langchain_cb])
```

## 🛠️ Development

### Extending Functionality

```python
class CustomCallback(LearningDocumentationCallback):
    def custom_method(self, data):
        # Custom logic
        pass
```

### Debug Mode

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

*Transforms GNS3 Copilot into a learning platform with robust error handling.*
