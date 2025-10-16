"""
LangChain Callback Handler for Process Analysis Documentation

This module provides a custom LangChain callback handler that integrates
with the process analysis documentation system to capture the complete execution
process of GNS3 Copilot, including proper error handling.
"""

import datetime
import logging
from typing import Any, Dict, List, Optional
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import AgentAction, AgentFinish, LLMResult
from .process_callback import LearningDocumentationCallback

# Set up logger for error handling
logger = logging.getLogger(__name__)


class LearningLangChainCallback(BaseCallbackHandler):
    """
    Custom LangChain callback handler for capturing execution process with proper error handling.

    This handler integrates with LangChain's callback system to automatically
    capture Thought/Action/Action Input/Observation/Final Answer steps
    during agent execution, while properly handling and categorizing errors.
    """

    def __init__(self, learning_callback: LearningDocumentationCallback):
        """
        Initialize the callback handler.

        Args:
            learning_callback: LearningDocumentationCallback instance
        """
        self.learning_callback = learning_callback
        self.session_started = False
        self.current_action = None  # Track current action for error handling
        self.latest_result = {}  # Store latest execution results including generated files
        self.files_generated = False  # Track if files have been generated for current session

    def on_chain_start(
        self,
        serialized: Dict[str, Any],
        inputs: Dict[str, Any],
        **kwargs: Any
    ) -> None:
        """Called when a chain starts running."""
        if not self.session_started and "input" in inputs:
            # Start a new learning documentation session
            user_input = inputs["input"]
            self.learning_callback.start_new_session(user_input)
            self.session_started = True
            self.files_generated = False  # Reset file generation flag for new session

    def on_agent_action(
        self,
        action: AgentAction,
        color: Optional[str] = None,  # pylint: disable=unused-argument
        **kwargs: Any
    ) -> Any:
        """Called when agent takes an action."""
        # Track current action for error handling
        self.current_action = action

        # Extract thought content from action.log
        thought_content = None
        if hasattr(action, 'log') and action.log:
            thought_content = self._extract_thought_from_log(action.log)

        # Record a complete ReAct step (Thought + Action + Action Input)
        self.learning_callback.record_complete_step(
            thought=thought_content,
            tool_name=action.tool,
            action_input=action.tool_input
        )

    def _extract_thought_from_log(self, log_content: str) -> Optional[str]:
        """Extract Thought content from action.log"""
        lines = log_content.split('\n')
        thought_lines = []
        in_thought = False

        for line in lines:
            stripped_line = line.strip()
            if stripped_line.startswith('Thought:'):
                in_thought = True
                thought_content = stripped_line.split(':', 1)[1].strip()
                if thought_content:
                    thought_lines.append(thought_content)
            elif in_thought:
                if stripped_line.startswith('Action:'):
                    break  # Thought ends
                if stripped_line:  # Ignore empty lines
                    thought_lines.append(stripped_line)

        return '\n'.join(thought_lines) if thought_lines else None

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,  # pylint: disable=unused-argument
        observation_prefix: Optional[str] = None,  # pylint: disable=unused-argument
        llm_prefix: Optional[str] = None,  # pylint: disable=unused-argument
        **kwargs: Any
    ) -> None:
        """Called when tool finishes running."""
        # Only add observation if we have a current action and output is not an error
        if self.current_action and not self._is_error_output(output):
            self.learning_callback.add_observation_to_current_step(output)
            self.current_action = None  # Reset after successful completion

    def on_agent_finish(
        self,
        finish: AgentFinish,
        color: Optional[str] = None,  # pylint: disable=unused-argument
        **kwargs: Any
    ) -> None:
        """Called when agent finishes."""
        # Prevent duplicate file generation
        if self.files_generated:
            logger.debug("Files already generated for this session, skipping")
            return

        # Record the final answer
        final_answer = finish.return_values.get("output", "")
        self.learning_callback.record_final_answer(final_answer)

        # Finalize the session and save to files
        session_data = self.learning_callback.finalize_session()
        if session_data:
            generated_files = self.learning_callback.save_session_to_file(session_data)
            logger.info("Learning documentation saved to: %s", generated_files)

            # Store generated files for later access by main program
            self.latest_result = {"generated_files": generated_files}
            self.files_generated = True  # Mark files as generated

        # Reset for next session
        self.session_started = False

    def on_llm_start(
        self,
        serialized: Dict[str, Any],
        prompts: List[str],
        **kwargs: Any
    ) -> None:
        """Called when LLM starts running."""

    def on_llm_end(
        self,
        response: LLMResult,
        **kwargs: Any
    ) -> None:
        """Called when LLM finishes running."""

    def on_llm_new_token(
        self,
        token: str,
        **kwargs: Any
    ) -> None:
        """Called on each new token from LLM."""

    def on_chain_end(
        self,
        outputs: Dict[str, Any],
        **kwargs: Any
    ) -> None:
        """Called when chain finishes running."""

    def on_chain_error(
        self,
        error: Exception,
        **kwargs: Any
    ) -> None:
        """Called when chain encounters an error."""
        # Handle ReAct parsing errors and other chain errors
        error_msg = str(error)

        # Check for interruption-related errors
        if self._is_interruption_error(error):
            self._handle_interruption(error)
        elif "Invalid Format: Missing 'Action:' after 'Thought:'" in error_msg:
            self._handle_react_parsing_error(error)
        else:
            self._record_general_error(error)
            # For other chain errors, mark session as failed
            self._handle_session_failure(error)

    def on_tool_error(
        self,
        error: Exception,
        **kwargs: Any
    ) -> None:
        """Called when tool encounters an error."""
        if self.current_action:
            self._record_tool_error(error)
            self.current_action = None  # Reset after error handling

        # Check if this is an interruption
        if self._is_interruption_error(error):
            self._handle_interruption(error)
        else:
            self._handle_session_failure(error)

    def on_llm_error(
        self,
        error: Exception,
        **kwargs: Any
    ) -> None:
        """Called when LLM encounters an error."""
        # Check for interruption-related errors
        if self._is_interruption_error(error):
            self._handle_interruption(error)
        else:
            self._record_general_error(error)
            self._handle_session_failure(error)

    def _is_error_output(self, output: str) -> bool:
        """Check if the output is an error message."""
        if not isinstance(output, str):
            return False
        error_patterns = [
            "Invalid Format: Missing 'Action:' after 'Thought:'",
            "Could not parse LLM output:",
            "Failed to parse action",
            "OutputParserException",
            "Error:",
            "Exception:"
        ]
        return any(pattern in output for pattern in error_patterns)

    def _handle_react_parsing_error(self, error: Exception):
        """Handle ReAct parsing errors specifically."""
        error_msg = str(error)

        _current_session = self.learning_callback.current_session
        # Record error information to the current step
        if _current_session and _current_session["reaction_steps"]:
            current_step = _current_session["reaction_steps"][-1]
            current_step["parsing_error"] = {
                "error_type": "ReActParsingError",
                "error_message": error_msg,
                "timestamp": datetime.datetime.now().isoformat()
            }

        # Log the error
        logger.error("ReAct parsing error: %s", error_msg)

    def _record_tool_error(self, error: Exception):
        """Record tool execution errors."""
        _current_session = self.learning_callback.current_session
        if _current_session and _current_session["reaction_steps"]:
            current_step = _current_session["reaction_steps"][-1]
            current_step["tool_error"] = {
                "error_type": type(error).__name__,
                "error_message": str(error),
                "timestamp": datetime.datetime.now().isoformat()
            }

        logger.error("Tool execution error: %s: %s", type(error).__name__, error)

    def _record_general_error(self, error: Exception):
        """Record general errors."""
        logger.error("General error in execution: %s: %s", type(error).__name__, error)

    def _is_interruption_error(self, error: Exception) -> bool:
        """Check if the error is related to interruption."""
        error_msg = str(error).lower()
        error_type = type(error).__name__.lower()

        interruption_patterns = [
            "keyboardinterrupt",
            "interrupted",
            "cancelled",
            "timeout",
            "connection aborted",
            "connection reset",
            "stream closed",
            "operation cancelled",
            "task was destroyed",
            "asyncio cancellederror"
        ]

        return (any(pattern in error_msg for pattern in interruption_patterns) or
                any(pattern in error_type for pattern in interruption_patterns))

    def _handle_interruption(self, error: Exception):
        """Handle interruption by performing emergency save."""
        logger.warning("Execution interrupted: %s: %s", type(error).__name__, error)

        # Perform emergency save
        generated_files = self.learning_callback.emergency_save(
            interruption_reason=f"{type(error).__name__}: {error}"
        )

        if generated_files:
            logger.info("Execution interrupted. Partial documentation saved to:%s", generated_files)
        else:
            logger.info("Execution interrupted. No active session to save.")

        # Reset session state
        self.session_started = False
        self.current_action = None

    def _handle_session_failure(self, error: Exception):
        """Handle session failure by marking it as failed."""
        logger.error("Session failed: %s: %s", type(error).__name__, error)

        # Mark session as failed
        generated_files = self.learning_callback.mark_session_failed(
            failure_reason=f"{type(error).__name__}: {error}"
        )

        if generated_files:
            logger.info("Session failed. Error documentation saved to: %s", generated_files)

        # Reset session state
        self.session_started = False
        self.current_action = None
