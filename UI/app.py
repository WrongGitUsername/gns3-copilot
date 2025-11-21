import json
import ast
import uuid
import streamlit as st
from langchain.messages import ToolMessage, HumanMessage, AIMessage
from agent import agent
from public_model import format_tool_response
        
# spinner_html
SPINNER_HTML = """
<div style="text-align: left; margin: 20px 0;">
  <span style="
    display: inline-block;
    width: 20px; height: 20px;
    border: 3px solid #f0f0f0;
    border-top: 3px solid #1e88e5;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  "></span>
</div>
<style>
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>
"""    

# streamlit UI
st.set_page_config(page_title="GNS3 Copilot", layout="wide")
st.title("GNS3 Copilot")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Unique thread ID for each session
config = {"configurable": {"thread_id": str(uuid.uuid4())}}

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
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        # 使用st.spinner显示加载动画
        with st.spinner('GNS3 Copilot is working...'):
            
            # Initialize messages
            human = [
                HumanMessage(
                    content=prompt
                )
            ]

            # Stream the agent response
            for chunk in agent.stream(
                {"messages": human},
                config=config,
                stream_mode="updates"
                ):
            
                for node_name, update in chunk.items():
                    if "messages" in update:
                        for msg in update["messages"]:
                            if isinstance(msg, AIMessage):
                                full_response += (
                                    "---\n\n"
                                    f"{msg.content}"
                                    )
                                message_placeholder.markdown(full_response, unsafe_allow_html=True)
                                
                                if msg.tool_calls:
                                    for tool in msg.tool_calls:
                                        args_pretty = format_tool_response(tool.get('args').get('tool_input'))
                                        full_response += (
                                            f"\n\n **Tool Used:** {tool.get('name')}\n\n"                                            
                                            "<details>\n"
                                            "<summary>Tool Call Details</summary>\n\n"
                                            f"```json\n\n"
                                            f"{args_pretty}\n\n"
                                            "```\n\n"
                                            "</details>\n\n"
                                            )
                                        message_placeholder.markdown(full_response, unsafe_allow_html=True)
                            
                            elif isinstance(msg, ToolMessage):
                                content_pretty = format_tool_response(msg.content)
                                full_response += (
                                    f"\n\n **Tool Response:** \n\n"
                                    "<details>\n"
                                    "<summary>Tool Response Details</summary>\n\n"
                                    "```json\n\n"
                                    f"{content_pretty}\n\n"
                                    "```\n\n"
                                    "</details>\n\n"
                                )
                                message_placeholder.markdown(full_response, unsafe_allow_html=True)

            # Finalize the assistant message
            #message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})