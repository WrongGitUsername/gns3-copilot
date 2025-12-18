from openai import OpenAI
from typing import Union, BinaryIO, Optional, List
import io
import os
import json
from dotenv import load_dotenv
from gns3_copilot.log_config import setup_logger

# Load environment variables
load_dotenv()

logger = setup_logger("openai_stt")

# Default networking prompt to improve recognition of technical terms
DEFAULT_GNS3_PROMPT = (
    "GNS3, Cisco, router, switch, OSPF, BGP, EIGRP, ISIS, VLAN, STP, "
    "interface, FastEthernet, GigabitEthernet, loopback, config terminal, "
    "no shutdown, show running-config, Wireshark, encapsulation."
)

def get_stt_config():
    """
    Get STT configuration from environment variables with sensible defaults.
    
    Returns:
        dict: Dictionary containing STT configuration parameters.
    """
    return {
        'api_key': os.getenv('STT_API_KEY', ''),
        'base_url': os.getenv('STT_BASE_URL', 'http://127.0.0.1:8001/v1'),
        'model': os.getenv('STT_MODEL', 'whisper-1'),
        'language': os.getenv('STT_LANGUAGE', None),
        'temperature': float(os.getenv('STT_TEMPERATURE', '0.0')),
        'response_format': os.getenv('STT_RESPONSE_FORMAT', 'json')
    }

def speech_to_text(
    audio_data: Union[bytes, BinaryIO],
    model: Optional[str] = None,
    language: Optional[str] = None,
    prompt: Optional[str] = DEFAULT_GNS3_PROMPT,
    response_format: Optional[str] = None,
    temperature: Optional[float] = None,
    timestamp_granularities: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> Union[str, dict]:
    """
    Transcribe audio to text using OpenAI Whisper API.
    
    Args:
        audio_data: Audio data as bytes or file-like object.
        model: Optional[str]: Whisper model name. If not provided, uses STT_MODEL environment variable or "whisper-1".
        language: Optional[str]: ISO 639-1 language code. If not provided, uses STT_LANGUAGE environment variable or None.
        prompt: Optional[str]: Contextual text to guide transcription.
        response_format: Optional[str]: Output format (json, text, srt, etc.). If not provided, uses STT_RESPONSE_FORMAT environment variable or "json".
        temperature: Optional[float]: Sampling temperature (0.0 to 1.0). If not provided, uses STT_TEMPERATURE environment variable or 0.0.
        timestamp_granularities: Optional[List[str]]: Levels of detail for timestamps.
        api_key: Optional[str]: OpenAI API key. If not provided, uses STT_API_KEY environment variable or "".
        base_url: Optional[str]: Custom API endpoint. If not provided, uses STT_BASE_URL environment variable or "http://127.0.0.1:8001/v1".
    """
    # Get default configuration from environment variables
    config = get_stt_config()
    
    # Use provided parameters or fall back to environment defaults
    model = model if model is not None else config['model']
    response_format = response_format if response_format is not None else config['response_format']
    temperature = temperature if temperature is not None else config['temperature']
    api_key = api_key if api_key is not None else config['api_key']
    base_url = base_url if base_url is not None else config['base_url']
    language = language if language is not None else config['language']
    
    # 1. Basic parameter validation
    if not audio_data:
        raise ValueError("Audio data cannot be empty")
    
    valid_models = ["whisper-1", "gpt-4o-transcribe", "gpt-4o-transcribe-diarize"]
    if model not in valid_models:
        raise ValueError(f"Invalid model '{model}'. Supported: {valid_models}")
    
    valid_formats = ["json", "text", "srt", "verbose_json", "vtt", "tsv"]
    if response_format not in valid_formats:
        raise ValueError(f"Invalid response_format '{response_format}'")

    # 2. Audio preprocessing and size validation (OpenAI 25MB limit)
    if isinstance(audio_data, bytes):
        size_mb = len(audio_data) / (1024 * 1024)
        audio_file = io.BytesIO(audio_data)
        audio_file.name = "audio.wav"
    else:
        audio_file = audio_data
        if not hasattr(audio_file, "name"):
            setattr(audio_file, "name", "audio.wav")
        
        # Check size of the file-like object
        audio_file.seek(0, os.SEEK_END)
        size_mb = audio_file.tell() / (1024 * 1024)
        audio_file.seek(0) # Important: reset pointer

    if size_mb > 25:
        raise ValueError(f"Audio file size too large ({size_mb:.2f}MB). Max limit is 25MB.")

    try:
        # 3. Initialize OpenAI Client
        client = OpenAI(
            api_key=api_key if api_key is not None else "local-dummy",
            base_url=base_url if base_url is not None else "http://127.0.0.1:8001/v1",
            timeout=60.0  # Transcription can be slow; use longer timeout
        )

        # 4. Prepare API request parameters
        api_params = {
            "file": audio_file,
            "model": model,
            "response_format": response_format,
            "temperature": temperature,
        }
        
        if language: api_params["language"] = language
        if prompt: api_params["prompt"] = prompt
        if timestamp_granularities: api_params["timestamp_granularities"] = timestamp_granularities

        # 5. Execute API Call
        response = client.audio.transcriptions.create(**api_params)

        # 6. Handle response variations across SDK versions and formats
        # Return raw string if format is text/srt/vtt/tsv
        if isinstance(response, str):
            return response

        # Extract dict if response is a Pydantic model (OpenAI SDK v1.0+)
        if hasattr(response, 'model_dump'):
            data = response.model_dump()
            # If JSON format requested but only need text string
            if response_format == "json":
                return data.get("text", "")
            return data

        # Generic fallback
        return str(response)

    except Exception as e:
        logger.error(f"STT API call failed: {type(e).__name__} - {str(e)}")
        raise Exception(f"Speech-to-text service error: {str(e)}")

def speech_to_text_simple(
    audio_data: Union[bytes, BinaryIO],
    **kwargs
) -> str:
    """
    Simplified version that always returns a plain transcription string.
    """
    result = speech_to_text(
        audio_data=audio_data,
        response_format="text",
        **kwargs
    )
    return str(result)

# Module Test
if __name__ == "__main__":
    print("Whisper STT module initialized...")
    
    # Display current environment configuration
    print("\n=== Current STT Environment Configuration ===")
    config = get_stt_config()
    for key, value in config.items():
        if 'key' in key.lower() and value:
            print(f'{key}: ***')
        else:
            print(f'{key}: {value}')
    
    # Example usage with environment variables
    print("\n=== Example Usage ===")
    print("Using environment variables for configuration:")
    print("result = speech_to_text(audio_data)")
    print()
    print("Overriding specific parameters:")
    print("result = speech_to_text(audio_data, model='gpt-4o-transcribe', language='en')")
