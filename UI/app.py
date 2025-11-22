import json
import uuid
import streamlit as st
from langchain.messages import ToolMessage, HumanMessage, AIMessage
from agent import agent
from public_model import format_tool_response
        

# streamlit UI
st.set_page_config(page_title="GNS3 Copilot", layout="wide")
st.title("GNS3 Copilot")

# Unique thread ID for each session
config = {"configurable": {"thread_id": str(uuid.uuid4()), "max_iterations": 100}}

# siderbar info
with st.sidebar:
    st.title("About")
    st.markdown(
        """
        GNS3 Copilot is an AI-powered assistant designed to help network engineers with GNS3-related tasks. 
        It leverages advanced language models to provide insights, answer questions, and assist with network simulations.
        
        **Features:**
        - Answer GNS3-related queries
        - Provide configuration examples
        - Assist with troubleshooting
        
        **Usage:**
        Simply type your questions or commands in the chat interface, and GNS3 Copilot will respond accordingly.
        
        **Note:** This is a prototype version. For more information, visit the [GNS3 Copilot GitHub Repository](https://github.com/yueguobin/gns3-copilot).
        """
    )
         
# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):

        current_text_chunk = ""
        active_text_placeholder = st.empty() 
        
        # Core aggregation state: only stores currently streaming tool information
        # Structure: {'id': str, 'name': str, 'args_string': str} or None
        current_tool_state = None
        
        # History container: used to sequentially accumulate and display all tool calls and responses, solving UI disorder issues
        tool_history_container = st.container()
        
        # Stream the agent response
        for chunk in agent.stream(
            {"messages": [HumanMessage(content=prompt)]},
            config=config,
            stream_mode="messages"
            ):
        
            for msg in chunk:
                #with open('log.txt', "a", encoding='utf-8') as f:
                #    f.write(f"{msg}\n\n")
                                       
                if isinstance(msg, AIMessage):
                    
                    # Check if content is a list and safely extract the first text element, adapted for gemini
                    if isinstance(msg.content, list) and msg.content and 'text' in msg.content[0]:
                        actual_text = msg.content[0]['text']
                        # Now actual_text is the clean text you need
                        current_text_chunk += actual_text
                        active_text_placeholder.markdown(current_text_chunk, unsafe_allow_html=True)
                        
                    elif isinstance(msg.content, str):                                                    
                        current_text_chunk += str(msg.content)
                        active_text_placeholder.markdown(current_text_chunk, unsafe_allow_html=True)
                    
                    # Get metadata (ID and name) from tool_calls
                    if msg.tool_calls:
                        for tool in msg.tool_calls:
                            tool_id = tool.get('id')
                            if tool_id: # Only when ID is not empty, consider it as the start of a new tool call
                                # Initialize current tool state (this is the only time to get ID)
                                # Note: only one tool can be called at a time
                                current_tool_state = {
                                    "id": tool_id, 
                                    "name": tool.get('name', 'UNKNOWN_TOOL'),
                                    "args_string": "" ,
                                }   
                                
                    # Concatenate parameter strings from tool_call_chunk
                    if hasattr(msg, 'tool_call_chunks') and msg.tool_call_chunks:
                        if current_tool_state:
                            tool_data = current_tool_state
                            
                            for chunk_update in msg.tool_call_chunks:
                                args_chunk = chunk_update.get('args', '')
                                    
                                    # Core: string concatenation
                                if isinstance(args_chunk, str):
                                    tool_data['args_string'] += args_chunk
                                                                
                elif isinstance(msg, ToolMessage):
                    # Check if ToolMessage's ID matches current state
                    if current_tool_state and current_tool_state['id'] == msg.tool_call_id:
                        tool_data = current_tool_state
                        # Parse complete parameter string
                        parsed_args = {}
                        try:
                            parsed_args = json.loads(tool_data['args_string'])
                        except json.JSONDecodeError:
                            parsed_args = {"error": "JSON parse failed after stream complete."}
                        
                        # Serialize the tool_input value in parsed_args to a JSON array for expansion when using st.json
                        command_list = json.loads(parsed_args['tool_input'])
                        parsed_args['tool_input'] = command_list
                        
                        # Build the final display structure that meets your requirements
                        display_tool_call = {
                            "name": tool_data['name'],
                            "id": tool_data['id'],
                            # Inject tool_input structure
                            "args": parsed_args, 
                            "type": tool_data.get('type', 'tool_call') # Maintain completeness
                        }
                        
                        # Update Call Expander, display final parameters (collapsed)
                        with st.expander(
                            f"**Tool Call Complete:** `{tool_data['name']}`", expanded=False
                        ):
                            # Use the final complete structure
                            st.json(display_tool_call)
                            
                    # Clear state after completion, ready to receive next tool call
                    current_tool_state = None
                            
                    content_pretty = format_tool_response(msg.content)
                                          
                    with st.expander("**Tool Response**"):
                        st.json(json.loads(content_pretty), expanded=False)
                    
                    active_text_placeholder = st.empty()
