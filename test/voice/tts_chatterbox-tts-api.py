# OpenAI API test (non-streaming)
from openai import OpenAI

input_1 = """
I read topology now.

Topology has:

Project name: network_ai
Six routers: R-1, R-2, R-3, R-4, R-5, R-6
Seven links (cables) connect them
Links:

R-1 Ge 0/0 → R-2 Ge 0/0
R-2 Ge 0/3 → R-3 Ge 0/2
R-2 Ge 0/4 → R-4 Ge 0/2
R-3 Ge 0/5 → R-5 Ge 0/3
R-4 Ge 0/5 → R-5 Ge 0/4
R-5 Ge 0/0 → R-6 Ge 0/0
R-3 Ge 0/0 → R-4 Ge 0/0
All routers have 16 ports each. No switches or PCs in this topology. Topology ready for configuration
"""

input_2 = """
I can help you write network documentation. What specifically do you need?

Topology diagrams – I can read the current GNS3 layout and describe it
Configuration templates – EVPN-VXLAN, SR-MPLS, BGP designs
Troubleshooting guides – Common failure modes and verification steps
Automation playbooks – Ansible, pyATS, or Python scripts
Tell me what you're building or what problem you're solving, 
and I'll give you the concise, engineer-grade documentation you need.
"""

# Initialize the client
client = OpenAI(api_key="dummy-key", base_url="http://localhost:4123/v1")

# Generate audio
response = client.audio.speech.create(
    model="tts-1",
    voice="alloy",
    response_format="wav",
    input=input_1,
)

# Get audio binary data
audio_data = response.content  # response.content is of type bytes

# Display and play in the Notebook
#display(Audio(audio_data, autoplay=False))
with open("output.wav", "wb") as f:
    f.write(audio_data)
