"""
Log configuration package for GNS3 Copilot tools.

This package provides centralized logging configuration utilities
to eliminate duplicate logging setup code across modules.
"""

from .logging_config import (
    setup_logger,
    get_logger,
    configure_package_logging,
    setup_tool_logger,
    LOGGER_CONFIGS,
)

__all__ = [
    "setup_logger",
    "get_logger", 
    "configure_package_logging",
    "setup_tool_logger",
    "LOGGER_CONFIGS",
]
