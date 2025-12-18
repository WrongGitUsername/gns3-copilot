"""
OpenAI TTS Interface Module
---------------------------
This module provides a robust interface for converting text to speech using 
OpenAI-compatible APIs, specifically optimized for WAV output and automated 
duration calculation.
"""

from openai import OpenAI, APIError, AuthenticationError, RateLimitError, APIConnectionError
from typing import Optional
import io
import os
import soundfile as sf
from dotenv import load_dotenv
from gns3_copilot.log_config import setup_logger

# Load environment variables
load_dotenv()

# Setup logger
logger = setup_logger("openai_tts")

def get_tts_config():
    """
    Get TTS configuration from environment variables with sensible defaults.
    
    Returns:
        dict: Dictionary containing TTS configuration parameters.
    """
    return {
        'api_key': os.getenv('TTS_API_KEY', 'dummy-key'),
        'base_url': os.getenv('TTS_BASE_URL', 'http://localhost:4123/v1'),
        'model': os.getenv('TTS_MODEL', 'tts-1'),
        'voice': os.getenv('TTS_VOICE', 'alloy'),
        'speed': float(os.getenv('TTS_SPEED', '1.0'))
    }

def text_to_speech_wav(
    text: str,
    model: Optional[str] = None,
    voice: Optional[str] = None, 
    speed: Optional[float] = None,
    instructions: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> bytes:
    """
    Convert text to speech audio in WAV format using OpenAI TTS API.

    Args:
        text (str): The text content to convert. Max length is 4096 characters.
        model (Optional[str]): TTS model to use. Options: "tts-1", "tts-1-hd", "gpt-4o-mini-tts". 
                              If not provided, uses TTS_MODEL environment variable or "tts-1".
        voice (Optional[str]): The voice persona. Options: "alloy", "ash", "ballad", etc.
                              If not provided, uses TTS_VOICE environment variable or "alloy".
        speed (Optional[float]): Audio speed from 0.25 to 4.0. 
                                If not provided, uses TTS_SPEED environment variable or 1.0.
        instructions (Optional[str]): Voice control instructions (gpt-4o-mini-tts only).
        api_key (Optional[str]): API key for authentication. 
                                If not provided, uses TTS_API_KEY environment variable or "dummy-key".
        base_url (Optional[str]): Base URL for the API endpoint. 
                                 If not provided, uses TTS_BASE_URL environment variable or "http://localhost:4123/v1".

    Returns:
        bytes: Binary audio data in WAV format.

    Raises:
        ValueError: If input parameters are invalid.
        Exception: If API authentication, connection, or rate limits fail.
    """
    
    # Get default configuration from environment variables
    config = get_tts_config()
    
    # Use provided parameters or fall back to environment defaults
    model = model if model is not None else config['model']
    voice = voice if voice is not None else config['voice']
    speed = speed if speed is not None else config['speed']
    api_key = api_key if api_key is not None else config['api_key']
    base_url = base_url if base_url is not None else config['base_url']
    
    # 1. Basic parameter validation
    if not text or not text.strip():
        raise ValueError("Error: Text content cannot be empty.")
    
    if len(text) > 4096:
        raise ValueError(f"Error: Text length ({len(text)}) exceeds 4096 character limit.")
    
    if not (0.25 <= speed <= 4.0):
        raise ValueError("Error: Speed must be between 0.25 and 4.0.")

    # 2. Model and Voice validation
    valid_models = ["tts-1", "tts-1-hd", "gpt-4o-mini-tts"]
    if model not in valid_models:
        raise ValueError(f"Error: Unsupported model '{model}'. Valid options: {valid_models}")
    
    valid_voices = ["alloy", "ash", "ballad", "coral", "echo", "fable", "onyx", "nova", "sage", "shimmer", "verse"]
    if voice not in valid_voices:
        raise ValueError(f"Error: Unsupported voice '{voice}'. Valid options: {valid_voices}")

    # 3. Prepare API parameters (Format fixed to WAV)
    api_params = {
        "model": model,
        "voice": voice,
        "response_format": "wav",
        "input": text,
        "speed": speed,
    }
    
    # Optional instructions for specific models
    if instructions:
        if model == "gpt-4o-mini-tts":
            api_params["instructions"] = instructions
        else:
            logger.warning(f"Model {model} does not support instructions. Parameter ignored.")

    try:
        # Initialize OpenAI client
        logger.debug(f"Initializing OpenAI client with base_url: {base_url}")
        client = OpenAI(api_key=api_key, base_url=base_url)
        
        # Execute API request
        logger.info(f"Generating TTS audio using model: {model}, voice: {voice}, text length: {len(text)} characters")
        response = client.audio.speech.create(**api_params)
        logger.debug("TTS API request completed successfully")
        
        return response.content

    # 4. Comprehensive Error Handling
    except AuthenticationError as e:
        logger.error(f"Authentication failed: {e}")
        raise Exception("Authentication failed: Please check your API Key.")
    except RateLimitError as e:
        logger.error(f"Rate limit exceeded: {e}")
        raise Exception("Rate limit exceeded: Please wait before trying again.")
    except APIConnectionError as e:
        logger.error(f"Connection error: {e}")
        raise Exception("Connection error: Cannot reach the server. Check your network or base_url.")
    except APIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise Exception(f"OpenAI API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error in TTS processing: {e}")
        raise Exception(f"Unexpected error: {str(e)}")

def get_duration(audio_bytes: bytes) -> float:
    """
    Calculate the duration of WAV audio data in seconds.

    Args:
        audio_bytes (bytes): The binary audio data.

    Returns:
        float: Duration in seconds. Returns 0.0 if calculation fails.
    """
    try:
        with io.BytesIO(audio_bytes) as bio:
            data, samplerate = sf.read(bio)
            return len(data) / samplerate
    except Exception as e:
        logger.error(f"Failed to calculate duration: {e}")
        return 0.0

# --- Usage Example ---
if __name__ == "__main__":
    test_topology = (
        "Network Setup: Router 1 connects to Router 2 via Gigabit interface. "
        "The topology is now ready for OSPF configuration."
    )

    try:
        logger.info("Starting TTS test with default configuration")
        print("Generating audio...")
        print("Using environment variables for TTS configuration...")
        
        # Display current configuration
        config = get_tts_config()
        logger.info(f"TTS Configuration - Model: {config['model']}, Voice: {config['voice']}, Speed: {config['speed']}")
        print(f"TTS Model: {config['model']}")
        print(f"TTS Voice: {config['voice']}")
        print(f"TTS Speed: {config['speed']}")
        print(f"TTS Base URL: {config['base_url']}")
        print(f"TTS API Key: {'***' if config['api_key'] != 'dummy-key' else 'dummy-key'}")
        
        # Generate audio using environment variables (no explicit parameters needed)
        audio_data = text_to_speech_wav(
            text=test_topology
            # All other parameters will be loaded from .env file
        )

        duration = get_duration(audio_data)
        logger.info(f"TTS audio generated successfully, duration: {duration:.2f} seconds")
        print(f"Success! Audio Duration: {duration:.2f} seconds")

        with open("network_info.wav", "wb") as f:
            f.write(audio_data)
        logger.info("Audio file saved as network_info.wav")
        print("File saved as network_info.wav")
        
        # Example with explicit parameter override
        print("\n--- Example with parameter override ---")
        logger.info("Testing TTS with parameter override")
        audio_data_override = text_to_speech_wav(
            text=test_topology,
            voice="onyx",  # Override voice from environment
            api_key="your-api-key",  # Override API key
            base_url="http://localhost:4123/v1"  # Override base URL
        )
        logger.info("Parameter override test completed successfully")
        print("Override example completed successfully!")

    except Exception as err:
        logger.error(f"TTS test process failed: {err}")
        print(f"Process failed: {err}")
