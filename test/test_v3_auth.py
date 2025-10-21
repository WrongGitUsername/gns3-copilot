#!/usr/bin/env python3
"""
Test script for v3 API authentication functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from custom_gns3fy import Gns3Connector

def test_v2_auth():
    """Test v2 API authentication (basic auth)"""
    print("Testing v2 API authentication...")
    try:
        # This will use basic auth
        server = Gns3Connector(
            url="http://192.168.88.98",
            user="admin",
            cred="admin",
            api_version=2
        )
        version = server.get_version()
        print(f"v2 API Version: {version}")
        return True
    except Exception as e:
        print(f"v2 API test failed: {e}")
        return False

def test_v3_auth():
    """Test v3 API authentication (JWT token)"""
    print("Testing v3 API authentication...")
    try:
        # This will use JWT token auth
        server = Gns3Connector(
            url="http://192.168.88.98",
            user="admin",
            cred="admin",
            api_version=3
        )
        version = server.get_version()
        print(f"v3 API Version: {version}")
        print(f"Access Token: {server.access_token}")
        return True
    except Exception as e:
        print(f"v3 API test failed: {e}")
        return False

def test_v3_auth_failure():
    """Test v3 API authentication with wrong credentials"""
    print("Testing v3 API authentication failure...")
    try:
        server = Gns3Connector(
            url="http://192.168.88.98",
            user="admin",
            cred="wrongpassword",
            api_version=3
        )
        version = server.get_version()
        print(f"Unexpected success: {version}")
        return False
    except Exception as e:
        print(f"Expected v3 API auth failure: {e}")
        return True

if __name__ == "__main__":
    print("GNS3 v3 API Authentication Test")
    print("=" * 50)
    
    # Test v2 API
    v2_success = test_v2_auth()
    print()
    
    # Test v3 API
    v3_success = test_v3_auth()
    print()
    
    # Test v3 API failure case
    v3_failure_success = test_v3_auth_failure()
    print()
    
    print("Test Results:")
    print(f"v2 API: {'PASS' if v2_success else 'FAIL'}")
    print(f"v3 API: {'PASS' if v3_success else 'FAIL'}")
    print(f"v3 Auth Failure: {'PASS' if v3_failure_success else 'FAIL'}")
    
    if v2_success and v3_success and v3_failure_success:
        print("\nAll tests PASSED! v3 API authentication is working correctly.")
    else:
        print("\nSome tests FAILED! Please check the implementation.")
