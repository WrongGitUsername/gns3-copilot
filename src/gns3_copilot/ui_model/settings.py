"""
Streamlit-based settings management module for GNS3 Copilot application.

This module provides a comprehensive configuration interface for managing GNS3 server
connections, LLM model settings, and application preferences. It handles loading and
saving configuration to/from .env files, validates input parameters, and maintains
session state for persistent settings across the Streamlit application.

Key Features:
- GNS3 server configuration (host, URL, API version, authentication)
- LLM model provider setup with support for multiple providers
- Environment variable management and persistence
- Input validation and error handling
- Streamlit UI components for interactive configuration
"""

import os

import requests
import streamlit as st
from dotenv import find_dotenv, load_dotenv, set_key
from requests.exceptions import RequestException

from gns3_copilot.log_config import setup_logger

logger = setup_logger("settings")

# """
# .env file content
# GNS3_SERVER_HOST='127.0.0.1'
# GNS3_SERVER_URL='http://127.0.0.1:3080'
# API_VERSION='2'
# GNS3_SERVER_USERNAME=''
# GNS3_SERVER_PASSWORD=''
# MODE_PROVIDER='deepseek'
# MODEL_NAME='deepseek-chat'
# MODEL_API_KEY='your_api_key'
# BASE_URL=''
# TEMPERATURE='0.0'
# VOICE='false'
# LINUX_TELNET_USERNAME=''
# LINUX_TELNET_PASSWORD=''
# """

# config file
ENV_FILENAME = ".env"
ENV_FILE_PATH = find_dotenv(usecwd=True)

# Defines the mapping between Streamlit widget keys and their corresponding .env variable names.
# Format: {Streamlit_Key: Env_Variable_Name}
CONFIG_MAP = {
    # GNS3 Server Configuration
    "GNS3_SERVER_HOST": "GNS3_SERVER_HOST",
    "GNS3_SERVER_URL": "GNS3_SERVER_URL",
    "API_VERSION": "API_VERSION",
    "GNS3_SERVER_USERNAME": "GNS3_SERVER_USERNAME",
    "GNS3_SERVER_PASSWORD": "GNS3_SERVER_PASSWORD",
    # Model Configuration
    "MODE_PROVIDER": "MODE_PROVIDER",
    # Note: This key might require special handling (e.g., dynamic loading or mapping)
    "MODEL_NAME": "MODEL_NAME",
    "MODEL_API_KEY": "MODEL_API_KEY",  # Base API Key
    "BASE_URL": "BASE_URL",
    "TEMPERATURE": "TEMPERATURE",
    # Voice Configuration
    "VOICE": "VOICE",
    # Voice TTS Configuration
    "TTS_API_KEY": "TTS_API_KEY",
    "TTS_BASE_URL": "TTS_BASE_URL",
    "TTS_MODEL": "TTS_MODEL",
    "TTS_VOICE": "TTS_VOICE",
    "TTS_SPEED": "TTS_SPEED",
    # Voice STT Configuration
    "STT_API_KEY": "STT_API_KEY",
    "STT_BASE_URL": "STT_BASE_URL",
    "STT_MODEL": "STT_MODEL",
    "STT_LANGUAGE": "STT_LANGUAGE",
    "STT_TEMPERATURE": "STT_TEMPERATURE",
    "STT_RESPONSE_FORMAT": "STT_RESPONSE_FORMAT",
    # Other Settings
    "LINUX_TELNET_USERNAME": "LINUX_TELNET_USERNAME",
    "LINUX_TELNET_PASSWORD": "LINUX_TELNET_PASSWORD",
    # Prompt Configuration
    "ENGLISH_LEVEL": "ENGLISH_LEVEL",
}

# Example list of supported providers (used for validation during loading)
MODEL_PROVIDERS = [
    "openai",
    "anthropic",
    "azure_openai",
    "deepseek",
    "xai",
    "openrouter",
    # ... other providers
]

# Voice TTS configuration options (used for validation during loading)
TTS_MODELS = ["tts-1", "tts-1-hd", "gpt-4o-mini-tts"]
TTS_VOICES = [
    "alloy",
    "ash",
    "ballad",
    "coral",
    "echo",
    "fable",
    "onyx",
    "nova",
    "sage",
    "shimmer",
    "verse",
]

# Voice STT configuration options (used for validation during loading)
STT_MODELS = ["whisper-1", "gpt-4o-transcribe", "gpt-4o-transcribe-diarize"]
STT_RESPONSE_FORMATS = ["json", "text", "srt", "verbose_json", "vtt", "tsv"]

# If find_dotenv fails to locate the file, or if the file does not exist, attempt to create it.
if not ENV_FILE_PATH or not os.path.exists(ENV_FILE_PATH):
    # Assume the file should be located in the current working directory
    ENV_FILE_PATH = os.path.join(os.getcwd(), ENV_FILENAME)

    # If the file still does not exist, create it
    if not os.path.exists(ENV_FILE_PATH):
        try:
            # Create an empty .env file so that set_key can write to it later
            with open(ENV_FILE_PATH, "w", encoding="utf-8") as f:
                f.write(f"# Configuration file: {ENV_FILENAME}\n")
            logger.info("Created new .env file at: %s", ENV_FILE_PATH)
            st.warning(
                f"**{ENV_FILENAME}** file not found. "
                "A new file has been automatically created in the application root directory. "
                "Please configure below and click Save."
            )
        except Exception as e:
            logger.error("Failed to create %s file: %s", ENV_FILENAME, e)
            st.error(
                f"Failed to create {ENV_FILENAME} file. "
                f"Save function will be disabled. Error: {e}"
            )
            ENV_FILE_PATH = ""


def load_config_from_env() -> None:
    """Load configuration from the .env file and initialize st.session_state."""
    # Only attempt to load if the path is valid and the file exists
    logger.info("Starting to load configuration from .env file")
    if ENV_FILE_PATH and os.path.exists(ENV_FILE_PATH):
        logger.debug("Loading .env file from: %s", ENV_FILE_PATH)
        load_dotenv(ENV_FILE_PATH)
        logger.info("Successfully loaded .env file")
    else:
        logger.warning(".env file not found at: %s", ENV_FILE_PATH)

    # Load environment variables into Streamlit's session state
    for st_key, env_key in CONFIG_MAP.items():
        # Get the value from os.environ; default to an empty string if not found
        env_value = os.getenv(env_key)
        default_value = env_value if env_value is not None else ""

        # Special handling for API_VERSION (kept consistent)
        if st_key == "API_VERSION":
            # Ensure the default value is either "2" or "3"
            default_value = "2" if default_value not in ["2", "3"] else default_value

        # Special handling for MODE_PROVIDER (updated key name)
        if st_key == "MODE_PROVIDER":
            if default_value not in MODEL_PROVIDERS:
                # If the loaded value is not in the supported list,
                # set it to an empty string for the user to select
                logger.warning(
                    "Unsupported MODE_PROVIDER %s, setting to empty", default_value
                )
                default_value = ""

        # Special handling for TEMPERATURE (Ensure default is a number or empty string)
        if st_key == "TEMPERATURE" and not default_value.replace(".", "", 1).isdigit():
            # Provide a reasonable default value if not set or invalid
            logger.debug(
                "Invalid TEMPERATURE value : %s, setting to default '0.0'",
                default_value,
            )
            default_value = "0.0"

        # Special handling for VOICE (boolean)
        if st_key == "VOICE":
            # 确保 default_value 是字符串后再进行处理
            voice_str = str(default_value).lower().strip()

            if voice_str not in (
                "true",
                "false",
                "1",
                "0",
                "yes",
                "no",
                "on",
                "off",
                "",
            ):
                logger.debug(
                    "Invalid VOICE value: %s, setting to default 'false'", default_value
                )
                voice_str = "false"

            # 直接计算布尔值并存入 session_state
            is_enabled: bool = voice_str in ("true", "1", "yes", "on")
            st.session_state[st_key] = is_enabled

            logger.debug("Loaded config: %s = %s", st_key, is_enabled)
            continue  # 重要：处理完布尔类型后跳过本次循环，防止被最后的通用赋值覆盖

        # Special handling for TTS configuration
        if st_key == "TTS_MODEL" and default_value not in TTS_MODELS:
            logger.warning("Unsupported TTS_MODEL %s, setting to empty", default_value)
            default_value = ""

        if st_key == "TTS_VOICE" and default_value not in TTS_VOICES:
            logger.warning("Unsupported TTS_VOICE %s, setting to empty", default_value)
            default_value = ""

        if st_key == "TTS_SPEED":
            try:
                speed_float = float(default_value)
                if not (0.25 <= speed_float <= 4.0):
                    logger.debug(
                        "Invalid TTS_SPEED value: %s, setting to default '1.0'",
                        default_value,
                    )
                    default_value = "1.0"
            except ValueError:
                logger.debug(
                    "Invalid TTS_SPEED value: %s, setting to default '1.0'",
                    default_value,
                )
                default_value = "1.0"

        # Special handling for STT configuration
        if st_key == "STT_MODEL" and default_value not in STT_MODELS:
            logger.warning("Unsupported STT_MODEL %s, setting to empty", default_value)
            default_value = ""

        if (
            st_key == "STT_RESPONSE_FORMAT"
            and default_value not in STT_RESPONSE_FORMATS
        ):
            logger.warning(
                "Unsupported STT_RESPONSE_FORMAT %s, setting to empty", default_value
            )
            default_value = ""

        if st_key == "STT_TEMPERATURE":
            try:
                temp_float = float(default_value)
                if not (0.0 <= temp_float <= 1.0):
                    logger.debug(
                        "Invalid STT_TEMPERATURE value: %s, setting to default '0.0'",
                        default_value,
                    )
                    default_value = "0.0"
            except ValueError:
                logger.debug(
                    "Invalid STT_TEMPERATURE value: %s, setting to default '0.0'",
                    default_value,
                )
                default_value = "0.0"

        # Set the value in session state
        st.session_state[st_key] = default_value
        logger.debug(
            "Loaded config: %s = %s",
            st_key,
            "[HIDDEN]" if "PASSWORD" in st_key or "KEY" in st_key else default_value,
        )
    logger.info("Configuration loading completed")


def save_config_to_env() -> None:
    """Save the current session state to the .env file."""
    # Prevent saving if the .env file path is invalid
    logger.info("Starting to save configuration to .env file")

    # Initialize saved_count counter
    saved_count = 0

    if not ENV_FILE_PATH:
        logger.error("Cannot save configuration: .env file path is invalid")
        st.error("Cannot save configuration because the .env file path is invalid.")
        return

    for st_key, env_key in CONFIG_MAP.items():
        current_value = st.session_state.get(st_key)

        if current_value is not None:
            str_value = str(current_value)

            try:
                # Save the value back to the .env file
                set_key(ENV_FILE_PATH, env_key, str_value)

                # Immediately update the current Python process's environment variables
                os.environ[env_key] = str_value

                saved_count += 1
                logger.debug(
                    "Saved config: %s = %s",
                    st_key,
                    "[HIDDEN]"
                    if "PASSWORD" in st_key or "KEY" in st_key
                    else str_value,
                )
            except Exception as e:
                logger.error("Failed to save %s: %s", st_key, e)

    logger.info(
        "Configuration save completed. Saved %s configuration items to %s",
        saved_count,
        ENV_FILE_PATH,
    )
    st.success("Configuration successfully saved to the .env file!")


def check_gns3_api() -> None:
    """
    Check whether the GNS3 API is reachable using the provided configuration.
    """
    logger.info("Starting GNS3 API check.")

    version: str = str(st.session_state.get("API_VERSION", "2"))

    required_fields = {
        "GNS3_SERVER_HOST": "GNS3 Server Host",
        "GNS3_SERVER_URL": "GNS3 Server URL",
        "API_VERSION": "API Version",
    }

    # Add auth fields for API v3
    if version == "3":
        required_fields.update(
            {
                "GNS3_SERVER_USERNAME": "GNS3 Server Username",
                "GNS3_SERVER_PASSWORD": "GNS3 Server Password",
            }
        )

    # Detect missing fields
    missing_fields = [
        label for key, label in required_fields.items() if not st.session_state.get(key)
    ]

    if missing_fields:
        message = "Please fill out the following fields:\n\n"
        message += "\n".join(f" - {field}" for field in missing_fields)
        logger.warning("Missing fields detected: %s", ", ".join(missing_fields))
        st.error(message)
        return

    # Extract validated values
    url: str = st.session_state.get("GNS3_SERVER_URL", "")
    auth: tuple[str, str] | None = None

    if version == "3":
        u = st.session_state.get("GNS3_SERVER_USERNAME", "")
        p = st.session_state.get("GNS3_SERVER_PASSWORD", "")
        if u and p:
            auth = (u, p)

    logger.debug(
        "Checking GNS3 API", extra={"url": url, "version": version, "auth": bool(auth)}
    )

    try:
        response = requests.get(url, auth=auth, timeout=5)
        response.raise_for_status()

        logger.info("Successfully connected to the GNS3 API at %s", url)
        st.success(f"Successfully connected to the GNS3 API at {url}")

    except RequestException as exc:
        logger.error(f"Failed to connect to the GNS3 API: {exc}")
        st.error(f"Failed to connect to the GNS3 API: {exc}")


# Initialization
if "GNS3_SERVER_HOST" not in st.session_state:
    logger.info("Initializing Settings page - loading configuration")
    load_config_from_env()
else:
    logger.debug("Settings page already initialized")

# Streamlit UI
st.title("GNS3 Copilot Settings")
st.info(f"Configuration file path: **{ENV_FILE_PATH}**")

with st.expander("🔧 GNS3 API Settings", expanded=True):
    # GNS3 Server address/API point
    col1, col2 = st.columns([1, 2])
    with col1:
        st.text_input(
            "GNS3 Server Host *",
            key="GNS3_SERVER_HOST",
            type="default",
            placeholder="E.g., 127.0.0.1",
        )
    with col2:
        st.text_input(
            "GNS3 Server URL *",
            key="GNS3_SERVER_URL",
            type="default",
            placeholder="E.g., http://127.0.0.1:3080 or http://127.0.0.1:8000",
        )

    # GNS3 API version select
    col1, col2, col3 = st.columns([1, 2, 2])
    with col1:
        st.selectbox("GNS3 API Version", ["2", "3"], key="API_VERSION")

    if st.session_state.get("API_VERSION") == "3":
        with col2:
            st.text_input(
                "GNS3 User *",
                key="GNS3_SERVER_USERNAME",
                type="default",
                placeholder="E.g., admin",
            )
        with col3:
            st.text_input(
                "GNS3 Password *",
                key="GNS3_SERVER_PASSWORD",
                type="password",
                placeholder="E.g., admin",
            )
    else:
        pass

    # Button to manually check if GNS3 API is reachable
    if st.button("Check GNS3 API"):
        check_gns3_api()

with st.expander("🤖 LLM Model Configuration", expanded=True):
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        # LLM Model Provider
        st.text_input(
            "Model Provider *",  # Updated to use * for required field
            key="MODE_PROVIDER",
            type="default",
            help="""
    Supported model_provider values and the corresponding integration package are:

    openai,
    anthropic,
    ollama,
    deepseek,
    xai...

    If using the 'OpenRouter' platform, please enter 'openai' here.
            """,
            placeholder="e.g. 'deepseek', 'openai'",
        )

    with col2:
        # LLM Model Name
        st.text_input(
            "Model Name *",
            key="MODEL_NAME",
            type="default",
            help="""
The name or ID of the model, e.g. 'o3-mini', 'claude-sonnet-4-5-20250929', 'deepseek-caht'.

If using the OpenRouter platform,
please enter the model name in the OpenRouter format,
e.g.: 'openai/gpt-4o-mini', 'x-ai/grok-4-fast'.
            """,
            placeholder="e.g. 'o3-mini', 'claude-sonnet-4-5-20250929', 'deepseek-caht'",
        )

    with col3:
        # LLM model temperature
        st.text_input(
            "Model Temperature",
            key="TEMPERATURE",
            type="default",
            help="""
Controls randomness: higher values mean more random output. Typical range is 0.0 to 1.0.
            """,
        )

    # LLM model provider base url
    st.text_input(
        "Base Url",
        key="BASE_URL",
        type="default",
        help="""
To use OpenRouter, the Base Url must be entered, e.g., https://openrouter.ai/api/v1.
        """,
        placeholder="e.g., OpenRouter https://openrouter.ai/api/v1",
    )

    # LLM API KEY
    st.text_input(
        "Model API Key *",
        key="MODEL_API_KEY",
        type="password",
        help="""
The key required for authenticating with the model's provider.
This is usually issued when you sign up for access to the model.
        """,
    )

with st.expander("🎤 Voice Settings (TTS/STT)", expanded=True):
    # Voice Enable/Disable Toggle
    st.subheader("Voice Control")
    voice_enabled = st.checkbox(
        "Enable Voice Features (TTS/STT)",
        value=st.session_state.get("VOICE", False),
        help="""
Enable or disable voice features including:
- **Text-to-Speech (TTS)**: Convert AI responses to speech
- **Speech-to-Text (STT)**: Convert voice input to text

When disabled, all voice-related settings below will be hidden.
        """,
    )

    # Update session state with boolean value
    st.session_state["VOICE"] = voice_enabled

    # Show voice settings only when voice is enabled
    if voice_enabled:
        st.markdown("---")  # Separator

        # TTS Configuration Section
        st.subheader("Text-to-Speech (TTS) Configuration")

        # TTS First row: API Key, Model, Voice
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.text_input(
                "TTS API Key",
                key="TTS_API_KEY",
                type="password",
                help="""
API key for TTS service authentication.
Leave empty for local/dummy services.
                """,
                placeholder="Enter your TTS API key",
            )
        with col2:
            st.selectbox(
                "TTS Model",
                options=[""] + TTS_MODELS,
                key="TTS_MODEL",
                help="""
Select the TTS model to use:
- **tts-1**: Standard quality, faster
- **tts-1-hd**: High quality, slower
- **gpt-4o-mini-tts**: Latest model with voice instructions support
                """,
            )
        with col3:
            st.selectbox(
                "TTS Voice",
                options=[""] + TTS_VOICES,
                key="TTS_VOICE",
                help="""
Select the voice persona for TTS output.
Different voices have different tones and characteristics.
                """,
            )

        # TTS Second row: Base URL and Speed
        col1, col2 = st.columns([2, 1])
        with col1:
            st.text_input(
                "TTS Base URL",
                key="TTS_BASE_URL",
                type="default",
                help="""
Base URL for the TTS API endpoint.
Use local TTS service endpoints like http://localhost:4123/v1
                """,
                placeholder="e.g., http://localhost:4123/v1",
            )
        with col2:
            st.slider(
                "TTS Speed",
                min_value=0.25,
                max_value=4.0,
                value=1.0,
                step=0.25,
                key="TTS_SPEED",
                help="""
Controls the speed of speech synthesis:
- 0.25: Very slow
- 1.0: Normal speed
- 4.0: Very fast
                """,
            )

        # STT Configuration Section
        st.markdown("---")  # Separator
        st.subheader("Speech-to-Text (STT) Configuration")

        # STT First row: API Key, Model, Language
        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.text_input(
                "STT API Key",
                key="STT_API_KEY",
                type="password",
                help="""
API key for STT service authentication.
Leave empty for local/dummy services.
                """,
                placeholder="Enter your STT API key",
            )
        with col2:
            st.selectbox(
                "STT Model",
                options=[""] + STT_MODELS,
                key="STT_MODEL",
                help="""
Select the STT model to use:
- **whisper-1**: Standard Whisper model
- **gpt-4o-transcribe**: GPT-4 based transcription
- **gpt-4o-transcribe-diarize**: With speaker diarization
                """,
            )
        with col3:
            st.text_input(
                "STT Language",
                key="STT_LANGUAGE",
                type="default",
                help="""
ISO 639-1 language code (e.g., 'en', 'zh', 'ja').
Leave empty for auto-detection.
                """,
                placeholder="e.g., en, zh, ja (optional)",
            )

        # STT Second row: Base URL, Temperature, Response Format
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.text_input(
                "STT Base URL",
                key="STT_BASE_URL",
                type="default",
                help="""
Base URL for the STT API endpoint.
Use local STT service endpoints like http://127.0.0.1:8001/v1
                """,
                placeholder="e.g., http://127.0.0.1:8001/v1",
            )
        with col2:
            st.slider(
                "STT Temperature",
                min_value=0.0,
                max_value=1.0,
                value=0.0,
                step=0.1,
                key="STT_TEMPERATURE",
                help="""
Controls randomness in transcription:
- 0.0: Deterministic, most accurate
- 1.0: More creative, less accurate
                """,
            )
        with col3:
            st.selectbox(
                "STT Response Format",
                options=[""] + STT_RESPONSE_FORMATS,
                key="STT_RESPONSE_FORMAT",
                help="""
Output format for transcription results:
- **json**: Standard JSON with text
- **text**: Plain text only
- **verbose_json**: JSON with timestamps
- **srt/vtt**: Subtitle formats
                """,
            )
    else:
        st.info(
            "💡 **Voice features are currently disabled.** Enable the toggle above to configure TTS/STT settings."
        )

with st.expander("⚙️ Other Settings", expanded=True):
    english_levels = ["Normal Prompt", "A1", "A2", "B1", "B2", "C1", "C2"]
    st.selectbox(
        "English Level",
        options=english_levels,
        key="ENGLISH_LEVEL",
        help="""
Select your English proficiency level based on the CEFR (Common European Framework of Reference for Languages) framework:

**CEFR English Levels:**
- **A1 (Beginner)**: Basic phrases, simple network terminology
- **A2 (Elementary)**: Simple sentences, common network concepts
- **B1 (Intermediate)**: Complex sentences, technical explanations
- **B2 (Upper-Intermediate)**: Professional network terminology
- **C1 (Advanced)**: Expert-level network discussions
- **C2 (Proficiency)**: Native-level technical communication

**Auto Select**: Uses the standard network automation prompt (React Prompt) optimized for general technical users

The system will adjust prompt complexity, vocabulary, and explanation style based on your selected level.
""",
    )

    col1, col2 = st.columns([1, 1])
    with col1:
        st.text_input(
            "Linux Console Username",
            key="LINUX_TELNET_USERNAME",
            placeholder="E.g., debian",
            type="default",
            help="""
Use gns3 debian linux.

https://www.gns3.com/marketplace/appliances/debian-2
            """,
        )
    with col2:
        st.text_input(
            "Linux Console Password",
            key="LINUX_TELNET_PASSWORD",
            placeholder="E.g., debian",
            type="password",
        )

if ENV_FILE_PATH:
    st.button("Save Settings to .env", on_click=save_config_to_env)
else:
    # Cannot find or create the .env file, so the save button is disabled.
    st.error(
        "Could not find or create the .env file, so the save button has been disabled."
    )
