import streamlit as st
import toml
import os
from typing import Dict, Any


st.title("Settings(Not effective)")

# GNS3 Server address/API point
col1, col2 = st.columns([1,2])
with col1:
    st.text_input(
        "GNS3 Server Host",
        key="GNS3_SERVER_HOST",
        type="default",
        placeholder="E.g., 127.0.0.1") 
with col2:
    st.text_input(
        "GNS3 Server URL",
        key="GNS3_SERVER_URL",
        type="default",
        placeholder="E.g., http://127.0.0.1:3080 or http://127.0.0.1:8000")

# GNS3 API version select
col1, col2, col3 = st.columns([1,2,2])
with col1:
    api_version = st.selectbox("GNS3 API Version", ["2", "3"], key="API_VERSION")
if st.session_state["API_VERSION"] == "3":
    with col2:
        st.text_input(
            "GNS3 User",
            key="GNS3_SERVER_USERNAME",
            type="default",
            placeholder="E.g., admin"
            )
    with col3:
        st.text_input(
            "GNS3 Passwd",
            key="GNS3_SERVER_PASSWORD",
            type="password",
            placeholder="E.g., admin"
            )
else:
    pass

# Define a list of all supported providers (using constants is good practice)
MODEL_PROVIDERS = [
    "DeepSeek", 
    "OpenAI", 
    "Xai", 
    "OpenRouter",
]
col1, col2 = st.columns([1,3])
with col1:
    # Select LLM model provider
    model_provider = st.selectbox(
        "Model Provider",
        MODEL_PROVIDERS,
        key="model_provider"
    )
with col2:
    # Check if a provider has been selected (i.e., the session state is initialized).
    # Since the action is the same for ALL providers, we only need to check once.
    if st.session_state.get("model_provider") == "OpenRouter":
        st.text_input(
            "Model Name", 
            key="model_name", 
            placeholder=f"E.g., use 'openai/gpt-4o-mini' or 'x-ai/grok-4-fast'",
        )
    if st.session_state.get("model_provider") == "Xai":
        st.text_input(
            "Model Name", 
            key="model_name", 
            placeholder=f"E.g., use 'grok-4-fast'",
        )
    if st.session_state.get("model_provider") == "OpenAI":
        st.text_input(
            "Model Name", 
            key="model_name", 
            placeholder=f"E.g., use 'gpt-4o-mini'",
        )    
    if st.session_state.get("model_provider") == "DeepSeek":
        st.selectbox(
            "Model Name",
            ["deepseek-chat"],
            key="model_name", 
        )    

# LLM API KEY
st.text_input("Model API Key", key="MODEL_API_KEY", type="password")

st.header("Other Settings")

col1, col2 = st.columns([1,1])
with col1:
    st.text_input(
        "Linux Console Username",
        key="LINUX_TELNET_USERNAME",
        placeholder="E.g., debian",
        type="default"
    )
with col2:
    st.text_input(
        "Linux Console Username",
        key="LINUX_TELNET_PASSWORD",
        placeholder="E.g., debian",
        type="password"
    )