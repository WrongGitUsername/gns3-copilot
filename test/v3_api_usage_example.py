#!/usr/bin/env python3
"""
Example usage of GNS3 v3 API authentication
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from custom_gns3fy import Gns3Connector, Project, Node

def example_v2_usage():
    """Example of using v2 API (backward compatibility)"""
    print("=== v2 API Usage Example ===")
    
    # v2 API uses basic authentication
    server = Gns3Connector(
        url="http://192.168.88.98",
        user="admin", 
        cred="admin",
        api_version=2  # Default is 2, so this is optional
    )
    
    # All existing code works exactly the same
    projects = server.get_projects()
    print(f"Found {len(projects)} projects using v2 API")
    
    return server

def example_v3_usage():
    """Example of using v3 API with JWT authentication"""
    print("\n=== v3 API Usage Example ===")
    
    # v3 API uses JWT token authentication
    server = Gns3Connector(
        url="http://192.168.88.98",
        user="admin",
        cred="admin", 
        api_version=3  # This enables v3 API with JWT auth
    )
    
    # The API usage is exactly the same!
    projects = server.get_projects()
    print(f"Found {len(projects)} projects using v3 API")
    
    # You can access the JWT token if needed
    print(f"JWT Token: {server.access_token}")
    
    return server

def example_project_operations(server):
    """Example of project operations with v3 API"""
    print("\n=== Project Operations Example ===")
    
    # Create a project using v3 API
    project = Project(
        name="test-v3-project",
        connector=server
    )
    
    try:
        project.create()
        print(f"Created project: {project.name} (ID: {project.project_id})")
        
        # List nodes in the project
        project.get_nodes()
        print(f"Project has {len(project.nodes)} nodes")
        
        # Clean up
        project.delete()
        print("Project deleted")
        
    except Exception as e:
        print(f"Project operation failed: {e}")

def example_automatic_token_refresh():
    """Example showing automatic token refresh (if implemented)"""
    print("\n=== Token Refresh Example ===")
    
    server = Gns3Connector(
        url="http://192.168.88.98",
        user="admin",
        cred="admin",
        api_version=3
    )
    
    # Make multiple API calls - token will be automatically managed
    for i in range(3):
        try:
            version = server.get_version()
            print(f"API call {i+1}: Success - {version}")
        except Exception as e:
            print(f"API call {i+1}: Failed - {e}")

if __name__ == "__main__":
    print("GNS3 v3 API Authentication Usage Examples")
    print("=" * 60)
    
    try:
        # Show v2 API usage (backward compatible)
        v2_server = example_v2_usage()
        
        # Show v3 API usage
        v3_server = example_v3_usage()
        
        # Show project operations with v3
        example_project_operations(v3_server)
        
        # Show token management
        example_automatic_token_refresh()
        
        print("\n✅ All examples completed successfully!")
        print("\nKey Features:")
        print("- Backward compatible: v2 API code works unchanged")
        print("- Automatic authentication: Just set api_version=3")
        print("- JWT token management: Automatic token handling")
        print("- Same API interface: No code changes needed")
        
    except Exception as e:
        print(f"\n❌ Example failed: {e}")
        print("Please ensure GNS3 server is running and credentials are correct.")
