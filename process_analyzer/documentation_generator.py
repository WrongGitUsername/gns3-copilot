"""
Documentation Generator for Process Analysis Sessions

This module provides functionality to generate various formats of
documentation from captured learning session data.
"""

import json
from typing import Dict, Any, List


class DocumentationGenerator:
    """
    Generator for creating various documentation formats from learning 
    session data.

    This class can generate:
    - Markdown reports for easy reading
    - Technical analysis documents for detailed study
    - Summary reports for quick overview
    """

    def __init__(self) -> None:
        """Initialize the documentation generator."""

    def _format_content_for_display(self, content: Any) -> str:
        """
        Format content for display in Markdown, handling newlines and
        special characters properly.

        Args:
            content: Raw content to format

        Returns:
            Formatted content ready for Markdown display
        """
        if isinstance(content, (dict, list)):
            return json.dumps(content, indent=2, ensure_ascii=False)

        if isinstance(content, str):
            # Handle escaped newlines and other special characters
            formatted = content.replace('\\n', '\n')
            formatted = formatted.replace('\\t', '\t')
            formatted = formatted.replace('\\"', '"')
            formatted = formatted.replace("\\'", "'")
            return formatted

        return str(content)

    def _truncate_long_content(
        self,
        content: str,
        max_lines: int = 1000
    ) -> str:
        """
        Truncate long content while preserving readability using line 
        count control.

        Args:
            content: Content to truncate
            max_lines: Maximum number of lines before truncation

        Returns:
            Truncated content with ellipsis if needed
        """
        lines = content.split('\n')

        if len(lines) <= max_lines:
            return content

        # Keep first 80% and last 20% if very long
        if len(lines) > max_lines * 1.5:
            keep_lines = (
                lines[:int(max_lines * 0.8)]
                + ['...']
                + lines[-int(max_lines * 0.2):]
            )
            truncated_content = '\n'.join(keep_lines)
        else:
            truncated_content = '\n'.join(lines[:max_lines])

        return f"{truncated_content}\n... (content truncated)"

    def _format_json_block(self, data: Any) -> str:
        """Format JSON data as a Markdown code block."""
        json_str = json.dumps(data, indent=2, ensure_ascii=False)
        return f"```{json_str}\n```"

    def _format_step_header(self, step_num: int, step_type: str) -> str:
        """Format step header for Markdown."""
        type_mapping = {
            'thought': 'Thought Process',
            'action': 'Execute Action', 
            'observation': 'Observation Result'
        }
        step_title = type_mapping.get(step_type, 'Unknown Step')
        return f"### Step {step_num}: {step_title}\n\n"

    def generate_technical_analysis(
        self,
        session_data: Dict[str, Any],
        output_path: str
    ) -> None:
        """
        Generate technical analysis document focusing on tool usage and 
        inputs/outputs.

        Args:
            session_data: Complete session data
            output_path: Path to save the technical analysis file
        """
        content = self._build_technical_analysis_content(session_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def generate_summary_report(
        self,
        session_data: Dict[str, Any],
        output_path: str
    ) -> None:
        """
        Generate summary report with key highlights.

        Args:
            session_data: Complete session data
            output_path: Path to save the summary file
        """
        content = self._build_summary_content(session_data)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    def _build_markdown_content(self, session_data: Dict[str, Any]) -> str:
        """Build comprehensive Markdown content using efficient string ops."""
        parts = [
            self._build_execution_overview(session_data),
            "## Detailed Execution Process\n\n"
        ]

        for step in session_data['reaction_steps']:
            parts.append(self._format_step_block(step))

        parts.extend([
            self._build_final_answer_section(session_data),
            self._build_tool_statistics(session_data)
        ])

        return ''.join(parts)

    def _build_execution_overview(self, session_data: Dict[str, Any]) -> str:
        """Build execution overview section."""
        tools_used = (
            ', '.join(session_data['metadata']['tools_used'])
            if session_data['metadata']['tools_used']
            else 'None'
        )

        return f"""# GNS3 Copilot Learning Report

## Execution Overview
- **Session ID**: {session_data['session_id']}
- **User Input**: {session_data['user_input']}
- **Start Time**: {session_data['start_time']}
- **End Time**: {session_data['end_time']}
- **Execution Duration**: {session_data['metadata']['execution_duration']}
- **Total Steps**: {session_data['metadata']['total_steps']}
- **Tools Used**: {tools_used}

"""

    def _format_step_block(self, step: Dict[str, Any]) -> str:
        """Format individual step as Markdown block."""
        step_num = step['step_number']
        step_type = step['step_type']
        timestamp = step['timestamp']

        if step_type == 'thought':
            return (
                self._format_step_header(step_num, step_type) +
                f"**Time**: {timestamp}\n\n" +
                f"{step['content']}\n\n"
            )

        if step_type == 'action':
            return (
                self._format_step_header(step_num, step_type) +
                f"**Time**: {timestamp}\n\n" +
                f"**Tool Used**: `{step['tool_name']}`\n\n" +
                "**Input Parameters**:\n" +
                self._format_json_block(step['action_input']) +
                "\n"
            )

        if step_type == 'observation':
            content = self._format_observation_content(step['content'])
            return (
                self._format_step_header(step_num, step_type) +
                f"**Time**: {timestamp}\n\n" +
                f"{content}"
            )

        return ""

    def _format_observation_content(self, content: Any) -> str:
        """Format observation content for display."""
        if isinstance(content, (dict, list)):
            return f"{self._format_json_block(content)}\n\n"

        formatted = self._format_content_for_display(content)
        if len(formatted) > 2000:
            formatted = self._truncate_long_content(formatted, 2000)

        return f"```\n{formatted}\n```\n\n"

    def _build_final_answer_section(self, session_data: Dict[str, Any]) -> str:
        """Build final answer section."""
        return f"""## Final Answer

{session_data['final_answer']}

---

## Metadata

- **Session Number**: {session_data['metadata']['session_number']}
- **Execution Duration**: {session_data['metadata']['execution_duration']}
- **Tool Usage Statistics**:
"""

    def _build_tool_statistics(self, session_data: Dict[str, Any]) -> str:
        """Build tool usage statistics."""
        stats = []
        for tool in session_data['metadata']['tools_used']:
            tool_count = sum(
                1 for step in session_data['reaction_steps']
                if (step['step_type'] == 'action'
                    and step['tool_name'] == tool)
            )
            stats.append(f"  - `{tool}`: {tool_count} uses")

        footer = (
            "\n---\n"
            "*This report is automatically generated by "
            "GNS3 Copilot learning system*"
        )

        return '\n'.join(stats + ['', footer])

    def _build_technical_analysis_content(
        self,
        session_data: Dict[str, Any]
    ) -> str:
        """Build technical analysis content focusing on tool details."""
        parts = [self._build_tech_overview(session_data)]

        config_tools, display_tools, gns3_tools = self._categorize_tools(
            session_data['reaction_steps']
        )

        for step in session_data['reaction_steps']:
            if step['step_type'] == 'react_step':
                parts.append(self._format_react_step(step))
            else:
                parts.append(self._format_legacy_step(step))

        parts.extend(self._build_tool_stats(config_tools, display_tools, gns3_tools))
        parts.append(self._build_tech_final_answer(session_data))

        return ''.join(parts)

    def _build_tech_overview(self, session_data: Dict[str, Any]) -> str:
        """Build technical analysis overview."""
        execution_status = session_data.get('execution_status', 'unknown')
        status_text = {
            'completed': 'Completed Successfully',
            'interrupted': 'Interrupted',
            'failed': 'Failed',
            'running': 'Still Running',
            'unknown': 'Unknown Status'
        }.get(execution_status, 'Unknown Status')

        overview = [
            "# GNS3 Copilot Technical Analysis Report\n\n",
            "## Execution Overview\n",
            f"- **User Input**: {session_data['user_input']}\n",
            f"- **Session ID**: {session_data['session_id']}\n",
            f"- **Execution Status**: {status_text}\n",
            f"- **Start Time**: {session_data['start_time']}\n"
        ]

        if session_data.get('end_time'):
            overview.append(f"- **End Time**: {session_data['end_time']}\n")
        else:
            overview.append("- **End Time**: N/A\n")

        overview.extend([
            f"- **Total Steps**: {session_data['metadata']['total_steps']}\n",
            f"- **Execution Duration**: {session_data['metadata']['execution_duration']}\n"
        ])

        if interruption := session_data.get('interruption_reason'):
            overview.append(
                f"- **Interruption Reason**: {interruption}\n"
            )

        overview.append("\n## Detailed Execution Process Analysis\n\n")
        return ''.join(overview)

    def _categorize_tools(self, steps: List[Dict[str, Any]]) -> tuple:
        """Categorize tools used in steps."""
        config_tools = []
        display_tools = []
        gns3_tools = []

        for step in steps:
            tool_name = step.get('tool_name', '')
            tool_lower = tool_name.lower()

            if 'config' in tool_lower:
                config_tools.append(tool_name)
            elif 'display' in tool_lower or 'command' in tool_lower:
                display_tools.append(tool_name)
            elif 'gns3' in tool_lower:
                gns3_tools.append(tool_name)

        return config_tools, display_tools, gns3_tools

    def _format_react_step(
        self,
        step: Dict[str, Any]
    ) -> str:
        """Format ReAct step with detailed analysis."""
        parts = [
            f"### Step {step['step_number']}: ReAct Execution Cycle\n\n"
        ]

        if thought := step.get('thought'):
            parts.append(f"**Thought Process**:\n{thought}\n\n")

        if tool_name := step.get('tool_name'):
            parts.append(f"**Tool Used**: `{tool_name}`\n\n")

            if tool_name and 'config' in tool_name.lower():
                parts.append(self._format_config_analysis(step.get('action_input')))

        if action_input := step.get('action_input'):
            parts.extend([
                "**Tool Input Parameters**:\n",
                self._format_json_block(action_input),
                "\n"
            ])

        if parsing_error := step.get('parsing_error'):
            parts.extend([
                "**ReAct Parsing Error**:\n",
                f"```\n{parsing_error['error_message']}\n```\n\n"
            ])

        if tool_error := step.get('tool_error'):
            parts.extend([
                "**Tool Execution Error**:\n",
                f"```\n{tool_error['error_message']}\n```\n\n"
            ])

        if observation := step.get('observation'):
            parts.append(self._format_observation_result(observation))

        return ''.join(parts)

    def _format_config_analysis(self, action_input: Any) -> str:
        """Format configuration tool analysis."""
        if not isinstance(action_input, list) or not action_input:
            return "\n"

        analysis = ["**Configuration Tool Analysis**:\n"]
        for item in action_input:
            if isinstance(item, dict) and 'device_name' in item:
                device_name = item.get('device_name', 'Unknown')
                commands = item.get('config_commands', item.get('commands', []))
                analysis.append(
                    f"- Device `{device_name}`: {len(commands)} "
                    "configuration commands\n"
                )

        analysis.append("\n")
        return ''.join(analysis)

    def _format_observation_result(self, observation: Any) -> str:
        """Format observation result for technical analysis."""
        result_parts = ["**Observation Result**:\n"]

        if isinstance(observation, list):
            result_parts.extend(self._format_list_observation(observation))
        else:
            result_parts.extend(self._format_single_observation(observation))

        return ''.join(result_parts)

    def _format_list_observation(self, observation: List[Any]) -> List[str]:
        """Format list-type observation results."""
        result_parts = ["**Multi-Device Results**:\n"]

        for i, result in enumerate(observation):
            if isinstance(result, dict) and 'device_name' in result:
                result_parts.extend(self._format_device_result(result))
            else:
                result_parts.extend([
                    f"#### Result {i+1}:\n",
                    self._format_json_block(result),
                    "\n"
                ])

        return result_parts

    def _format_device_result(self, result: Dict[str, Any]) -> List[str]:
        """Format device-specific observation result."""
        device_name = result['device_name']
        result_parts = [f"#### Device: {device_name}\n\n"]

        for key, value in result.items():
            if key != 'device_name':
                result_parts.extend(self._format_device_property(key, value))

        return result_parts

    def _format_device_property(self, key: str, value: Any) -> List[str]:
        """Format a single device property."""
        formatted = self._format_content_for_display(value)

        if isinstance(value, str):
            truncated = self._truncate_long_content(formatted)
            return [
                f"**{key}**:\n",
                f"```\n{truncated}\n```\n\n"
            ]

        return [
            f"**{key}**:\n",
            f"```\n{formatted}\n```\n\n"
        ]

    def _format_single_observation(self, observation: Any) -> List[str]:
        """Format single observation result."""
        if isinstance(observation, (dict, list)):
            return [f"{self._format_json_block(observation)}\n\n"]

        if isinstance(observation, str):
            formatted = self._format_content_for_display(observation)
            return [f"```\n{formatted}\n```\n\n"]

        return [f"```\n{observation}\n```\n\n"]

    def _format_legacy_step(self, step: Dict[str, Any]) -> str:
        """Format legacy step types."""
        step_type = step['step_type']

        if step_type == 'thought':
            return (
                self._format_step_header(step['step_number'], step_type) +
                f"{step['content']}\n\n"
            )

        if step_type == 'action':
            tool_name = step['tool_name']
            return (
                self._format_step_header(step['step_number'], step_type) +
                f"**Tool Used**: `{tool_name}`\n\n" +
                f"{self._format_json_block(step['action_input'])}\n\n"
            )

        if step_type == 'observation':
            observation = step['content']
            header = self._format_step_header(step['step_number'], step_type)

            if isinstance(observation, (dict, list)):
                return f"{header}{self._format_json_block(observation)}\n\n"
            return f"{header}```\n{observation}\n```\n\n"

        return ""

    def _build_tool_stats(
        self,
        config_tools: List[str],
        display_tools: List[str],
        gns3_tools: List[str]
    ) -> List[str]:
        """Build tool usage statistics sections."""
        stats = ["## Tool Usage Statistics\n\n"]

        # Configuration tools
        stats.append(
            f"- **Configuration Tool Usage Count**: {len(config_tools)} times\n"
        )
        if config_tools:
            unique = ', '.join(set(config_tools))
            stats.append(f"  - Configuration tools used: {unique}\n")

        # Display tools
        stats.append(
            f"- **Display Tool Usage Count**: {len(display_tools)} times\n"
        )
        if display_tools:
            unique = ', '.join(set(display_tools))
            stats.append(f"  - Display tools used: {unique}\n")

        # GNS3 tools
        stats.append(
            f"- **GNS3 Tool Usage Count**: {len(gns3_tools)} times\n"
        )
        if gns3_tools:
            unique = ', '.join(set(gns3_tools))
            stats.append(f"  - GNS3 tools used: {unique}\n")

        stats.append("\n")
        return stats

    def _build_tech_final_answer(self, session_data: Dict[str, Any]) -> str:
        """Build final answer for technical report."""
        return (
            f"## Final Answer\n\n{session_data['final_answer']}\n\n"
            "---\n"
            "*This technical analysis report is automatically generated by "
            "GNS3 Copilot learning system*"
        )

    def _build_summary_content(self, session_data: Dict[str, Any]) -> str:
        """Build summary content with key highlights."""
        counts = self._calculate_step_counts(session_data['reaction_steps'])

        parts = [
            f"""# GNS3 Copilot Execution Summary

## Basic Information
- **Session ID**: {session_data['session_id']}
- **User Request**: {session_data['user_input']}
- **Execution Duration**: {session_data['metadata']['execution_duration']}
- **Total Steps**: {session_data['metadata']['total_steps']}

## Execution Flow Overview
""",
            f"- **Thought Steps**: {counts['thought']} times\n",
            f"- **Action Steps**: {counts['action']} times\n",
            f"- **Observation Steps**: {counts['observation']} times\n\n"
        ]

        if tools_used := session_data['metadata']['tools_used']:
            parts.append(self._build_tools_summary(tools_used, session_data))

        parts.append(self._build_key_steps_summary(session_data['reaction_steps']))
        parts.append(self._build_summary_final(session_data))

        return ''.join(parts)

    def _calculate_step_counts(self, steps: List[Dict[str, Any]]) -> Dict[str, int]:
        """Calculate counts for different step types."""
        return {
            'thought': sum(1 for step in steps if step['step_type'] == 'thought'),
            'action': sum(1 for step in steps if step['step_type'] == 'action'),
            'observation': sum(
                1 for step in steps if step['step_type'] == 'observation'
            )
        }

    def _build_tools_summary(
        self,
        tools_used: List[str],
        session_data: Dict[str, Any]
    ) -> str:
        """Build tools usage summary."""
        tool_stats = []
        steps = session_data['reaction_steps']

        for tool in tools_used:
            count = sum(
                1 for step in steps
                if (step['step_type'] == 'action' and step['tool_name'] == tool)
            )
            tool_stats.append(f"- `{tool}` ({count} times)")

        return "## Tools Used\n\n" + '\n'.join(tool_stats) + "\n\n"

    def _build_key_steps_summary(self, steps: List[Dict[str, Any]]) -> str:
        """Build key steps summary."""
        summary_parts = ["## Key Steps Summary\n\n"]

        for step in steps:
            if step['step_type'] == 'action':
                tool_name = step['tool_name']
                summary_parts.append(f"1. **Tool Used**: `{tool_name}`\n")

                if isinstance(step['action_input'], list) and step['action_input']:
                    summary_parts.extend(
                        self._format_action_details(step['action_input'])
                    )
                summary_parts.append("\n")

        return ''.join(summary_parts)

    def _format_action_details(self, action_input: List[Any]) -> List[str]:
        """Format action input details for summary."""
        details = []
        first_item = action_input[0] if action_input else {}

        if isinstance(first_item, dict):
            # Device names
            if 'device_name' in first_item:
                devices = [
                    item.get('device_name', 'Unknown')
                    for item in action_input
                    if isinstance(item, dict)
                ]
                details.append(f"   - Target Devices: {', '.join(devices)}\n")

            # Command count
            if 'commands' in first_item or 'config_commands' in first_item:
                cmd_key = (
                    'commands' if 'commands' in first_item 
                    else 'config_commands'
                )
                cmd_count = sum(
                    len(item.get(cmd_key, []))
                    for item in action_input
                    if isinstance(item, dict)
                )
                details.append(f"   - Command Count: {cmd_count}\n")

        return details

    def _build_summary_final(self, session_data: Dict[str, Any]) -> str:
        """Build final section for summary."""
        return f"""## Final Result

{session_data['final_answer']}

---

*This summary is automatically generated by GNS3 Copilot*
"""

    def generate_index_file(
        self,
        sessions: List[Dict[str, Any]],
        output_path: str
    ) -> None:
        """
        Generate index file listing all available sessions.

        Args:
            sessions: List of session data
            output_path: Path to save the index file
        """
        parts = [
            "# GNS3 Copilot Learning Session Index\n\n",
            "This directory contains all learning session records.\n\n",
            "## Session List\n\n",
            "| Session ID | User Input | Start Time | Steps | Tools | File |\n",
            "|------------|------------|------------|-------|-------|------|\n"
        ]

        for session in sessions:
            session_id = session['session_id']
            user_input = (
                session['user_input'][:50] + "..."
                if len(session['user_input']) > 50
                else session['user_input']
            )
            start_time = session['start_time'].split('T')[1][:8]
            step_count = session['metadata']['total_steps']
            tools_count = len(session['metadata']['tools_used'])

            parts.append(
                f"| {session_id} | {user_input} | {start_time} | "
                f"{step_count} | {tools_count} | "
                f"[View Details]({session_id}.md) |\n"
            )

        parts.extend([
            "\n---\n",
            "*Index file automatically generated by GNS3 Copilot*"
        ])

        content = ''.join(parts)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
