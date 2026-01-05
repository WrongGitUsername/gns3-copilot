"""
Pytest configuration and fixtures for GNS3 Copilot test suite.
"""

import os
import pytest
from unittest.mock import patch


@pytest.fixture
def mock_env():
    """
    Fixture that sets up mock environment variables for testing.
    
    This fixture is automatically applied to all tests via pytest.ini's usefixtures.
    It provides a consistent environment for tests that require environment variables.
    
    Environment variables set:
    - API_VERSION: GNS3 API version (defaults to "2")
    - GNS3_SERVER_URL: GNS3 server URL (defaults to "http://localhost:3080")
    """
    mock_env_vars = {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080",
    }
    
    with patch.dict(os.environ, mock_env_vars, clear=False):
        yield mock_env_vars


@pytest.fixture
def mock_gns3_v2_env():
    """
    Fixture that sets up mock GNS3 v2 environment variables.
    """
    mock_env_vars = {
        "API_VERSION": "2",
        "GNS3_SERVER_URL": "http://localhost:3080",
    }
    
    with patch.dict(os.environ, mock_env_vars, clear=False):
        yield mock_env_vars


@pytest.fixture
def mock_gns3_v3_env():
    """
    Fixture that sets up mock GNS3 v3 environment variables with authentication.
    """
    mock_env_vars = {
        "API_VERSION": "3",
        "GNS3_SERVER_URL": "http://localhost:3080",
        "GNS3_USERNAME": "admin",
        "GNS3_PASSWORD": "password",
    }
    
    with patch.dict(os.environ, mock_env_vars, clear=False):
        yield mock_env_vars
