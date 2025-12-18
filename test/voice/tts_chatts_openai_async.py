
input="""
I can help you write network documentation. What specifically do you need?

Topology diagrams – I can read the current GNS3 layout and describe it
Configuration templates – EVPN-VXLAN, SR-MPLS, BGP designs
Troubleshooting guides – Common failure modes and verification steps
Automation playbooks – Ansible, pyATS, or Python scripts
Tell me what you're building or what problem you're solving, 
and I'll give you the concise, engineer-grade documentation you need.
"""

import asyncio

from openai import AsyncOpenAI
from openai.helpers import LocalAudioPlayer

openai = AsyncOpenAI(api_key="dummy-key", base_url="http://localhost:4123/v1")

async def main() -> None:
    async with openai.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=input,
        #instructions="Speak in a cheerful and positive tone.",
        response_format="wav",
    ) as response:
        await LocalAudioPlayer().play(response)

if __name__ == "__main__":
    asyncio.run(main())
    
    
