import gradio as gr
import io
from contextlib import redirect_stdout
import time

def run_gradio_ui(agent_executor, *args, **kwargs):
    def chat_fn(message, _):
        try:
            # 捕获 verbose 输出
            stdout_buffer = io.StringIO()
            with redirect_stdout(stdout_buffer):
                result = agent_executor.invoke({"input": message})
            
            # 获取 verbose 输出和最终答案
            verbose_output = stdout_buffer.getvalue().splitlines()
            final_answer = result.get('output', '抱歉，无法处理您的请求。')
            
            # 逐步返回 verbose 输出
            yield "📝 **详细信息:**\n\n"
            for line in verbose_output:
                yield f"```\n{line}\n```\n"
                time.sleep(0.1)  # 模拟流式返回的延迟
            
            # 最后返回最终答案
            yield f"\n🎯 **答案:**\n\n{final_answer}"
        except Exception as e:
            yield f"❌ **发生错误:**\n\n```\n{str(e)}\n```"

    demo = gr.ChatInterface(
        fn=chat_fn,
        title="🤖 GNS3 Copilot - 智能网络助手",
        description="输入网络命令或问题，查看 AI 的响应和详细信息！",
        theme=gr.themes.Default(),
        type="messages"
    )
    demo.launch(server_name="0.0.0.0", server_port=7860)

if __name__ == "__main__":
    run_gradio_ui()
