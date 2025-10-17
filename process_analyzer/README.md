# GNS3 Copilot Process Analyzer Module

A comprehensive process analysis and documentation system that captures complete execution workflows (Thought/Action/Action Input/Observation/Final Answer) with robust error handling and recovery mechanisms.

## 🚀 Features

- **Complete Process Capture**: Records full ReAct execution cycles with detailed context
- **Error Recovery**: Automatic interruption handling and emergency save functionality
- **Documentation Generation**: Creates technical analysis and summary reports automatically
- **LangChain Integration**: Seamless callback handler integration with Chainlit
- **Session Management**: Comprehensive session tracking with timestamp-based organization
- **Report Distribution**: Automatic sharing of technical reports in chat interface
- **Historical Analysis**: Complete record of all user interactions for learning and debugging

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

The process analyzer automatically generates comprehensive reports for each user session:

### Report Types
- **Technical Analysis**: Detailed execution process with tool usage statistics, timing information, and step-by-step breakdown
- **Summary Report**: Quick overview of key points, results, and recommendations

### Report Storage
- **Location**: All reports are saved to the `../reports/` directory
- **Naming Convention**: `session_YYYYMMDD_HHMMSS_X_technical.md` where X is the session number
- **Automatic Sharing**: Technical reports are automatically shared in the Chainlit chat interface
- **Historical Tracking**: Complete session history maintained for analysis and debugging

### Accessing Reports
```bash
# List all generated reports
ls ../reports/

# View latest report
ls -t ../reports/ | head -1

# Search for specific sessions
grep -r "Configure OSPF" ../reports/
```

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

## 🐛 Troubleshooting

### Common Issues

1. **Report Generation Failures**
   - **Symptom**: Reports not generated after session completion
   - **Solution**: Check `../reports/` directory permissions and disk space
   - **Log**: Check `../log/gns3_copilot.log` for error details

2. **Session Data Loss**
   - **Symptom**: Incomplete session data in reports
   - **Cause**: Application interruption during execution
   - **Solution**: Emergency save functionality automatically preserves progress

3. **File Permission Errors**
   - **Symptom**: Cannot write to reports directory
   - **Solution**: Ensure write permissions for the application user
   - **Command**: `chmod 755 ../reports/`

### Error Recovery

The process analyzer includes robust error recovery mechanisms:

- **Automatic Interruption Detection**: Catches `KeyboardInterrupt`, connection errors, and timeouts
- **Emergency Save**: Automatically saves session progress during unexpected termination
- **Error Classification**: Distinguishes between different types of errors for targeted recovery
- **Graceful Degradation**: Continues operation even if some components fail

## ⚙️ Configuration

### Output Directory Configuration
```python
# Custom output directory (default: ../reports/)
learning_cb = LearningDocumentationCallback(output_dir="/custom/path")
```

### Session Management
```python
# Configure session retention
learning_cb.max_sessions = 100  # Maximum sessions to keep
learning_cb.cleanup_interval = 3600  # Cleanup interval in seconds
```

## 📈 Performance Considerations

- **Session Overhead**: Minimal impact on execution performance
- **Memory Usage**: Approximately 1-2MB per typical session
- **Disk Usage**: Reports typically 10-50KB each
- **Cleanup**: Automatic cleanup prevents disk space issues

---

*Transforms GNS3 Copilot into a learning platform with robust error handling and comprehensive documentation.*
