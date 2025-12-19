from agent import agent
from langchain.messages import HumanMessage
from langchain_core.runnables import RunnableConfig

config: RunnableConfig = {"configurable": {"thread_id": "123123hahahahahhaha"}}

human = [
    HumanMessage(
        content=(
            "Hello, GNS3 Copilot!,"
            "ping test from r-1 to r-6"
            )
        )
    ]

messages = agent.stream(
    {"messages": human},
    config=config,
    stream_mode="updates"
    )

for chunk in messages:
    print(chunk)
    # for node_name, update in chunk.items():
        #if "messages" in update:
            #for msg in update["messages"]:
                #print(msg)
                #if isinstance(msg, AIMessage):
                #    print("AIMessage:", msg.content)
                #    if msg.tool_calls:
                #        for tool in msg.tool_calls:
                #            print(f"tool_name: {tool['name']},"
                #                   f"{tool['args']},"
                #                   f"tool_calls_id={tool['id']}"
                #                   )
                #elif isinstance(msg, ToolMessage):
                #    print(msg.content)