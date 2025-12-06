import streamlit as st
import os
from dotenv import load_dotenv, set_key, find_dotenv

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
    "MODEL_NAME": "MODEL_NAME",   # Note: This key might require special handling (e.g., dynamic loading or mapping)
    "MODEL_API_KEY": "MODEL_API_KEY", # Base API Key
    "BASE_URL":"BASE_URL",
    "TEMPERATURE":"TEMPERATURE",
    # Other Settings
    "LINUX_TELNET_USERNAME": "LINUX_TELNET_USERNAME",
    "LINUX_TELNET_PASSWORD": "LINUX_TELNET_PASSWORD",
}

# Example list of supported providers (used for validation during loading)
MODEL_PROVIDERS = [
    "openai", "anthropic", "azure_openai", 
    "deepseek", "xai", "openrouter",
    # ... other providers
]

# If find_dotenv fails to locate the file, or if the file does not exist, attempt to create it.
if not ENV_FILE_PATH or not os.path.exists(ENV_FILE_PATH):
    # Assume the file should be located in the current working directory
    ENV_FILE_PATH = os.path.join(os.getcwd(), ENV_FILENAME)
    
    # If the file still does not exist, create it
    if not os.path.exists(ENV_FILE_PATH):
        try:
            # Create an empty .env file so that set_key can write to it later
            with open(ENV_FILE_PATH, 'w') as f:
                f.write(f"# Configuration file: {ENV_FILENAME}\n")
            st.warning(f"**{ENV_FILENAME}** file not found. A new file has been automatically created in the application root directory. Please configure below and click Save.")
        except Exception as e:
            st.error(f"Failed to create {ENV_FILENAME} file. Save function will be disabled. Error: {e}")
            ENV_FILE_PATH = None
            
def load_config_from_env():
    """Load configuration from the .env file and initialize st.session_state."""
    # Only attempt to load if the path is valid and the file exists
    if ENV_FILE_PATH and os.path.exists(ENV_FILE_PATH):
        load_dotenv(ENV_FILE_PATH)
    
    # Load environment variables into Streamlit's session state
    for st_key, env_key in CONFIG_MAP.items():
        # Get the value from os.environ; default to an empty string if not found
        default_value = os.getenv(env_key) if os.getenv(env_key) is not None else ""
        
        # Special handling for API_VERSION (kept consistent)
        if st_key == "API_VERSION":
            # Ensure the default value is either "2" or "3"
            default_value = "2" if default_value not in ["2", "3"] else default_value
        
        # Special handling for MODE_PROVIDER (updated key name)
        if st_key == "MODE_PROVIDER":
            if default_value not in MODEL_PROVIDERS:
                 # If the loaded value is not in the supported list, set it to an empty string for the user to select
                 default_value = ""
        
        # Special handling for TEMPERATURE (Ensure default is a number or empty string)
        if st_key == "TEMPERATURE" and not default_value.replace('.', '', 1).isdigit():
            # Provide a reasonable default value if not set or invalid
            default_value = "0.0" 

        # Set the value in session state
        st.session_state[st_key] = default_value

def save_config_to_env():
    """Save the current session state to the .env file."""
    # Prevent saving if the .env file path is invalid
    if not ENV_FILE_PATH:
        st.error("Cannot save configuration because the .env file path is invalid.")
        return
        
    for st_key, env_key in CONFIG_MAP.items():
        current_value = st.session_state.get(st_key)
        
        if current_value is not None:
            str_value = str(current_value)
            
            # Save the value back to the .env file
            set_key(ENV_FILE_PATH, env_key, str_value)
            
            # Immediately update the current Python process's environment variables
            os.environ[env_key] = str_value
            
    st.success("Configuration successfully saved to the .env file!")
            
# Initialization
if 'GNS3_SERVER_HOST' not in st.session_state:
    load_config_from_env()

# Streamlit UI
st.title("GNS3 Settings")
st.info(f"Configuration file path: **{ENV_FILE_PATH}**")

# GNS3 Server address/API point
col1, col2 = st.columns([1,2])
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
col1, col2, col3 = st.columns([1,2,2])
with col1:
    st.selectbox(
        "GNS3 API Version", 
        ["2", "3"], 
        key="API_VERSION"
    )

if st.session_state.get("API_VERSION") == "3":
    with col2:
        st.text_input(
            "GNS3 User *",
            key="GNS3_SERVER_USERNAME",
            type="default",
            placeholder="E.g., admin"
            )
    with col3:
        st.text_input(
            "GNS3 Passwd *",
            key="GNS3_SERVER_PASSWORD",
            type="password",
            placeholder="E.g., admin"
            )
else:
    pass

st.header("LLM Model Configuration")
col1, col2, col3 = st.columns([1,2,1])

with col1:
    # LLM Model Provider
    st.text_input(
        "Model Provider *", # Updated to use * for required field
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
        placeholder="e.g. 'deepseek', 'openai'"
    )
    
with col2:
    # LLM Model Name
    st.text_input(
        "Model Name *",
        key="MODEL_NAME",
        type="default",
        help="""
The name or ID of the model, e.g. 'o3-mini', 'claude-sonnet-4-5-20250929', 'deepseek-caht'.
    
If using the OpenRouter platform, please enter the model name in the OpenRouter format, e.g.: 'openai/gpt-4o-mini', 'x-ai/grok-4-fast'.
        """,
        placeholder="e.g. 'o3-mini', 'claude-sonnet-4-5-20250929', 'deepseek-caht'"
    )
    
with col3:
    # LLM model temperature
    st.text_input(
        "Model Temperature", 
        key="TEMPERATURE", 
        type="default",
        help="""
Controls randomness: higher values mean more random output. Typical range is 0.0 to 1.0.
        """
    )

# LLM model provider base url
st.text_input(
    "Base Url", 
    key="BASE_URL", 
    type="default",
    help="""
To use OpenRouter, the Base Url must be entered, e.g., https://openrouter.ai/api/v1.
    """,
    placeholder="e.g., OpenRouter https://openrouter.ai/api/v1"
)

# LLM API KEY
st.text_input(
    "Model API Key *", 
    key="MODEL_API_KEY", 
    type="password",
    help="""
The key required for authenticating with the model’s provider. This is usually issued when you sign up for access to the model. 
    """
)

st.header("Other Settings")

col1, col2 = st.columns([1,1])
with col1:
    st.text_input(
        "Linux Console Username",
        key="LINUX_TELNET_USERNAME",
        placeholder="E.g., debian",
        type="default",
        help="""
Use gns3 debian linux. 

https://www.gns3.com/marketplace/appliances/debian-2
        """
    )
with col2:
    st.text_input(
        "Linux Console Password",
        key="LINUX_TELNET_PASSWORD",
        placeholder="E.g., debian",
        type="password"
    )

if ENV_FILE_PATH:
    st.button("Save Settings to .env", on_click=save_config_to_env)
else:
    # Cannot find or create the .env file, so the save button is disabled.
    st.error("Could not find or create the .env file, so the save button has been disabled.")