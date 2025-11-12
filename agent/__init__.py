"""
GNS3 Copilot Agent Package

This package contains the main GNS3 Copilot agent implementation for network automation tasks.
"""

from .gns3_copilot import agent

# Dynamic version management
try:
    from importlib.metadata import version
    __version__ = version("gns3-copilot")
except ImportError:
    # Fallback for Python < 3.8
    try:
        import pkg_resources
        __version__ = pkg_resources.get_distribution("gns3-copilot").version
    except Exception:
        __version__ = "unknown"
except Exception:
    __version__ = "unknown"

__author__ = "GNS3 Copilot Team"
__description__ = "AI-powered network automation assistant for GNS3"

__all__ = [
    "agent",
]
