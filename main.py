import os
import logging

# 设置 LangChain 调试环境变量
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_DEBUG"] = "true"
os.environ["LANGCHAIN_VERBOSE"] = "true"

# 配置 Python 日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from langchain_agent import GNS3Agent

def main():
    logger.info("开始初始化 GNS3 Agent...")
    
    # 初始化Agent
    agent = GNS3Agent()
    
    # 获取可用设备
    logger.info("获取可用设备...")
    devices = agent.get_available_devices()
    print(f"可用设备: {devices}")
    
    # 交互式查询
    while True:
        user_input = input("\n请输入查询命令（输入'quit'退出）: ")
        if user_input.lower() == 'quit':
            break
            
        logger.info(f"处理用户查询: {user_input}")
        result = agent.query(user_input)
        
        if result["success"]:
            print("=" * 50)
            print(result["result"])
            print("=" * 50)
        else:
            print(f"错误: {result['result']}")

if __name__ == "__main__":
    main()