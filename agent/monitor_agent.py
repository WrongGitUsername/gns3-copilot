# 接executor_agent的输出，使用一个单独的 LLM Chain (或一个固定的判断函数) 对执行结果进行评估。
# Prompt 重点： 强调判断 (Judge) 和比较 (Compare)。
# 输入包含 task, expected_output, 和 actual_output。
# 可以是一个简单的 LLM Chain，输出一个布尔值 (True / False) 和一个评估报告。