"""
Process Analysis Callback Handler

This module provides a callback handler to capture the complete execution process
of GNS3 Copilot, including Thought/Action/Action Input/Observation/Final Answer.
"""

import json
import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from .documentation_generator import DocumentationGenerator


class LearningDocumentationCallback:
    """
    Callback handler for capturing complete execution process for learning purposes.

    This class captures the full ReAct framework execution process:
    - Thought: AI reasoning process
    - Action: Tool selection
    - Action Input: Tool parameters
    - Observation: Tool execution results
    - Final Answer: Final response to user
    """

    def __init__(self, output_dir: str = "process_docs"):
        """
        Initialize the learning documentation callback.

        Args:
            output_dir (str): Directory to save learning documents
        """
        self.output_dir = Path(output_dir)
        self.current_session: Optional[Dict[str, Any]] = None
        self.session_counter = 0

        # Ensure output directory exists
        self.output_dir.mkdir(exist_ok=True)

    def start_new_session(self, user_input: str, session_id: Optional[str] = None) -> str:
        """
        Start a new documentation session.

        Args:
            user_input (str): User's input/command
            session_id (str, optional): Custom session ID

        Returns:
            str: Session ID
        """
        self.session_counter += 1

        if session_id is None:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            session_id = f"session_{timestamp}_{self.session_counter}"

        self.current_session = {
            "session_id": session_id,
            "user_input": user_input,
            "start_time": datetime.datetime.now().isoformat(),
            "reaction_steps": [],
            "final_answer": "",
            "end_time": "",
            "execution_status": "running",  # running, completed, interrupted, failed
            "interruption_reason": None,
            "metadata": {
                "session_number": self.session_counter,
                "total_steps": 0,
                "tools_used": [],
                "execution_duration": ""
            }
        }

        return session_id

    def record_complete_step(self, thought: str = None, tool_name: str = None,
                             action_input: Any = None) -> bool:
        """
        Record a complete ReAct step (Thought + Action + Action Input).

        Args:
            thought (str, optional): AI's reasoning/thinking process
            tool_name (str, optional): Name of the tool being used
            action_input (Any, optional): Input parameters for the tool

        Returns:
            bool: True if recorded successfully
        """
        if not self.current_session:
            return False

        # Record tool usage
        if tool_name and tool_name not in self.current_session["metadata"]["tools_used"]:
            self.current_session["metadata"]["tools_used"].append(tool_name)

        step = {
            "step_type": "react_step",
            "thought": thought,
            "tool_name": tool_name,
            "action_input": self._format_input(action_input) if action_input is not None else None,
            "observation": None,  # Will be added later
            "timestamp": datetime.datetime.now().isoformat(),
            "step_number": len(self.current_session["reaction_steps"]) + 1
        }

        self.current_session["reaction_steps"].append(step)
        return True

    def add_observation_to_current_step(self, observation: Any) -> bool:
        """
        Add observation to the most recent step.

        Args:
            observation (Any): Result/output from tool execution

        Returns:
            bool: True if recorded successfully
        """
        if not self.current_session or not self.current_session["reaction_steps"]:
            return False

        # Add observation to the last step
        current_step = self.current_session["reaction_steps"][-1]
        current_step["observation"] = self._format_observation(observation)
        current_step["timestamp"] = datetime.datetime.now().isoformat()  # Update timestamp

        return True

    # Keep old methods for backward compatibility
    def record_thought(self, thought: str) -> bool:
        """Legacy method - use record_complete_step instead."""
        return self.record_complete_step(thought=thought)

    def record_action(self, tool_name: str, action_input: Any) -> bool:
        """Legacy method - use record_complete_step instead."""
        return self.record_complete_step(tool_name=tool_name, action_input=action_input)

    def record_observation(self, observation: Any) -> bool:
        """Legacy method - use add_observation_to_current_step instead."""
        return self.add_observation_to_current_step(observation)

    def record_final_answer(self, final_answer: str) -> bool:
        """
        Record the Final Answer and complete the session.

        Args:
            final_answer (str): Final answer/response to user

        Returns:
            bool: True if recorded successfully
        """
        if not self.current_session:
            return False

        self.current_session["final_answer"] = final_answer
        self.current_session["end_time"] = datetime.datetime.now().isoformat()
        self.current_session["execution_status"] = "completed"

        # Calculate execution duration
        start_time = datetime.datetime.fromisoformat(self.current_session["start_time"])
        end_time = datetime.datetime.fromisoformat(self.current_session["end_time"])
        duration = end_time - start_time
        self.current_session["metadata"]["execution_duration"] = str(duration)
        self.current_session["metadata"]["total_steps"] = len(
            self.current_session["reaction_steps"]
            )

        return True

    def finalize_session(self) -> Optional[Dict[str, Any]]:
        """
        Finalize the current session and return the complete data.

        Returns:
            Optional[Dict[str, Any]]: Complete session data or None if no active session
        """
        if not self.current_session:
            return None

        session_data = self.current_session.copy()
        self.current_session = None

        return session_data

    def get_current_session(self) -> Optional[Dict[str, Any]]:
        """
        Get the current session data without finalizing it.

        Returns:
            Optional[Dict[str, Any]]: Current session data or None if no active session
        """
        return self.current_session.copy() if self.current_session else None

    def _format_input(self, action_input: Any) -> Any:
        """
        Format action input for consistent storage.

        Args:
            action_input (Any): Raw action input

        Returns:
            Any: Formatted action input
        """
        if isinstance(action_input, str):
            # Try to parse as JSON
            try:
                return json.loads(action_input)
            except Exception:  # pylint: disable=broad-except
                return action_input
        elif isinstance(action_input, (dict, list)):
            return action_input
        else:
            return str(action_input)

    def _format_observation(self, observation: Any) -> Any:
        """
        Format observation for consistent storage.

        Args:
            observation (Any): Raw observation

        Returns:
            Any: Formatted observation
        """
        if isinstance(observation, str):
            # Try to parse as JSON
            try:
                return json.loads(observation)
            except Exception:  # pylint: disable=broad-except
                return observation
        elif isinstance(observation, (dict, list)):
            return observation
        else:
            return str(observation)

    def save_session_to_file(self, session_data: Dict[str, Any]) -> List[str]:
        """
        Save session data to files in various formats.

        Args:
            session_data (Dict[str, Any]): Complete session data

        Returns:
            List[str]: List of generated file paths
        """
        session_id = session_data["session_id"]
        generated_files = []

        doc_gen = DocumentationGenerator()

        # Generate only technical analysis
        tech_file = self.output_dir / f"{session_id}_technical.md"
        doc_gen.generate_technical_analysis(session_data, str(tech_file))
        generated_files.append(str(tech_file))

        return generated_files

    def emergency_save(
        self,
        interruption_reason: str = "Unknown interruption"
        ) -> Optional[List[str]]:
        """
        Emergency save the current session when execution is interrupted.

        Args:
            interruption_reason (str): Reason for the interruption

        Returns:
            Optional[List[str]]: List of generated file paths or None if no active session
        """
        if not self.current_session:
            return None

        # Set interruption information
        self.current_session["end_time"] = datetime.datetime.now().isoformat()
        self.current_session["execution_status"] = "interrupted"
        self.current_session["interruption_reason"] = interruption_reason

        # Calculate execution duration up to interruption
        start_time = datetime.datetime.fromisoformat(self.current_session["start_time"])
        end_time = datetime.datetime.fromisoformat(self.current_session["end_time"])
        duration = end_time - start_time
        self.current_session["metadata"]["execution_duration"] = str(duration)
        self.current_session["metadata"]["total_steps"] = len(
            self.current_session["reaction_steps"]
            )

        # Save the interrupted session
        session_data = self.current_session.copy()
        generated_files = self.save_session_to_file(session_data)

        # Clear current session
        self.current_session = None

        return generated_files

    def mark_session_failed(self, failure_reason: str = "Unknown error") -> Optional[List[str]]:
        """
        Mark the current session as failed and save it.

        Args:
            failure_reason (str): Reason for the failure

        Returns:
            Optional[List[str]]: List of generated file paths or None if no active session
        """
        if not self.current_session:
            return None

        # Set failure information
        self.current_session["end_time"] = datetime.datetime.now().isoformat()
        self.current_session["execution_status"] = "failed"
        self.current_session["interruption_reason"] = failure_reason

        # Calculate execution duration up to failure
        start_time = datetime.datetime.fromisoformat(self.current_session["start_time"])
        end_time = datetime.datetime.fromisoformat(self.current_session["end_time"])
        duration = end_time - start_time
        self.current_session["metadata"]["execution_duration"] = str(duration)
        self.current_session["metadata"]["total_steps"] = len(
            self.current_session["reaction_steps"]
            )

        # Save the failed session
        session_data = self.current_session.copy()
        generated_files = self.save_session_to_file(session_data)

        # Clear current session
        self.current_session = None

        return generated_files

    def get_session_summary(self) -> Optional[Dict[str, Any]]:
        """
        Get a summary of the current session.

        Returns:
            Optional[Dict[str, Any]]: Session summary or None if no active session
        """
        if not self.current_session:
            return None

        return {
            "session_id": self.current_session["session_id"],
            "user_input": self.current_session["user_input"],
            "current_step_count": len(self.current_session["reaction_steps"]),
            "tools_used": self.current_session["metadata"]["tools_used"],
            "start_time": self.current_session["start_time"],
            "execution_status": self.current_session["execution_status"],
            "is_completed": self.current_session["execution_status"] == "completed"
        }
