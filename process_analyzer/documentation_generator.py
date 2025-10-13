"""
Documentation Generator for Process Analysis Sessions

This module provides functionality to generate various formats of documentation
from captured learning session data.
"""

import json
from typing import Dict, Any, List


class DocumentationGenerator:
    """
    Generator for creating various documentation formats from learning session data.

    This class can generate:
    - Markdown reports for easy reading
    - Technical analysis documents for detailed study
    - Summary reports for quick overview
    """

    def __init__(self):
        """Initialize the documentation generator."""
        pass

    def _format_content_for_display(self, content: Any) -> str:
        """
        Format content for display in Markdown, properly handling newlines and special characters.

        Args:
            content (Any): Raw content to format

        Returns:
            str: Formatted content ready for Markdown display
        """
        if isinstance(content, (dict, list)):
            return json.dumps(content, indent=2, ensure_ascii=False)
        elif isinstance(content, str):
            # Handle escaped newlines and other special characters
            # Replace literal \n with actual newlines for display
            formatted = content.replace('\\n', '\n')

            # Handle other common escape sequences
            formatted = formatted.replace('\\t', '\t')
            formatted = formatted.replace('\\"', '"')
            formatted = formatted.replace("\\'", "'")

            return formatted
        else:
            return str(content)

    def _truncate_long_content(self, content: str, max_lines: int = 1000) -> str:
        """
        Truncate long content while preserving readability using line count control.

        Args:
            content (str): Content to truncate
            max_lines (int): Maximum number of lines before truncation

        Returns:
            str: Truncated content with ellipsis if needed
        """
        lines = content.split('\n')

        if len(lines) <= max_lines:
            return content

        # Keep the most important lines (first 80% and last 20% if very long)
        if len(lines) > max_lines * 1.5:
            keep_lines = lines[:int(max_lines * 0.8)] + ['...'] + lines[-int(max_lines * 0.2):]
            truncated_content = '\n'.join(keep_lines)
        else:
            truncated_content = '\n'.join(lines[:max_lines])

        return truncated_content + '\n... (content truncated)'

    def generate_technical_analysis(self, session_data: Dict[str, Any], output_path: str) -> None:
        """
        Generate a technical analysis document focusing on tool usage and inputs/outputs.

        Args:
            session_data (Dict[str, Any]): Complete session data
            output_path (str): Path to save the technical analysis file
        """
        content = self._build_technical_analysis_content(session_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_summary_report(self, session_data: Dict[str, Any], output_path: str) -> None:
        """
        Generate a summary report with key highlights.

        Args:
            session_data (Dict[str, Any]): Complete session data
            output_path (str): Path to save the summary file
        """
        content = self._build_summary_content(session_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _build_markdown_content(self, session_data: Dict[str, Any]) -> str:
        """Build comprehensive Markdown content."""
        content = f"""# GNS3 Copilot Learning Report

## Execution Overview
- **Session ID**: {session_data['session_id']}
- **User Input**: {session_data['user_input']}
- **Start Time**: {session_data['start_time']}
- **End Time**: {session_data['end_time']}
- **Execution Duration**: {session_data['metadata']['execution_duration']}
- **Total Steps**: {session_data['metadata']['total_steps']}
- **Tools Used**: {', '.join(session_data['metadata']['tools_used']) if session_data['metadata']['tools_used'] else 'None'}

## Detailed Execution Process

"""

        for step in session_data['reaction_steps']:
            step_num = step['step_number']
            step_type = step['step_type']
            timestamp = step['timestamp']

            if step_type == 'thought':
                content += f"### Step {step_num}: Thought Process\n\n"
                content += f"**Time**: {timestamp}\n\n"
                content += f"{step['content']}\n\n"

            elif step_type == 'action':
                content += f"### Step {step_num}: Execute Action\n\n"
                content += f"**Time**: {timestamp}\n\n"
                content += f"**Tool Used**: `{step['tool_name']}`\n\n"
                content += f"**Input Parameters**:\n```json\n{json.dumps(step['action_input'], indent=2, ensure_ascii=False)}\n```\n\n"

            elif step_type == 'observation':
                content += f"### Step {step_num}: Observation Result\n\n"
                content += f"**Time**: {timestamp}\n\n"
                if isinstance(step['content'], (dict, list)):
                    content += f"```json\n{json.dumps(step['content'], indent=2, ensure_ascii=False)}\n```\n\n"
                else:
                    # Format content with proper newline handling
                    formatted_content = self._format_content_for_display(step['content'])
                    # Truncate if too long
                    if len(formatted_content) > 2000:
                        formatted_content = self._truncate_long_content(formatted_content, 2000)
                    content += f"```\n{formatted_content}\n```\n\n"

        content += f"""## Final Answer

{session_data['final_answer']}

---

## Metadata

- **Session Number**: {session_data['metadata']['session_number']}
- **Execution Duration**: {session_data['metadata']['execution_duration']}
- **Tool Usage Statistics**:
"""

        for tool in session_data['metadata']['tools_used']:
            tool_count = sum(1 for step in session_data['reaction_steps']
                           if step['step_type'] == 'action' and step['tool_name'] == tool)
            content += f"  - `{tool}`: {tool_count} uses\n"

        content += "\n---\n*This report is automatically generated by GNS3 Copilot learning system*"

        return content

    def _build_technical_analysis_content(self, session_data: Dict[str, Any]) -> str:
        """Build technical analysis content focusing on tool details."""

        # Determine execution status and format it
        execution_status = session_data.get('execution_status', 'unknown')
        status_emoji = {
            'completed': '✅',
            'interrupted': '⚠️',
            'failed': '❌',
            'running': '🔄',
            'unknown': '❓'
        }.get(execution_status, '❓')

        status_text = {
            'completed': 'Completed Successfully',
            'interrupted': 'Interrupted',
            'failed': 'Failed',
            'running': 'Still Running',
            'unknown': 'Unknown Status'
        }.get(execution_status, 'Unknown Status')

        content = f"""# GNS3 Copilot Technical Analysis Report

## Execution Overview
- **User Input**: {session_data['user_input']}
- **Session ID**: {session_data['session_id']}
- **Execution Status**: {status_emoji} {status_text}
- **Start Time**: {session_data['start_time']}
"""

        # Add end time and interruption reason if available
        if session_data.get('end_time'):
            content += f"- **End Time**: {session_data['end_time']}\n"
        else:
            content += "- **End Time**: N/A\n"

        content += f"""- **Total Steps**: {session_data['metadata']['total_steps']}
- **Execution Duration**: {session_data['metadata']['execution_duration']}
"""

        # Add interruption reason if session was interrupted or failed
        if session_data.get('interruption_reason'):
            content += f"- **Interruption Reason**: {session_data['interruption_reason']}\n"

        content += "\n## Detailed Execution Process Analysis\n\n"

        # Analyze tool usage
        config_tools = []
        display_tools = []
        gns3_tools = []

        for step in session_data['reaction_steps']:
            if step['step_type'] == 'react_step':
                content += f"### Step {step['step_number']}: ReAct Execution Cycle\n\n"

                # Thought part
                if step.get('thought'):
                    content += f"**Thought Process**:\n{step['thought']}\n\n"

                # Action part
                tool_name = step.get('tool_name')
                if tool_name:
                    content += f"**Tool Used**: `{tool_name}`\n\n"

                    # Categorize tools
                    if 'config' in tool_name.lower():
                        config_tools.append(tool_name)
                    elif 'display' in tool_name.lower() or 'command' in tool_name.lower():
                        display_tools.append(tool_name)
                    elif 'gns3' in tool_name.lower():
                        gns3_tools.append(tool_name)

                # Action Input part
                action_input = step.get('action_input')
                if action_input is not None:
                    content += f"**Tool Input Parameters**:\n```json\n{json.dumps(action_input, indent=2, ensure_ascii=False)}\n```\n\n"

                    # Add specific analysis based on tool type
                    if tool_name and 'config' in tool_name.lower():
                        content += "**Configuration Tool Analysis**:\n"
                        if isinstance(action_input, list) and action_input:
                            for item in action_input:
                                if isinstance(item, dict) and 'device_name' in item:
                                    device_name = item.get('device_name', 'Unknown')
                                    commands = item.get('config_commands', item.get('commands', []))
                                    content += f"- Device `{device_name}`: {len(commands)} configuration commands\n"
                        content += "\n"

                # Error handling part
                if "parsing_error" in step:
                    content += f"**ReAct Parsing Error**:\n```\n{step['parsing_error']['error_message']}\n```\n\n"

                if "tool_error" in step:
                    content += f"**Tool Execution Error**:\n```\n{step['tool_error']['error_message']}\n```\n\n"

                # Observation part
                observation = step.get('observation')
                if observation is not None:
                    content += f"**Observation Result**:\n"

                    # Format observation based on type
                    if isinstance(observation, list):
                        content += "**Multi-Device Results**:\n"
                        for i, result in enumerate(observation):
                            if isinstance(result, dict) and 'device_name' in result:
                                device_name = result['device_name']
                                content += f"#### Device: {device_name}\n\n"
                                for key, value in result.items():
                                    if key != 'device_name':
                                        if isinstance(value, str):
                                            # Format and truncate very long output
                                            formatted_value = self._format_content_for_display(value)
                                            truncated_value = self._truncate_long_content(formatted_value)
                                            content += f"**{key}**:\n```\n{truncated_value}\n```\n\n"
                                        else:
                                            formatted_value = self._format_content_for_display(value)
                                            content += f"**{key}**:\n```\n{formatted_value}\n```\n\n"
                            else:
                                content += f"#### Result {i+1}:\n```json\n{json.dumps(result, indent=2, ensure_ascii=False)}\n```\n\n"
                    else:
                        if isinstance(observation, (dict, list)):
                            content += f"```json\n{json.dumps(observation, indent=2, ensure_ascii=False)}\n```\n\n"
                        else:
                            # Handle long text output with proper formatting
                            if isinstance(observation, str):
                                formatted_observation = self._format_content_for_display(observation)
                                content += f"```\n{formatted_observation}\n```\n\n"
                            else:
                                content += f"```\n{observation}\n```\n\n"

            # Legacy support for old step types
            elif step['step_type'] == 'thought':
                content += f"### Step {step['step_number']}: Thought Process\n\n"
                content += f"{step['content']}\n\n"

            elif step['step_type'] == 'action':
                tool_name = step['tool_name']
                content += f"### Step {step['step_number']}: Execute Action\n\n"
                content += f"**Tool Used**: `{tool_name}`\n\n"

                # Categorize tools
                if 'config' in tool_name.lower():
                    config_tools.append(tool_name)
                elif 'display' in tool_name.lower() or 'command' in tool_name.lower():
                    display_tools.append(tool_name)
                elif 'gns3' in tool_name.lower():
                    gns3_tools.append(tool_name)

                # Format and display input parameters
                action_input = step['action_input']
                content += f"**Tool Input Parameters**:\n```json\n{json.dumps(action_input, indent=2, ensure_ascii=False)}\n```\n\n"

            elif step['step_type'] == 'observation':
                content += f"### Step {step['step_number']}: Observation Result\n\n"

                # Format observation based on type
                observation = step['content']
                if isinstance(observation, (dict, list)):
                    content += f"```json\n{json.dumps(observation, indent=2, ensure_ascii=False)}\n```\n\n"
                else:
                    content += f"```\n{observation}\n```\n\n"

        # Tool usage statistics
        content += "## Tool Usage Statistics\n\n"
        content += f"- **Configuration Tool Usage Count**: {len(config_tools)} times\n"
        if config_tools:
            unique_config_tools = list(set(config_tools))
            content += f"  - Configuration tools used: {', '.join(unique_config_tools)}\n"

        content += f"- **Display Tool Usage Count**: {len(display_tools)} times\n"
        if display_tools:
            unique_display_tools = list(set(display_tools))
            content += f"  - Display tools used: {', '.join(unique_display_tools)}\n"

        content += f"- **GNS3 Tool Usage Count**: {len(gns3_tools)} times\n"
        if gns3_tools:
            unique_gns3_tools = list(set(gns3_tools))
            content += f"  - GNS3 tools used: {', '.join(unique_gns3_tools)}\n"

        content += f"\n## Final Answer\n\n{session_data['final_answer']}\n\n"
        content += "---\n*This technical analysis report is automatically generated by GNS3 Copilot learning system*"

        return content

    def _build_summary_content(self, session_data: Dict[str, Any]) -> str:
        """Build summary content with key highlights."""
        content = f"""# GNS3 Copilot Execution Summary

## Basic Information
- **Session ID**: {session_data['session_id']}
- **User Request**: {session_data['user_input']}
- **Execution Duration**: {session_data['metadata']['execution_duration']}
- **Total Steps**: {session_data['metadata']['total_steps']}

## Execution Flow Overview
"""

        # Create a simplified flow overview
        thought_count = sum(1 for step in session_data['reaction_steps'] if step['step_type'] == 'thought')
        action_count = sum(1 for step in session_data['reaction_steps'] if step['step_type'] == 'action')
        observation_count = sum(1 for step in session_data['reaction_steps'] if step['step_type'] == 'observation')

        content += f"- **Thought Steps**: {thought_count} times\n"
        content += f"- **Action Steps**: {action_count} times\n"
        content += f"- **Observation Steps**: {observation_count} times\n\n"

        # List tools used
        if session_data['metadata']['tools_used']:
            content += "## Tools Used\n\n"
            for tool in session_data['metadata']['tools_used']:
                tool_count = sum(1 for step in session_data['reaction_steps']
                               if step['step_type'] == 'action' and step['tool_name'] == tool)
                content += f"- `{tool}` ({tool_count} times)\n"
            content += "\n"

        # Key steps summary
        content += "## Key Steps Summary\n\n"
        for step in session_data['reaction_steps']:
            if step['step_type'] == 'action':
                tool_name = step['tool_name']
                content += f"1. **Tool Used**: `{tool_name}`\n"
                if isinstance(step['action_input'], list) and step['action_input']:
                    # Show key input details
                    first_item = step['action_input'][0]
                    if isinstance(first_item, dict):
                        if 'device_name' in first_item:
                            devices = [item.get('device_name', 'Unknown') for item in step['action_input'] if isinstance(item, dict)]
                            content += f"   - Target Devices: {', '.join(devices)}\n"
                        if 'commands' in first_item or 'config_commands' in first_item:
                            cmd_key = 'commands' if 'commands' in first_item else 'config_commands'
                            cmd_count = sum(len(item.get(cmd_key, [])) for item in step['action_input'] if isinstance(item, dict))
                            content += f"   - Command Count: {cmd_count}\n"
                content += "\n"

        content += f"""## Final Result

{session_data['final_answer']}

---

*This summary is automatically generated by GNS3 Copilot*
"""

        return content

    def generate_index_file(self, sessions: List[Dict[str, Any]], output_path: str) -> None:
        """
        Generate an index file listing all available sessions.

        Args:
            sessions (List[Dict[str, Any]]): List of session data
            output_path (str): Path to save the index file
        """
        content = "# GNS3 Copilot Learning Session Index\n\n"
        content += "This directory contains all learning session records.\n\n"
        content += "## Session List\n\n"
        content += "| Session ID | User Input | Start Time | Steps | Tools | File |\n"
        content += "|------------|------------|------------|-------|-------|------|\n"

        for session in sessions:
            session_id = session['session_id']
            user_input = session['user_input'][:50] + "..." if len(session['user_input']) > 50 else session['user_input']
            start_time = session['start_time'].split('T')[1][:8]  # Extract time part
            step_count = session['metadata']['total_steps']
            tools_count = len(session['metadata']['tools_used'])

            content += f"| {session_id} | {user_input} | {start_time} | {step_count} | {tools_count} | [View Details]({session_id}.md) |\n"

        content += "\n---\n*Index file automatically generated by GNS3 Copilot*"

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
