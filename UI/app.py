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
        
        # 核心聚合状态：只存储当前正在流式传输的工具信息
        # 结构: {'id': str, 'name': str, 'args_string': str} 或 None
        current_tool_state = None
        
        # 历史容器：用于按顺序累积显示所有工具调用和响应，解决 UI 错乱问题
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
                    
                    # 检查 content 是否为列表，并安全地提取第一个文本元素，适配gemini
                    if isinstance(msg.content, list) and msg.content and 'text' in msg.content[0]:
                        actual_text = msg.content[0]['text']
                        # 现在 actual_text 才是您需要的干净文本
                        current_text_chunk += actual_text
                        active_text_placeholder.markdown(current_text_chunk, unsafe_allow_html=True)
                        
                    elif isinstance(msg.content, str):                                                    
                        current_text_chunk += str(msg.content)
                        active_text_placeholder.markdown(current_text_chunk, unsafe_allow_html=True)
                    
                    # 从tool_calls中获取元数据（ID和name）
                    if msg.tool_calls:
                        for tool in msg.tool_calls:
                            tool_id = tool.get('id')
                            if tool_id: # 只有当 ID 非空时，才认为是一个新的工具调用开始
                                # 初始化当前工具状态（这是唯一获取 ID 的时机）
                                # 注意： 只能一次调用一个工具
                                current_tool_state = {
                                    "id": tool_id, 
                                    "name": tool.get('name', 'UNKNOWN_TOOL'),
                                    "args_string": "" ,
                                }   
                                
                    # 从tool_call_chunk拼接参数字符串
                    if hasattr(msg, 'tool_call_chunks') and msg.tool_call_chunks:
                        if current_tool_state:
                            tool_data = current_tool_state
                            
                            for chunk_update in msg.tool_call_chunks:
                                args_chunk = chunk_update.get('args', '')
                                    
                                    # 核心：字符串拼接
                                if isinstance(args_chunk, str):
                                    tool_data['args_string'] += args_chunk
                                                                
                elif isinstance(msg, ToolMessage):
                    # 检查 ToolMessage 的 ID 是否匹配当前状态
                    if current_tool_state and current_tool_state['id'] == msg.tool_call_id:
                        tool_data = current_tool_state
                        # 解析完整的参数字符串
                        parsed_args = {}
                        try:
                            parsed_args = json.loads(tool_data['args_string'])
                        except json.JSONDecodeError:
                            parsed_args = {"error": "JSON parse failed after stream complete."}
                        
                        # 将parsed_args中的tool_input的值序列为json数组，以便在st.json时展开。
                        command_list = json.loads(parsed_args['tool_input'])
                        parsed_args['tool_input'] = command_list
                        
                        # 构建符合您要求的最终显示结构
                        display_tool_call = {
                            "name": tool_data['name'],
                            "id": tool_data['id'],
                            # 注入 tool_input 结构
                            "args": parsed_args, 
                            "type": tool_data.get('type', 'tool_call') # 保持完整性
                        }
                        
                        # 更新 Call Expander，显示最终参数 (折叠起来)
                        with st.expander(
                            f"**Tool Call Complete:** `{tool_data['name']}`", expanded=False
                        ):
                            # 使用最终的完整结构
                            st.json(display_tool_call)
                            
                    # 完成后清除状态，准备接收下一个工具调用
                    current_tool_state = None
                            
                    content_pretty = format_tool_response(msg.content)
                                          
                    with st.expander("**Tool Response**"):
                        st.json(json.loads(content_pretty), expanded=False)
                    
                    active_text_placeholder = st.empty()