"""
GNS3 Network Automation Assistant

This module implements a conversational AI assistant for GNS3 network automation tasks.
It uses Chainlit for the user interface, LangChain for agent orchestration, and DeepSeek LLM
for natural language processing. The assistant can execute network commands, configure devices,
and manage GNS3 topology operations.
"""

import asyncio
import os
from typing import Optional
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
from process_analyzer import LearningDocumentationCallback
from process_analyzer.langchain_callback import LearningLangChainCallback

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


async def _send_report_file(file_path: str):
    """
    Send technical report file to Chainlit chat window.
    
    Args:
        file_path (str): Path to the report file to send
    """
    try:
        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_name)[1].lower()

        # Get FastAPI configuration from environment variables
        fastapi_host = os.getenv("FASTAPI_HOST", "localhost")
        fastapi_port = os.getenv("FASTAPI_PORT", "8001")

        if file_extension == '.html':
            # For HTML files, send URL link to FastAPI static service
            file_url = f"http://{fastapi_host}:{fastapi_port}/reports/{file_name}"

            await cl.Message(
                content=f"**Report**: [View in Browser]({file_url})",
            ).send()
            logger.info("Successfully sent HTML report URL: %s", file_url)

        else:
            # For non-HTML files (e.g., Markdown), send as file attachment
            with open(file_path, 'rb') as file:
                file_content = file.read()

            mime_type = "text/markdown" if file_extension == '.md' else "text/plain"

            await cl.Message(
                content="**Report**: Download file below:",
                elements=[
                    cl.File(
                        name=file_name,
                        content=file_content,
                        mime=mime_type,
                        display="inline"
                    )
                ],
            ).send()
            logger.info("Successfully sent report file: %s", file_path)

    except (OSError, IOError) as e:
        logger.error("Failed to send report file %s: %s", file_path, e)
        await cl.Message(
            content="**Error**: Failed to send report file: "
                    f"{os.path.basename(file_path)}.\n\n"
                    "Please check local directory `reports/` manually.",
        ).send()

@cl.password_auth_callback
async def authen_callback(username: str, password: str) -> Optional[cl.User]:
    """
    Authenticate user credentials and return user object.
    Args:
        username (str): Username
        password (str): Password
    Returns:
        Optional[cl.User]: User object if authentication succeeds, None otherwise
    """
    if (username, password) == ("admin", "admin"):
        return cl.User(
            identifier = "admin",
            metadata = {"role": "admin", "provider": "credentials"}
        )

    return None

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

        # Initialize process analyzer callback
        learning_cb = LearningDocumentationCallback(output_dir="reports")
        cl.user_session.set("learning_callback", learning_cb)
        logger.debug("Process analyzer callback initialized")

        # Create ReAct agent with custom prompt
        logger.debug("Creating ReAct agent with custom prompt")
        agent = create_react_agent(llm, tools, custom_prompt)

        # Create AgentExecutor with configuration to handle network automation tasks
        logger.debug("Creating AgentExecutor with configuration")
        agent_executor = AgentExecutor(
            agent=agent,
            tools=tools,
            verbose=False,
            handle_parsing_errors=True,
            max_iterations=50,
            return_intermediate_steps=True  # Return intermediate reasoning steps
        )

        # Store agent executor in user session for later use
        cl.user_session.set("agent_executor", agent_executor)
        logger.info("AgentExecutor created and stored in session")

        # Send welcome message
        app_user = cl.user_session.get("user")

        await cl.Message(
            content=f"Hello {app_user.identifier}! "
            "Welcome to GNS3 Network Assistant! How can I help you with "
            "network automation tasks?\n\n"
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
    if user_input.lower() in ['quit', 'exit']:
        logger.info("User requested to exit the session")
        await cl.Message(content="Goodbye!").send()
        return

    # Reset stop flag for new message
    cl.user_session.set("stop_requested", False)
    logger.debug("Stop flag reset for new message")

    try:
        # Get learning callback from session
        learning_cb = cl.user_session.get("learning_callback")

        # Create callback handlers list
        callbacks = []

        # Add Chainlit's LangChain callback handler
        logger.debug("Creating LangChain callback handler")
        callback_handler = cl.LangchainCallbackHandler(
            stream_final_answer=True,
            answer_prefix_tokens=["Final", "Answer"]
        )
        callbacks.append(callback_handler)

        # Initialize learning callback handler variable
        learning_callback_handler = None

        # Add learning documentation callback if available
        if learning_cb:
            learning_callback_handler = LearningLangChainCallback(learning_cb)
            callbacks.append(learning_callback_handler)
            logger.debug("Learning documentation callback added")

        # Use astream for streaming processing with cancellation support
        logger.debug("Starting agent execution stream")
        try:
            async for _ in agent_executor.astream(
                {"input": user_input},
                config={"callbacks": callbacks}
            ):
                # Check if stop was requested
                if cl.user_session.get("stop_requested", False):
                    logger.info("Agent execution cancelled by user")
                    await cl.Message(content="Execution stopped by user.").send()
                    break

                # Rely on cl.LangchainCallbackHandler for rendering, no manual processing needed
            else:
                # This runs only if the loop wasn't broken (no cancellation)
                logger.info("Agent execution completed successfully")

        except asyncio.CancelledError:
            logger.info("Agent execution was cancelled")
            # Don't send additional message here since Chainlit already shows "Task manual stopped."

        # Send generated report files after execution (regardless of success/failure)
        if learning_cb and learning_callback_handler and hasattr(
            learning_callback_handler, 'latest_result'
            ):
            generated_files = learning_callback_handler.latest_result.get('generated_files', [])
            if generated_files:
                logger.info("Sending %d report files to chat", len(generated_files))
                for file_path in generated_files:
                    await _send_report_file(file_path)
            else:
                logger.debug("No report files generated for this session")

    except (RuntimeError, ValueError, KeyError) as e:
        # Error handling for common exceptions during agent execution
        logger.warning("Agent execution error: %s", str(e))
        await cl.Message(content=f"Error: {str(e)}").send()
    except (AttributeError, TypeError, OSError) as e:
        # Catch-all for other specific unexpected exceptions
        logger.error("Unexpected error during message processing: %s", str(e), exc_info=True)
        await cl.Message(content=f"Unexpected error: {str(e)}").send()
