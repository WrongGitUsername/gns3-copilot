import asyncio
from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer
import textwrap # 用于更清晰地处理多行字符串

# 确保您的本地服务（如 FastChat 或 litellm 代理）在 http://localhost:8000/v1 运行
openai = AsyncOpenAI(base_url="http://localhost:8000/v1", api_key="not-needed")

input_str = """
I can help you write network documentation. What specifically do you need?

Topology diagrams – I can read the current G N S 3 layout and describe it
Configuration templates – E V P N-V X LAN, S R-M P L S, B G P designs
Troubleshooting guides – Common failure modes and verification steps
Automation playbooks – Ansible, py A T S, or Python scripts
Tell me what you're building or what problem you're solving, 
and I'll give you the concise, engineer-grade documentation you need

I can help you write network documentation. What specifically do you need?

Topology diagrams – I can read the current G N S 3 layout and describe it
Configuration templates – E V P N-V X LAN, S R-M P L S, B G P designs
Troubleshooting guides – Common failure modes and verification steps
Automation playbooks – Ansible, py A T S, or Python scripts
Tell me what you're building or what problem you're solving, 
and I'll give you the concise, engineer-grade documentation you need
"""

async def main() -> None:
    print("--- 准备按行进行异步 TTS 转换和播放 ---")
    
    # 1. 分割文本：使用 splitlines() 获取每一行
    # filter(None, ...) 用于去除空行 (包括只包含空格或制表符的行)
    lines = [
        line.strip() 
        for line in input_str.splitlines() 
        if line.strip()
    ]
    
    if not lines:
        print("警告：输入字符串中没有检测到有效的文本行。")
        return

    # 2. 遍历每一行文本并执行 TTS
    for i, line in enumerate(lines, 1):
        print(f"\n[第 {i} 行] 正在处理文本: '{line}'")
        
        try:
            # 3. 对当前行调用异步 TTS API
            async with openai.audio.speech.with_streaming_response.create(
                model="gpt-4o-mini-tts",
                voice="coral",
                input=line,  # <-- 关键修改：传入当前循环的文本行
                instructions="Speak in a clear and helpful tone.", # 修改了语气描述
                response_format="wav",
                speed=0.5
            ) as response:
                print(f"    ▶️ 开始播放第 {i} 行音频...")
                # 4. 使用 LocalAudioPlayer 播放流
                # LocalAudioPlayer 是一个同步阻塞操作，但它是在异步上下文中被调用的
                await LocalAudioPlayer().play(response)
                print(f"    ✅ 第 {i} 行播放完毕。")
                
        except Exception as e:
            print(f"❌ 第 {i} 行 TTS 转换/播放出错：{e}")
            # 如果本地服务返回错误，可以打印更多细节
            # print(f"原始响应状态: {response.status_code if 'response' in locals() else 'N/A'}")

if __name__ == "__main__":
    # 异步运行 main 函数
    asyncio.run(main())