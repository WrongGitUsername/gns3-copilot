"""
GNS3 Network Automation Assistant

This module implements an AI-powered assistant for GNS3 network automation and management.
It uses LangChain for agent orchestration and DeepSeek LLM for natural language processing.
The assistant provides comprehensive GNS3 topology management capabilities including:
- Reading and analyzing GNS3 project topologies
- Creating and managing network nodes and links
- Executing network configuration and display commands on multiple devices
- Managing VPCS (Virtual PC Simulator) commands
- Starting and controlling GNS3 nodes

The assistant integrates with various tools to provide a complete network automation
solution for GNS3 environments.
"""
import sqlite3
import operator
from typing import Literal
from typing_extensions import TypedDict, Annotated
from dotenv import load_dotenv
from langchain.messages import AnyMessage, SystemMessage, ToolMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.sqlite import SqliteSaver
from gns3_client import GNS3TopologyTool
from tools_v2 import GNS3TemplateTool
from tools_v2 import GNS3CreateNodeTool
from tools_v2 import GNS3LinkTool
from tools_v2 import GNS3StartNodeTool
from tools_v2 import ExecuteMultipleDeviceConfigCommands
from tools_v2 import ExecuteMultipleDeviceCommands
from tools_v2 import VPCSMultiCommands
from log_config import setup_logger
from prompts.react_prompt import SYSTEM_PROMPT

load_dotenv()

# Set up logger for GNS3 Copilot
logger = setup_logger("gns3_copilot", log_file="log/gns3_copilot.log")

base_model = init_chat_model(
    model="deepseek-chat",
    temperature=0
)

assist_model = init_chat_model(
    model="google_genai:gemini-2.5-flash",
    temperature=0
)

# Define the available tools for the agent
tools = [
    GNS3TemplateTool(),                # Get GNS3 node templates
    GNS3TopologyTool(),                # Read GNS3 topology information
    GNS3CreateNodeTool(),              # Create new nodes in GNS3
    GNS3LinkTool(),                    # Create links between nodes
    GNS3StartNodeTool(),               # Start GNS3 nodes
    ExecuteMultipleDeviceCommands(),   # Execute show/display commands on multiple devices
    ExecuteMultipleDeviceConfigCommands(),  # Execute configuration commands on multiple devices
    VPCSMultiCommands(),                    # Execute VPCS commands on multiple devices
]
# Augment the LLM with tools
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = base_model.bind_tools(tools)

# Log application startup
logger.info("GNS3 Copilot application starting up")
logger.debug("Available tools: %s", [tool.__class__.__name__ for tool in tools])

# Define state
class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    llm_calls: int

# Define model node
def llm_call(state: dict):
    """LLM decides whether to call a tool or not"""

    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(
                        content=SYSTEM_PROMPT
                    )
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }

# Define tool node
def tool_node(state: dict):
    """Performs the tool call"""

    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        observation = tool.invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id=tool_call["id"]))
    return {"messages": result}

# Define end logic
def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    """Decide if we should continue the loop or stop based upon whether the LLM made a tool call"""

    messages = state["messages"]
    last_message = messages[-1]

    # If the LLM makes a tool call, then perform an action
    if last_message.tool_calls:
        return "tool_node"

    # Otherwise, we stop (reply to the user)
    return END

# Build and compile the agent
# Build workflow
agent_builder = StateGraph(MessagesState)

# Add nodes
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)

# Add edges to connect nodes
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
agent_builder.add_edge("tool_node", "llm_call")

# Add checkpointing
conn = sqlite3.connect("gns3_checkpoint.db", check_same_thread=False)
memory = SqliteSaver(conn=conn)

# Compile the agent
agent = agent_builder.compile(checkpointer=memory)
