from openai import OpenAI

client = OpenAI(
    api_key="local-dummy",
    base_url="http://127.0.0.1:8001/v1",
)
audio_file= open("output.wav", "rb")

stream = client.audio.transcriptions.create(
    file=audio_file,
    model="whisper-1",
    response_format='text',
    stream=True
)

for event in stream:
    print(event)