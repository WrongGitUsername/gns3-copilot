"""
GNS3 Copilot Agent Package

This package contains the main GNS3 Copilot agent implementation for network automation tasks.
"""

from .gns3_copilot import (
    agent,
    llm,
    tools,
    logger,
    SYSTEM_PROMPT
)

__version__ = "1.0.0"
__author__ = "GNS3 Copilot Team"
__description__ = "AI-powered network automation assistant for GNS3"

__all__ = [
    "agent",
    "llm", 
    "tools",
    "logger",
    "SYSTEM_PROMPT",
]
