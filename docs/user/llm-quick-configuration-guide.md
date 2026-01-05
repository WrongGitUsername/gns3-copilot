# LLM Quick Configuration Guide

## Overview

GNS3 Copilot provides a streamlined LLM configuration experience through predefined provider configurations. This feature significantly reduces the complexity of setting up LLM providers, especially for new users.

## Quick Configuration Feature

The Settings page now includes a "Quick Configuration" section that allows you to select from predefined LLM providers with automatic configuration filling.

### Supported Provider Categories

#### 🔗 Aggregator Platforms
- **OpenRouter**: Multi-provider aggregator
  - Base URL: `https://openrouter.ai/api/v1`
  - API key required
  - Popular models:
    - openai/gpt-4o-mini
    - openai/gpt-4o
    - anthropic/claude-3.5-sonnet
    - deepseek/deepseek-chat
    - google/gemini-flash-1.5

#### 🏢 First-Party Providers
- **OpenAI**: Official OpenAI API
  - Base URL: `https://api.openai.com/v1`
  - API key required
  - Models: gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-3.5-turbo, o1-mini, o1-preview

- **DeepSeek**: DeepSeek AI
  - Base URL: `https://api.deepseek.com/v1`
  - API key required
  - Models: deepseek-chat, deepseek-coder

- **Anthropic**: Claude models
  - Base URL: `https://api.anthropic.com/v1`
  - API key required
  - Models: claude-3.5-sonnet, claude-3.5-haiku, claude-3-opus

- **Google**: Gemini models
  - Base URL: `https://generativelanguage.googleapis.com/v1beta`
  - API key required
  - Models: gemini-1.5-flash, gemini-1.5-pro, gemini-1.0-pro

- **xAI**: Grok models
  - Base URL: `https://api.x.ai/v1`
  - API key required
  - Models: grok-beta, grok-2-vision

## How to Use Quick Configuration

### Step 1: Navigate to Settings
1. Open GNS3 Copilot
2. Click on the "Settings" page in the sidebar

### Step 2: Select a Provider
1. In the "LLM Model Configuration" section, locate "Quick Configuration"
2. Click the "Select LLM Provider" dropdown
3. Choose your desired provider from the list

### Step 3: Select a Model
1. After selecting a provider, a model list will appear
2. Select a model from the dropdown or choose "Custom model name..." to enter manually

### Step 4: Enter API Key
1. All providers require an API key
2. Enter your API key in the "Model API Key" field

### Step 5: Save Configuration
1. Click "Save Settings to .env"
2. Your configuration is now saved and ready to use

## Manual Configuration

For advanced users who need custom configurations:

1. Select "Custom" from the provider dropdown
2. Or use the "Manual Configuration" section below the quick configuration
3. Manually enter:
   - Model Provider (e.g., openai, anthropic, deepseek)
   - Model Name (e.g., gpt-4o-mini, claude-3.5-sonnet)
   - Base URL (if applicable)
   - Model API Key (if required)
   - Model Temperature (optional, default is 0.7)

## Adding New Providers

To add a new predefined provider, edit `src/gns3_copilot/ui_model/utils/llm_providers.py`:

```python
from gns3_copilot.ui_model.utils.llm_providers import LLM_PROVIDERS

LLM_PROVIDERS["New Provider"] = ProviderConfig(
    provider="provider_type",  # e.g., openai, anthropic
    base_url="https://api.provider.com/v1",
    models=["model1", "model2", "model3"],
    requires_api_key=True,
    category="first_party",  # or "aggregator"
)
```

## Troubleshooting

### Provider Not Working
- Verify the base URL is correct
- Check if API key is valid (if required)
- Ensure the service is accessible from your network
- Check provider documentation for any changes

### API Key Issues
- Ensure you've copied the full API key
- Check if the key has sufficient permissions
- Verify the key hasn't expired
- Check provider documentation for key format requirements

## Best Practices

1. **Start with Entry-Level Models**: Use models like gpt-4o-mini for testing and initial setup
2. **Check Documentation**: Always review provider documentation for model capabilities
3. **Save Configurations**: Save working configurations in case you need to revert
4. **Monitor Usage**: Keep track of token usage to manage costs

## Configuration Persistence

All configurations are saved to the `.env` file in your project directory. The file includes:
- MODE_PROVIDER
- MODEL_NAME
- BASE_URL
- MODEL_API_KEY
- TEMPERATURE

You can also manually edit the `.env` file if needed.

## Related Documentation

- [GNS3 Copilot User Guide](../README.md)
- [API Documentation](../docs/)
- [Contributing Guide](../CONTRIBUTING.md)
