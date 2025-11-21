from agent import agent
from langchain.messages import ToolMessage, HumanMessage, AIMessage
from langchain_core.runnables import RunnableConfig

config: RunnableConfig = {"configurable": {"thread_id": "hahahahahhaha"}}

human = [
    HumanMessage(
        content=(
            "Hello, GNS3 Copilot!,"
            "告诉我当前的拓扑情况。"
            )
        )
    ]

messages = agent.stream(
    {"messages": human},
    config=config,
    stream_mode="updates"
    )

for chunk in messages:
    for node_name, update in chunk.items():
        if "messages" in update:
            for msg in update["messages"]:
                if isinstance(msg, AIMessage):
                    print("AIMessage:", msg.content)
                    if msg.tool_calls:
                        for tool in msg.tool_calls:
                            print(f"tool_name: {tool['name']},"
                                   f"{tool['args']},"
                                   f"tool_calls_id={tool['id']}"
                                   )
                elif isinstance(msg, ToolMessage):
                    print(msg.content)