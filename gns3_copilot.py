"""
GNS3 Network Automation Assistant

This module implements a conversational AI assistant for GNS3 network automation tasks.
It uses Chainlit for the user interface, LangChain for agent orchestration, and DeepSeek LLM
for natural language processing. The assistant can execute network commands, configure devices,
and manage GNS3 topology operations.
"""

import asyncio
import chainlit as cl
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain_deepseek import ChatDeepSeek
from tools.display_tools_nornir import ExecuteMultipleDeviceCommands
from tools.config_tools_nornir import ExecuteMultipleDeviceConfigCommands
from tools.gns3_topology_reader import GNS3TopologyTool
from tools.gns3_get_node_temp import GNS3TemplateTool
from tools.gns3_create_node import GNS3CreateNodeTool
from tools.gns3_create_link import GNS3LinkTool
from tools.gns3_start_node import GNS3StartNodeTool
from tools.logging_config import setup_logger
from prompts.react_prompt import REACT_PROMPT_TEMPLATE

load_dotenv()

# Set up logger for GNS3 Copilot
logger = setup_logger("gns3_copilot", log_file="log/gns3_copilot.log")

# Initialize the DeepSeek language model
llm = ChatDeepSeek(model="deepseek-chat", temperature=0, streaming=True)

# Define the available tools for the agent
tools = [
    GNS3TemplateTool(),                # Get GNS3 node templates
    GNS3TopologyTool(),                # Read GNS3 topology information
    GNS3CreateNodeTool(),              # Create new nodes in GNS3
    GNS3LinkTool(),                    # Create links between nodes
    GNS3StartNodeTool(),               # Start GNS3 nodes
    ExecuteMultipleDeviceCommands(),   # Execute show/display commands on multiple devices
    ExecuteMultipleDeviceConfigCommands(),  # Execute configuration commands on multiple devices
]

# Log application startup
logger.info("GNS3 Copilot application starting up")
logger.debug("Available tools: %s", [tool.__class__.__name__ for tool in tools])

# Custom prompt template for the ReAct agent
custom_prompt = PromptTemplate(
    template=REACT_PROMPT_TEMPLATE,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
)

@cl.on_stop
async def on_stop():
    """Handle stop event when user clicks stop button"""
    logger.info("User clicked stop button, cancelling agent execution")

    # Set stop flag in user session
    cl.user_session.set("stop_requested", True)

    logger.debug("Stop flag set in user session")

@cl.on_chat_start
async def start():
    """Initialize AgentExecutor when chat starts"""
    logger.info("GNS3 Copilot session started")

    try:
        # Initialize stop flag
        cl.user_session.set("stop_requested", False)
        logger.debug("Stop flag initialized to False")

        # Create ReAct agent with custom prompt
        logger.debug("Creating ReAct agent with custom prompt")
        agent = create_react_agent(llm, tools, custom_prompt)

        # Create AgentExecutor with configuration to handle network automation tasks
        logger.debug("Creating AgentExecutor with configuration")
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=50,
            return_intermediate_steps=True  # Return intermediate reasoning steps
        )

        # Store agent executor in user session for later use
        cl.user_session.set("agent_executor", agent_executor)
        logger.info("AgentExecutor created and stored in session")

        # Send welcome message
        await cl.Message(
            content="Welcome to GNS3 Network Assistant! How can I help you with "
                    "network automation tasks?"
        ).send()
        logger.debug("Welcome message sent to user")

    except (ImportError, ConnectionError, RuntimeError, ValueError) as e:
        logger.error("Error during session start: %s", str(e), exc_info=True)
        await cl.Message(content=f"Failed to initialize session: {str(e)}").send()

@cl.on_message
async def main(message: cl.Message):
    """Process user messages and display reasoning process in real-time"""
    # Get agent executor from user session
    agent_executor = cl.user_session.get("agent_executor")
    user_input = message.content

    if len(user_input) > 100:
        logger.info("Received user message: %s...", user_input[:100])
    else:
        logger.info("Received user message: %s", user_input)

    # Check for exit commands
    if user_input.lower() in ['quit', 'exit', '退出']:
        logger.info("User requested to exit the session")
        await cl.Message(content="Goodbye!").send()
        return

    # Reset stop flag for new message
    cl.user_session.set("stop_requested", False)
    logger.debug("Stop flag reset for new message")

    try:
        # Create Chainlit's LangChain callback handler
        logger.debug("Creating LangChain callback handler")
        callback_handler = cl.LangchainCallbackHandler(
            stream_final_answer=True,
            answer_prefix_tokens=["Final", "Answer"]
        )

        # Use astream for streaming processing with cancellation support
        logger.debug("Starting agent execution stream")
        try:
            async for _ in agent_executor.astream(
                {"input": user_input},
                config={"callbacks": [callback_handler]}
            ):
                # Check if stop was requested
                if cl.user_session.get("stop_requested", False):
                    logger.info("Agent execution cancelled by user")
                    await cl.Message(content="⏹️ Execution stopped by user.").send()
                    break

                # Rely on cl.LangchainCallbackHandler for rendering, no manual processing needed
            else:
                # This runs only if the loop wasn't broken (no cancellation)
                logger.info("Agent execution completed successfully")

        except asyncio.CancelledError:
            logger.info("Agent execution was cancelled")
            # Don't send additional message here since Chainlit already shows "Task manual stopped."

    except (RuntimeError, ValueError, KeyError) as e:
        # Error handling for common exceptions during agent execution
        logger.warning("Agent execution error: %s", str(e))
        await cl.Message(content=f"Error: {str(e)}").send()
    except (AttributeError, TypeError, OSError) as e:
        # Catch-all for other specific unexpected exceptions
        logger.error("Unexpected error during message processing: %s", str(e), exc_info=True)
        await cl.Message(content=f"Unexpected error: {str(e)}").send()
