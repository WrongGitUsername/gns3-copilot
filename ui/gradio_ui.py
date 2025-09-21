import gradio as gr
import json
import pickle
import os
from datetime import datetime

# 对话历史保存文件路径
CHAT_HISTORY_FILE = "chat_history.pkl"


# 自定义 CSS 样式 - 现代优雅风格
custom_css = """
/* 全局样式 - 现代优雅 */
* {
    font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}

/* 页面背景 - 渐变美学 */
.gradio-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%) !important;
    background-size: 400% 400% !important;
    animation: gradientShift 15s ease infinite !important;
    min-height: 100vh;
    padding: 20px;
    position: relative;
}

/* 背景动画 */
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* 主容器 - 紧凑玻璃拟态 */
.main-container {
    background: rgba(255, 255, 255, 0.1) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 20px !important;
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px !important;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
}

/* 聊天界面 - 超高设计 */
.chatbot {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(10px) !important;
    border: none !important;
    border-radius: 20px !important;
    max-width: 100% !important;
    width: 100% !important;
    min-height: 800px !important;
    max-height: 1200px !important;
    margin: 10px 0 !important;
    overflow-y: auto;
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.1),
        inset 0 1px 0 rgba(255, 255, 255, 0.6) !important;
}

/* 隐藏标签 */
.chatbot .label,
.chatbot > label,
.chatbot .block-label {
    display: none !important;
}

/* 消息样式 - 现代气泡 */
.chatbot .message {
    margin: 16px 20px !important;
    padding: 20px 24px !important;
    border-radius: 18px !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
    border: none !important;
    position: relative;
    max-width: 85%;
}

/* 用户消息 - 渐变蓝紫 */
.chatbot .message.user {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    margin-left: auto !important;
    margin-right: 20px !important;
    border-bottom-right-radius: 6px !important;
}

.chatbot .message.user::before {
    content: '';
    position: absolute;
    bottom: 0;
    right: -8px;
    width: 0;
    height: 0;
    border: 8px solid transparent;
    border-bottom-color: #764ba2;
    border-right: 0;
    border-bottom-right-radius: 0;
}

/* AI 消息 - 柔和白色 */
.chatbot .message.bot {
    background: linear-gradient(135deg, #f8f9fa 0%, #ffffff 100%) !important;
    color: #2d3748 !important;
    margin-left: 20px !important;
    margin-right: auto !important;
    border: 1px solid rgba(0, 0, 0, 0.08) !important;
    border-bottom-left-radius: 6px !important;
}

.chatbot .message.bot::before {
    content: '';
    position: absolute;
    bottom: 0;
    left: -8px;
    width: 0;
    height: 0;
    border: 8px solid transparent;
    border-bottom-color: #ffffff;
    border-left: 0;
}

/* 代码块 - 专业深色主题 */
.chatbot pre {
    background: #1a1a1a !important;
    color: #f8f8f2 !important;
    border-radius: 12px !important;
    padding: 20px !important;
    margin: 16px 0 !important;
    font-family: "JetBrains Mono", "Fira Code", "SF Mono", monospace !important;
    font-size: 14px !important;
    line-height: 1.5 !important;
    overflow-x: auto;
    border: 1px solid #333 !important;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3) !important;
}

.chatbot code {
    background: rgba(102, 126, 234, 0.1) !important;
    color: #667eea !important;
    padding: 3px 6px !important;
    border-radius: 6px !important;
    font-family: "JetBrains Mono", "Fira Code", monospace !important;
    font-size: 13px !important;
}

/* 输入区域 - 紧凑设计 */
.gradio-textbox {
    max-width: 100% !important;
    margin: 10px 0 !important;
}

.gradio-textbox input,
.gradio-textbox textarea {
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 12px !important;
    color: #2d3748 !important;
    padding: 12px 18px !important;
    font-size: 14px !important;
    font-weight: 400 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1) !important;
}

.gradio-textbox input:focus,
.gradio-textbox textarea:focus {
    outline: none !important;
    border-color: rgba(102, 126, 234, 0.6) !important;
    background: rgba(255, 255, 255, 1) !important;
    box-shadow: 
        0 4px 20px rgba(0, 0, 0, 0.1),
        0 0 0 4px rgba(102, 126, 234, 0.1) !important;
    transform: translateY(-2px) !important;
}

.gradio-textbox input::placeholder,
.gradio-textbox textarea::placeholder {
    color: #a0aec0 !important;
    font-weight: 400 !important;
}

/* 按钮 - 紧凑设计 */
button {
    background: rgba(255, 255, 255, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 8px !important;
    color: #4a5568 !important;
    padding: 8px 16px !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

button:hover {
    transform: translateY(-3px) !important;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
    background: rgba(255, 255, 255, 1) !important;
}

button.primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    border: none !important;
    color: white !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
}

button.primary:hover {
    box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5) !important;
    transform: translateY(-3px) scale(1.02) !important;
}

button.secondary {
    background: rgba(255, 255, 255, 0.8) !important;
    color: #667eea !important;
    border: 2px solid rgba(102, 126, 234, 0.2) !important;
}

button.secondary:hover {
    border-color: rgba(102, 126, 234, 0.4) !important;
    background: rgba(255, 255, 255, 1) !important;
}

/* 按钮容器 */
.gradio-row {
    max-width: 100% !important;
    margin: 10px 0 !important;
    justify-content: center !important;
    gap: 8px !important;
}

/* 标题 - 紧凑设计 */
.title {
    color: white !important;
    text-align: center;
    font-size: 28px !important;
    font-weight: 600 !important;
    margin-bottom: 4px !important;
    text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3) !important;
    letter-spacing: -0.5px !important;
}

.subtitle {
    color: rgba(255, 255, 255, 0.8) !important;
    text-align: center;
    font-size: 14px !important;
    font-weight: 400 !important;
    margin-bottom: 20px !important;
    text-shadow: 0 1px 5px rgba(0, 0, 0, 0.2) !important;
}

/* Details 元素 - 现代折叠 */
details {
    background: rgba(255, 255, 255, 0.05) !important;
    backdrop-filter: blur(10px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    margin: 12px 0 !important;
    overflow: hidden !important;
    transition: all 0.3s ease !important;
}

details:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: rgba(255, 255, 255, 0.2) !important;
}

details summary {
    background: rgba(102, 126, 234, 0.9) !important;
    color: white !important;
    padding: 16px 20px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    cursor: pointer !important;
    border: none !important;
    margin: 0 !important;
    transition: all 0.3s ease !important;
    user-select: none !important;
}

details summary:hover {
    background: rgba(102, 126, 234, 1) !important;
}

details[open] summary {
    border-bottom: 1px solid rgba(255, 255, 255, 0.1) !important;
}

details > div {
    padding: 20px !important;
    color: rgba(255, 255, 255, 0.9) !important;
    line-height: 1.6 !important;
}

/* 头像 - 现代圆形 */
.avatar {
    width: 36px !important;
    height: 36px !important;
    border-radius: 50% !important;
    border: 3px solid rgba(255, 255, 255, 0.8) !important;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
}

/* 帮助信息 */
.help-content {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.3) !important;
    border-radius: 16px !important;
    padding: 24px !important;
    margin: 20px 0 !important;
    color: #2d3748 !important;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1) !important;
}

.help-content h3 {
    color: #667eea !important;
    margin-top: 0 !important;
    margin-bottom: 16px !important;
    font-weight: 700 !important;
}

/* 滚动条 - 现代设计 */
.chatbot::-webkit-scrollbar {
    width: 8px;
}

.chatbot::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.05);
    border-radius: 4px;
}

.chatbot::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px;
    transition: all 0.3s ease;
}

.chatbot::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #5a6fd8 0%, #6b4190 100%);
}

/* 加载动画 */
@keyframes slideInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.chatbot .message {
    animation: slideInUp 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
}

/* 响应式设计 */
@media (max-width: 1024px) {
    .gradio-container {
        padding: 16px;
    }
    
    .main-container {
        padding: 18px;
    }
    
    .title {
        font-size: 26px !important;
    }
}

@media (max-width: 768px) {
    .chatbot {
        min-height: 600px !important;
        max-height: 900px !important;
    }
    
    .title {
        font-size: 24px !important;
    }
    
    .subtitle {
        font-size: 12px !important;
    }
    
    .chatbot .message {
        margin: 12px 16px !important;
        padding: 16px 20px !important;
        max-width: 90%;
    }
    
    .gradio-container {
        padding: 12px;
    }
    
    .main-container {
        padding: 16px;
    }
}

@media (max-width: 480px) {
    .title {
        font-size: 20px !important;
    }
    
    .chatbot .message {
        margin: 8px 12px !important;
        padding: 14px 18px !important;
        max-width: 95%;
    }
    
    .chatbot {
        min-height: 500px !important;
        max-height: 700px !important;
    }
}

/* 特殊效果 */
.chatbot .message:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15) !important;
}

/* Markdown 样式优化 */
.chatbot .message h1,
.chatbot .message h2,
.chatbot .message h3 {
    margin-top: 20px !important;
    margin-bottom: 12px !important;
    font-weight: 700 !important;
}

.chatbot .message p {
    margin-bottom: 12px !important;
    line-height: 1.7 !important;
}

.chatbot .message ul,
.chatbot .message ol {
    padding-left: 20px !important;
    margin-bottom: 12px !important;
}

.chatbot .message li {
    margin-bottom: 6px !important;
}
"""

def load_chat_history():
    """从文件加载对话历史"""
    if os.path.exists(CHAT_HISTORY_FILE):
        try:
            with open(CHAT_HISTORY_FILE, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            print(f"加载对话历史失败: {e}")
    return []

def save_chat_history(chat_history):
    """保存对话历史到文件"""
    try:
        with open(CHAT_HISTORY_FILE, 'wb') as f:
            pickle.dump(chat_history, f)
    except Exception as e:
        print(f"保存对话历史失败: {e}")

# ... 保持其他代码不变，只修改布局部分 ...

def run_gradio_ui(agent_executor):
    """
    使用 gr.Blocks 配置并启动一个高级 Gradio 用户界面，
    思考过程直接显示在对话框内。
    """
    
    # 加载已保存的对话历史
    initial_chat_history = load_chat_history()
    
    with gr.Blocks(
        theme=None, 
        css=custom_css,
        title="GNS3 智能助手"
    ) as demo:
        
        # 标题区域
        gr.HTML("""
        <div class="title">
            ✨ GNS3 智能助手
        </div>
        <div class="subtitle">
            现代化网络自动化管理平台
        </div>
        """)

        # 使用 gr.State 来管理对话状态
        chat_state = gr.State(value=initial_chat_history)

        # 主聊天窗口 - 更高的窗口
        chatbot = gr.Chatbot(
            bubble_full_width=False, 
            render_markdown=True,
            value=initial_chat_history,
            height=850,
            avatar_images=[
                "https://cdn-icons-png.flaticon.com/512/149/149071.png",
                "https://cdn-icons-png.flaticon.com/512/4712/4712035.png",
            ],
        )

        # 用户输入区域
        with gr.Row():
            msg = gr.Textbox(
                label="",
                placeholder="输入您的问题或指令...",
                scale=6,
                container=False
            )
            submit_btn = gr.Button("发送", variant="primary", scale=1)
        
        # 按钮区域
        with gr.Row():
            clear_btn = gr.Button("清空", variant="secondary")
            export_btn = gr.Button("导出", variant="secondary")
            help_btn = gr.Button("帮助", variant="secondary")
            
        # 文件下载组件
        download_file = gr.File(visible=False)
        
        # 帮助信息（初始隐藏）
        help_info = gr.Markdown(
            """
            ### 🚀 快速开始
            
            **支持的命令类型：**
            - 📋 **查看配置:** `查看 R-1 设备配置`
            - 🔗 **接口状态:** `显示 R-2 接口状态`
            - 🌐 **路由协议:** `在 R-1 上配置 OSPF`
            - 🛠️ **接口配置:** `在 R-1 GE0/0 上配置 IP 地址`
            
            **示例查询：**
            - "检查 R-1 和 R-2 的 OSPF 邻居状态"
            - "在 R-3 上配置环回接口"
            - "显示所有设备的接口摘要"
            
            ### 💡 智能功能
            - 🤖 **自然语言处理:** 用中文自然语言描述网络需求
            - 🔍 **智能分析:** 自动理解设备拓扑和配置关系
            - ⚡ **快速响应:** 实时获取设备状态和配置信息
            - 📊 **可视化展示:** 清晰展示网络拓扑和配置结果
            
            **使用技巧：**
            - 使用设备名称如 R-1, R-2, R-3 等
            - 明确指定要操作的接口或协议
            - AI 会在执行命令前展示思考过程
            """,
            visible=False
        )

        def respond(message, chat_history):
            # 1. 立即更新UI，显示用户消息，AI开始思考
            chat_history.append((message, "🤔 正在分析你的问题..."))
            yield {
                chatbot: chat_history
            }

            # 2. 准备流式处理所需变量
            full_response = ""
            thinking_content = ""
            current_step = 0
            
            # 3. 迭代 Agent 的流式输出
            for chunk in agent_executor.stream({"input": message}):
                # a. 捕获新的思考和动作
                if "actions" in chunk:
                    for action in chunk["actions"]:
                        current_step += 1
                        
                        # 解析 action.log 内容，提取纯思考部分
                        log_content = action.log
                        
                        # 提取思考部分（去掉 Action 和 Action Input 部分）
                        thought_content = ""
                        if "Thought:" in log_content:
                            thought_part = log_content.split("Action:")[0]  # 取 Action 之前的部分
                            thought_content = thought_part.replace("Thought:", "").strip()
                        else:
                            thought_content = log_content.strip()
                        
                        # 构建当前步骤的思考过程内容
                        step_content = f"""
<details open>
<summary><strong>🔄 第 {current_step} 步：思考与行动</strong></summary>

**🤔 思考:**
{thought_content}

**▶️ 动作:** 调用工具 `{action.tool}`

**📥 输入参数:**
```json
{json.dumps(action.tool_input, indent=2, ensure_ascii=False) if isinstance(action.tool_input, dict) else str(action.tool_input)}
```

**👀 观察结果:** *等待工具返回结果...*
</details>

"""
                        thinking_content += step_content
                        
                        # 更新聊天窗口，显示当前的思考过程
                        chat_history[-1] = (message, thinking_content)
                        yield {
                            chatbot: chat_history
                        }

                # b. 捕获工具的观察结果
                elif "steps" in chunk:
                    for step in chunk["steps"]:
                        # 更新最后一个步骤的观察结果
                        thinking_content = thinking_content.replace(
                            "**👀 观察结果:** *等待工具返回结果...*",
                            f"**👀 观察结果:**\n```\n{step.observation}\n```"
                        )
                        
                        # 将当前步骤标记为完成（关闭details）
                        thinking_content = thinking_content.replace(
                            f'<details open>\n<summary><strong>🔄 第 {current_step} 步：思考与行动</strong></summary>',
                            f'<details>\n<summary><strong>✅ 第 {current_step} 步：已完成</strong></summary>'
                        )
                        
                        chat_history[-1] = (message, thinking_content)
                        yield {
                            chatbot: chat_history
                        }
                
                # c. 捕获并累加最终答案
                elif "output" in chunk:
                    full_response += chunk["output"]
                    
                    # 构建最终的完整回复（思考过程 + 最终答案）
                    final_content = thinking_content + f"""
---

## 🎯 最终答案

{full_response}
"""
                    
                    chat_history[-1] = (message, final_content)
                    yield {
                        chatbot: chat_history
                    }
            
            # 4. 保存对话历史到文件
            save_chat_history(chat_history)
            yield {
                chatbot: chat_history
            }

        def clear_chat():
            """清除当前对话"""
            empty_history = []
            save_chat_history(empty_history)
            return {
                chatbot: empty_history,
                chat_state: empty_history
            }

        def export_chat(chat_history):
            """导出对话历史为文本文件"""
            if not chat_history:
                return gr.update(visible=False)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"chat_history_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"GNS3 Copilot 对话历史\n")
                f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("="*50 + "\n\n")
                
                for i, (user_msg, ai_msg) in enumerate(chat_history, 1):
                    f.write(f"对话 {i}:\n")
                    f.write(f"用户: {user_msg}\n")
                    f.write(f"助手: {ai_msg or '(无回复)'}\n")
                    f.write("-"*30 + "\n\n")
            
            return gr.update(value=filename, visible=True)

        # 绑定事件
        submit_btn.click(
            respond, 
            [msg, chat_state], 
            [chatbot]
        ).then(
            lambda: gr.update(value=""), 
            outputs=[msg]
        ).then(
            lambda history: history,
            [chatbot],
            [chat_state]
        )
        
        msg.submit(
            respond, 
            [msg, chat_state], 
            [chatbot]
        ).then(
            lambda: gr.update(value=""), 
            outputs=[msg]
        ).then(
            lambda history: history,
            [chatbot],
            [chat_state]
        )

        clear_btn.click(
            clear_chat,
            outputs=[chatbot, chat_state]
        )

        export_btn.click(
            export_chat,
            [chat_state],
            [download_file]
        )

        help_btn.click(
            lambda: gr.update(visible=True) if not help_info.visible else gr.update(visible=False),
            outputs=[help_info]
        )

    # 启动 Gradio 服务
    print("Gradio UI is running on http://0.0.0.0:7860")
    print(f"对话历史将保存到: {os.path.abspath(CHAT_HISTORY_FILE)}")
    demo.launch(server_name="0.0.0.0", server_port=7860)