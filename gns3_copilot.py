from dotenv import load_dotenv
load_dotenv()

from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain_deepseek import ChatDeepSeek
from tools.device_command_tool import ExecuteCommands

# 直接在提示中嵌入 few-shot 示例
react_prompt_template = """
You are a network automation assistant that can execute commands on network devices. 
You have access to tools that can help you.

Here are some examples of how to interpret user requests:

Example 1:
Input: check R-1 and R-2 interfaces status
Output: Use execute_device_commands tool with:
{{"device_name": "R-1", "commands": ["show ip interface brief"]}}
{{"device_name": "R-2", "commands": ["show ip interface brief"]}}

Example 2:
Input: check R-3 and R-4 ospf status
Output: Use execute_device_commands tool with:
{{"device_name": "R-3", "commands": ["show ip ospf neighbor", "show ip ospf interface brief"]}}
{{"device_name": "R-4", "commands": ["show ip ospf neighbor", "show ip ospf interface brief"]}}

Example 3:
Input: view R-1 running config
Output: Use execute_device_commands tool with:
{{"device_name": "R-1", "commands": ["show running-config"]}}

You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action (should be a JSON string)
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Question: {input}
Thought: {agent_scratchpad}
"""

# 创建提示模板
custom_prompt = PromptTemplate(
    template=react_prompt_template,
    input_variables=["input", "agent_scratchpad", "tools", "tool_names"]
)

llm = ChatDeepSeek(model="deepseek-chat", temperature=0)
tools = [ExecuteCommands()]

# 使用自定义提示创建 ReAct agent
agent = create_react_agent(llm, tools, custom_prompt)

# 创建 AgentExecutor
agent_executor = AgentExecutor(
    agent=agent, 
    tools=tools, 
    verbose=True,
    handle_parsing_errors=True
)

if __name__ == "__main__":
    print("GNS3 Network Assistant - 输入 'quit' 退出")
    
    while True:
        user_input = input("\n请输入您的问题: ")
        
        if user_input.lower() in ['quit', 'exit', '退出']:
            break
            
        try:
            result = agent_executor.invoke({"input": user_input})
            print("\n回答:", result['output'])
        except Exception as e:
            print(f"错误: {e}")