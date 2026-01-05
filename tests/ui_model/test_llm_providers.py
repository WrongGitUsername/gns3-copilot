"""
Tests for LLM provider configuration module.

Tests verify that provider configurations are properly defined and accessible,
and that utility functions work as expected.
"""

import pytest

from gns3_copilot.ui_model.utils.llm_providers import (
    LLM_PROVIDERS,
    ProviderConfig,
    get_all_providers,
    get_provider_config,
)


class TestProviderConfig:
    """Tests for ProviderConfig class."""

    def test_provider_config_initialization(self):
        """Test that ProviderConfig initializes correctly."""
        config = ProviderConfig(
            provider="test_provider",
            base_url="https://api.test.com/v1",
            models=["model1", "model2"],
            requires_api_key=True,
            category="first_party",
        )

        assert config.provider == "test_provider"
        assert config.base_url == "https://api.test.com/v1"
        assert config.models == ["model1", "model2"]
        assert config.requires_api_key is True
        assert config.category == "first_party"


class TestLLMProviders:
    """Tests for LLM_PROVIDERS dictionary."""

    def test_llm_providers_is_not_empty(self):
        """Test that LLM_PROVIDERS contains entries."""
        assert len(LLM_PROVIDERS) > 0

    def test_all_providers_are_providerconfig(self):
        """Test that all entries in LLM_PROVIDERS are ProviderConfig instances."""
        for name, config in LLM_PROVIDERS.items():
            assert isinstance(config, ProviderConfig)
            assert isinstance(name, str)

    def test_required_fields_present(self):
        """Test that all providers have required fields."""
        required_fields = ["provider", "base_url", "models", "requires_api_key", "category"]

        for config in LLM_PROVIDERS.values():
            for field in required_fields:
                assert hasattr(config, field)
                assert getattr(config, field) is not None

    def test_models_are_lists(self):
        """Test that models field is always a list."""
        for config in LLM_PROVIDERS.values():
            assert isinstance(config.models, list)
            assert len(config.models) > 0

    def test_openrouter_config(self):
        """Test OpenRouter provider configuration."""
        openrouter = LLM_PROVIDERS.get("OpenRouter")
        assert openrouter is not None
        assert openrouter.provider == "openai"
        assert openrouter.base_url == "https://openrouter.ai/api/v1"
        assert openrouter.category == "aggregator"
        assert openrouter.requires_api_key is True
        assert len(openrouter.models) > 0

    def test_deepseek_config(self):
        """Test DeepSeek provider configuration."""
        deepseek = LLM_PROVIDERS.get("DeepSeek")
        assert deepseek is not None
        assert deepseek.provider == "deepseek"
        assert deepseek.base_url == "https://api.deepseek.com/v1"
        assert deepseek.category == "first_party"
        assert deepseek.requires_api_key is True


class TestUtilityFunctions:
    """Tests for utility functions."""

    def test_get_provider_config_existing(self):
        """Test get_provider_config with existing provider."""
        config = get_provider_config("OpenRouter")
        assert config is not None
        assert isinstance(config, ProviderConfig)
        assert config.provider == "openai"

    def test_get_provider_config_nonexistent(self):
        """Test get_provider_config with nonexistent provider."""
        config = get_provider_config("NonExistentProvider")
        assert config is None

    def test_get_all_providers_returns_list(self):
        """Test that get_all_providers returns a list."""
        providers = get_all_providers()
        assert isinstance(providers, list)

    def test_get_all_providers_contains_known_providers(self):
        """Test that get_all_providers contains known providers."""
        providers = get_all_providers()
        assert "OpenRouter" in providers
        assert "DeepSeek" in providers
