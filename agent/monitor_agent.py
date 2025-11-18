# Receives output from executor_agent and uses a separate LLM Chain (or a fixed judgment function) to evaluate execution results.
# Prompt focus: Emphasize judgment and comparison.
# Input includes task, expected_output, and actual_output.
# Can be a simple LLM Chain, outputting a boolean value (True/False) and an evaluation report.
