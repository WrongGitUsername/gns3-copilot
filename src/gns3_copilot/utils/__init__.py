"""
GNS3 Copilot Utils Package

This package provides utility functions for GNS3 Copilot, including:
- Version checking and update management functionality
- PyPI integration for automatic updates
- Version comparison utilities

Main modules:
- updater: Version checking and update management functionality

Author: WrongGitUsername
"""

# Import main utility functions
from .updater import get_installed_version, get_latest_version, is_update_available, run_update

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

__author__ = "WrongGitUsername"
__description__ = "Utility functions for GNS3 Copilot"
__url__ = "https://github.com/yueguobin/gns3-copilot"

# Export main utility functions
__all__ = [
    "get_installed_version",
    "get_latest_version", 
    "is_update_available",
    "run_update",
]

# Package initialization message
# print(f"GNS3 Copilot Utils package loaded (version {__version__})")
