"""
GNS3 Network Automation Assistant

This module implements a conversational AI assistant for GNS3 network automation tasks.
It uses Chainlit for the user interface, LangChain for agent orchestration, and DeepSeek LLM
for natural language processing. The assistant can execute network commands, configure devices,
and manage GNS3 topology operations.
"""

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from tools_v2 import GNS3TopologyTool
from tools_v2 import GNS3TemplateTool
from tools_v2 import GNS3CreateNodeTool
from tools_v2 import GNS3LinkTool
from tools_v2 import GNS3StartNodeTool
from tools_v2 import ExecuteMultipleDeviceConfigCommands
from tools_v2 import ExecuteMultipleDeviceCommands
from tools_v2 import VPCSCommands
from log_config import setup_logger
from prompts.react_prompt import SYSTEM_PROMPT

load_dotenv()

# Set up logger for GNS3 Copilot
logger = setup_logger("gns3_copilot", log_file="log/gns3_copilot.log")

# Initialize the DeepSeek language model
llm = ChatDeepSeek(
    model="deepseek-chat",
    temperature=0,
    streaming=True,
    timeout=60,
    max_retries=3,
    request_timeout=30
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
    VPCSCommands(),                    # Execute VPCS commands on multiple devices(not thread)
]

# Log application startup
logger.info("GNS3 Copilot application starting up")
logger.debug("Available tools: %s", [tool.__class__.__name__ for tool in tools])


# Create the agent using the new LangChain v1.0 create_agent function
agent = create_agent(
    llm,
    tools=tools,
    system_prompt=SYSTEM_PROMPT
)

logger.info("GNS3 Copilot agent created successfully with new LangChain v1.0 architecture")
