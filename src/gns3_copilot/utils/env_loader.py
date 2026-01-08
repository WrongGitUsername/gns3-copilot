"""
Environment variable loader module.

This module provides a unified interface for loading and retrieving environment variables,
ensuring that environment variables are reloaded on each access to support dynamic configuration changes.
"""

# mypy: ignore-errors

import os
import time
from typing import Any

from dotenv import load_dotenv

from gns3_copilot.log_config import setup_logger

logger = setup_logger("env_loader")

# Cache for loaded environment variables and timestamp
_env_cache: dict[str, Any] = {}
_last_load_time: float = 0
_CACHE_TTL: int = 1  # Cache TTL in seconds (0 means always reload)


def load_env_variables(force_reload: bool = False) -> None:  # noqa: C901,PLR0912
    """
    Load environment variables from .env file.

    This function loads environment variables from the .env file and caches them.
    The cache is valid for CACHE_TTL seconds, after which it will be reloaded automatically.

    Args:
        force_reload: If True, force reload even if cache is still valid
    """
    global _env_cache, _last_load_time

    current_time = time.time()

    # Check if we should skip reload (cache is valid and not forcing reload)
    cache_valid = (
        not force_reload
        and _last_load_time > 0
        and _CACHE_TTL > 0
        and (current_time - _last_load_time) < _CACHE_TTL
    )

    if cache_valid:
        cache_age = current_time - _last_load_time
        logger.debug(
            "Using cached environment variables (age: %.2fs, TTL: %ds)",
            cache_age,
            _CACHE_TTL,
        )
        return

    # Reload environment variables
    logger.debug("Reloading environment variables from .env file")
    dotenv_loaded = load_dotenv(override=True)

    if dotenv_loaded:
        logger.info("Successfully loaded environment variables from .env file")
    else:
        logger.warning(
            "No .env file found or failed to load. Using existing environment variables."
        )

    _last_load_time = current_time


def get_env_var(key: str, default: Any | None = None) -> Any | None:
    """
    Get environment variable value, loading .env file if needed.

    Args:
        key: Environment variable name
        default: Default value if key not found

    Returns:
        Environment variable value or default
    """
    # Ensure environment variables are loaded
    load_env_variables()

    return os.getenv(key, default)


def get_nornir_all_groups_config() -> dict[str, dict[str, Any]]:
    """
    Get all Nornir groups configuration for network devices.

    Returns:
        Dictionary containing all Nornir group configurations
    """
    # Ensure environment variables are loaded
    load_env_variables()

    return {
        "cisco_IOSv_telnet": {
            "platform": "cisco_ios",
            "hostname": os.getenv("GNS3_SERVER_HOST"),
            "timeout": 120,
            "username": os.getenv("GNS3_SERVER_USERNAME"),
            "password": os.getenv("GNS3_SERVER_PASSWORD"),
            "connection_options": {
                "netmiko": {"extras": {"device_type": "cisco_ios_telnet"}}
            },
        },
        "linux_telnet": {
            "platform": "linux",
            "hostname": os.getenv("GNS3_SERVER_HOST"),
            "timeout": 120,
            "username": os.getenv("LINUX_TELNET_USERNAME"),
            "password": os.getenv("LINUX_TELNET_PASSWORD"),
            "connection_options": {
                "netmiko": {
                    "platform": "linux",
                    "extras": {
                        "device_type": "generic_telnet",
                        "global_delay_factor": 3,
                        "timeout": 120,
                        "fast_cli": False,
                    },
                }
            },
        },
    }


def get_nornir_groups_config(group_name: str = "cisco_IOSv_telnet") -> dict[str, Any]:
    """
    Get Nornir groups configuration for network devices.

    Args:
        group_name: Name of the group configuration (default: "cisco_IOSv_telnet")

    Returns:
        Dictionary containing Nornir group configuration
    """
    # Ensure environment variables are loaded
    load_env_variables()

    all_groups = get_nornir_all_groups_config()

    result = all_groups.get(group_name, {})
    if not isinstance(result, dict):
        return {}
    return result


def get_nornir_defaults() -> dict[str, Any]:
    """
    Get Nornir default configuration.

    Returns:
        Dictionary containing Nornir defaults
    """
    return {"data": {"location": "gns3"}}


def get_gns3_server_config() -> dict[str, str | None]:
    """
    Get GNS3 server configuration from environment variables.

    Returns:
        Dictionary containing GNS3 server configuration
    """
    # Ensure environment variables are loaded
    load_env_variables()

    return {
        "api_version": os.getenv("API_VERSION"),
        "server_url": os.getenv("GNS3_SERVER_URL"),
        "username": os.getenv("GNS3_SERVER_USERNAME"),
        "password": os.getenv("GNS3_SERVER_PASSWORD"),
        "host": os.getenv("GNS3_SERVER_HOST"),
    }


def force_reload_env() -> None:
    """
    Force reload environment variables from .env file.

    Use this function when you need to ensure the latest configuration is loaded,
    for example, after a user has modified the .env file.
    """
    logger.info("Forcing reload of environment variables")
    load_env_variables(force_reload=True)


# Alias for load_env_variables for convenience
load_env = load_env_variables
