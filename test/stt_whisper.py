# pip install -U openai-whisper -i https://pypi.tuna.tsinghua.edu.cn/simple

import os
from pathlib import Path
import whisper
import torch
import warnings

# 忽略可能出现的 UserWarning 和其他不影响运行的警告
warnings.filterwarnings("ignore")

## --- 1. 路径设置 ---
# 获取当前文件所在目录的上级目录作为项目根目录
PROJECT_ROOT = Path(__file__).parent.parent.resolve()
# 假设您的测试音频文件位于项目根目录下的 'audio' 文件夹内
TEST_AUDIO = PROJECT_ROOT / "test" / "86_QiTianDaSheng.wav" 

print("========================================")
print(f"测试音频文件: {TEST_AUDIO}")

# 检查测试音频文件是否存在
if not TEST_AUDIO.exists():
    print("错误：测试音频文件不存在！请确保音频文件路径正确。")
    print("期望路径: " + str(TEST_AUDIO))
    exit(1)

## --- 2. 加载模型 ---
# 自动检测并使用 CUDA (GPU) 或 CPU
device = "cuda" if torch.cuda.is_available() else "cpu"
# 使用您选择的 medium 模型
model_name = "medium" 

print(f"使用设备: {device}")
print(f"正在加载 Whisper {model_name} 模型，请稍等...")
# 第一次运行时，此行代码会自动下载约 1.53 GB 的 medium 模型文件到本地缓存。
try:
    model = whisper.load_model(model_name, device=device) 
    print(f"Whisper {model_name} 模型加载成功！")
except Exception as e:
    print(f"模型加载失败，请检查 PyTorch 和 CUDA 环境：{e}")
    exit(1)

## --- 3. 开始转录 ---
print("========================================")
print(f"开始识别音频...")

# 识别函数
# 设置 language="en" (英文) 以提高准确性
# fp16=(device == "cuda") 启用半精度计算，在 GPU 上加速推理
result = model.transcribe(
    str(TEST_AUDIO),
    language="zh",       
    verbose=False,       
    fp16=(device == "cuda") 
)

# 提取文字
text = result["text"].strip()

## --- 4. 打印结果 ---
print("========================================")
print("识别完成！结果如下：")
print("========================================")
print(text)
print("========================================")
print(f"识别耗时: (请自行计时)")
# 可选：显示音频时长
try:
    audio_duration = whisper.load_audio(str(TEST_AUDIO)).shape[0] / whisper.base_sampling_rate
    print(f"音频时长: {audio_duration:.1f} 秒")
except:
    pass
print("========================================")