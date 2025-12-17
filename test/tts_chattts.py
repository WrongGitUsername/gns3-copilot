# OpenAI API test (non-streaming)
from openai import OpenAI

# 情感控制
# 在input中：  [oral_0]  [laugh_0]  [break_5]
# Initialize the client
client = OpenAI(api_key="dummy-key", base_url="http://localhost:8000/v1")

# Generate audio
response = client.audio.speech.create(
    model="tts-1",
    voice="echo",
    response_format="wav",
    speed="0.5",
    # 文本过滤的基本修改，针对英语的。 连续的大写字符，中间加空格。 连续的大写字母或小写字母前后有数字的，加空格。
    input="""
I can help you write network documentation. What specifically do you need?

Topology diagrams – I can read the current G N S 3 layout and describe it
Configuration templates – E V P N-V X L A N, S R-M P L S, B G P designs
Troubleshooting guides – Common failure modes and verification steps
Automation playbooks – Ansible, py A T S, or Python scripts
Tell me what you're building or what problem you're solving, 
and I'll give you the concise, engineer-grade documentation you need.""",
)

# Get audio binary data
audio_data = response.content  # response.content is of type bytes

# Display and play in the Notebook
#display(Audio(audio_data, autoplay=False))
with open("output.wav", "wb") as f:
    f.write(audio_data)
