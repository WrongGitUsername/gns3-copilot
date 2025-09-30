"""
GNS3 Network Automation Assistant

This module implements a conversational AI assistant for GNS3 network automation tasks.
It uses Chainlit for the user interface, LangChain for agent orchestration, and DeepSeek LLM
for natural language processing. The assistant can execute network commands, configure devices,
and manage GNS3 topology operations.
"""

import chainlit as cl
from dotenv import load_dotenv
load_dotenv()

from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain_deepseek import ChatDeepSeek
from tools.display_tools import ExecuteDisplayCommands
from tools.config_tools import ExecuteConfigCommands
from tools.gns3_topology_reader import GNS3TopologyTool
from tools.gns3_get_node_temp import GNS3TemplateTool
from tools.gns3_create_node import GNS3CreateNodeTool
from tools.gns3_create_link import GNS3LinkTool
from tools.gns3_start_node import GNS3StartNodeTool


# ReAct (Reasoning + Acting) prompt template for the agent
# This template guides the agent on how to reason about network automation tasks
react_prompt_template = """
You are a network automation assistant that can execute commands on network devices. 
You have access to tools that can help you.

Here are some examples of how to interpret user requests:

Example 1: Check interface status
Input: check R-1 and R-2 interfaces status
Thought: I need to check the interface status on R-1 and R-2. I should use the execute_device_commands tool.
Action: execute_device_commands
Action Input: {{"device_name": "R-1", "commands": ["show ip interface brief"]}}
Observation: [R-1 interface status output]
Action: execute_device_commands
Action Input: {{"device_name": "R-2", "commands": ["show ip interface brief"]}}
Observation: [R-2 interface status output]
Thought: I have the interface status for both R-1 and R-2. **I can now provide the final answer.**
**Final Answer: The interface status for R-1 and R-2 is as follows: [R-1 status], [R-2 status]**

Example 2: Check OSPF status
Input: check R-3 and R-4 ospf status
Thought: I need to check the OSPF status on R-3 and R-4. I should use the execute_device_commands tool.
Action: execute_device_commands
Action Input: {{"device_name": "R-3", "commands": ["show ip ospf neighbor", "show ip ospf interface brief"]}}
Observation: [R-3 OSPF status output]
Action: execute_device_commands
Action Input: {{"device_name": "R-4", "commands": ["show ip ospf neighbor", "show ip ospf interface brief"]}}
Observation: [R-4 OSPF status output]
Thought: I have the OSPF status for both R-3 and R-4. **I can now provide the final answer.**
**Final Answer: The OSPF status for R-3 and R-4 is as follows: [R-3 OSPF status], [R-4 OSPF status]**

Example 3: Configure a loopback interface (with pre-check)
Input: Configure a loopback interface on device R-3 with address 3.3.3.31/32.
Thought: First, I need to check the current interfaces to see if a loopback interface already exists. I should use the execute_device_commands tool.
Action: execute_device_commands
Action Input: {{"device_name": "R-3", "commands": ["show ip interface brief"]}}
Observation: [R-3 interface status output]
Thought: Now I need to analyze the output to see if a loopback interface already exists.
Thought: Based on the output, I can now decide whether to create a new loopback interface.
Action: execute_config_commands
Action Input: {{"device_name": "R-3", "config_commands": ["interface loopback0", "ip address 3.3.3.31 255.255.255.255", "exit"]}}
Observation: [Configuration commands executed successfully]
Thought: The configuration commands have been executed. Now I need to verify that the loopback interface was created successfully by checking the interface status again.
Action: execute_device_commands
Action Input: {{"device_name": "R-3", "commands": ["show ip interface brief", "show running-config interface loopback0"]}}
Observation: [Verification output showing loopback interface status and configuration]
Thought: I can see from the verification output that the loopback interface has been successfully created and configured with the correct IP address. **I can now provide the final answer.**
**Final Answer: A loopback interface has been successfully configured on R-3 with address 3.3.3.31/32. The configuration has been verified and the interface is now active.**

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action (should be a JSON string)
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer.
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}
"""

# Custom prompt template for the ReAct agent
custom_prompt = PromptTemplate(
    template=react_prompt_template,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
)

# Initialize the DeepSeek language model
# Using temperature=0 for deterministic responses in network automation tasks
llm = ChatDeepSeek(model="deepseek-chat", temperature=0, streaming=True)

# Define the available tools for the agent
# These tools provide capabilities for GNS3 topology management and network device operations
tools = [
    GNS3TemplateTool(),        # Get GNS3 node templates
    GNS3TopologyTool(),        # Read GNS3 topology information
    GNS3CreateNodeTool(),      # Create new nodes in GNS3
    GNS3LinkTool(),            # Create links between nodes
    GNS3StartNodeTool(),       # Start GNS3 nodes
    ExecuteDisplayCommands(),  # Execute show/display commands on network devices
    ExecuteConfigCommands()    # Execute configuration commands on network devices
]

@cl.on_chat_start
async def start():
    """Initialize AgentExecutor when chat starts"""
    # Create ReAct agent with custom prompt
    agent = create_react_agent(llm, tools, custom_prompt)
    
    # Create AgentExecutor with configuration to handle network automation tasks
    # Disable default verbose callback to avoid conflicts with Chainlit
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=False,  # Turn off verbose to prevent default callback interference
        handle_parsing_errors=True,  # Handle parsing errors gracefully
        max_iterations=50,  # Limit maximum iterations to prevent infinite loops
        return_intermediate_steps=True  # Return intermediate reasoning steps
    )
    
    # Store agent executor in user session for later use
    cl.user_session.set("agent_executor", agent_executor)
    
    # Send welcome message
    await cl.Message(content="Welcome to GNS3 Network Assistant! How can I help you with network automation tasks?").send()

@cl.on_message
async def main(message: cl.Message):
    """Process user messages and display reasoning process in real-time"""
    # Get agent executor from user session
    agent_executor = cl.user_session.get("agent_executor")
    user_input = message.content
    
    # Check for exit commands
    if user_input.lower() in ['quit', 'exit', '退出']:
        await cl.Message(content="Goodbye!").send()
        return

    try:
        # Create Chainlit's LangChain callback handler, compatible with Chainlit 2.8.1
        # This handler enables streaming of the agent's reasoning process
        callback_handler = cl.LangchainCallbackHandler(
            stream_final_answer=True,  # Enable streaming of final answers
            answer_prefix_tokens=["Final", "Answer"]  # Match prefix in the prompt template
        )
        
        # Use astream for streaming processing, relying on callback handler to render all output
        # The agent processes the user input and streams the reasoning steps
        async for _ in agent_executor.astream(
            {"input": user_input},
            config={"callbacks": [callback_handler]}
        ):
            # Rely on cl.LangchainCallbackHandler for rendering, no manual processing needed
            pass
        
    except Exception as e:
        # Error handling for any exceptions during agent execution
        await cl.Message(content=f"Error: {str(e)}").send()
