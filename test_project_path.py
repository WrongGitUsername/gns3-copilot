#!/usr/bin/env python3
"""
Test script for GNS3ProjectPath tool.

This script tests the GNS3ProjectPath tool with specific project information
to diagnose permission and path issues.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from gns3_copilot.gns3_client.gns3_project_path import GNS3ProjectPath

# Test with provided project information
project_name = "阿里巴巴"
project_id = "1445a4ba-4635-430b-a332-bef438f65932"

print("=" * 60)
print("Testing GNS3ProjectPath Tool")
print("=" * 60)
print(f"Project Name: {project_name}")
print(f"Project ID: {project_id}")
print()

# Create tool instance
tool = GNS3ProjectPath()

# Run the tool
result = tool._run({
    "project_name": project_name,
    "project_id": project_id
})

# Display results
print("Result:")
print("-" * 60)
import json
print(json.dumps(result, indent=2, ensure_ascii=False))
print("-" * 60)
print()

# Check if successful
if result.get("success"):
    project_path = result.get("project_path")
    print(f"✓ Successfully retrieved project path: {project_path}")
    print()
    
    # Check if path exists
    if os.path.exists(project_path):
        print(f"✓ Path exists")
        
        # Check if it's a directory
        if os.path.isdir(project_path):
            print(f"✓ Path is a directory")
            
            # Check if we can read it
            if os.access(project_path, os.R_OK):
                print(f"✓ Path is readable")
            else:
                print(f"✗ Path is NOT readable")
            
            # Check if we can write to it
            if os.access(project_path, os.W_OK):
                print(f"✓ Path is writable")
            else:
                print(f"✗ Path is NOT writable (Permission denied)")
            
            # List contents
            print()
            print("Directory contents:")
            try:
                contents = os.listdir(project_path)
                for item in contents[:10]:  # Show first 10 items
                    print(f"  - {item}")
                if len(contents) > 10:
                    print(f"  ... and {len(contents) - 10} more items")
            except PermissionError as e:
                print(f"  ✗ Cannot list directory: {e}")
        else:
            print(f"✗ Path is NOT a directory")
    else:
        print(f"✗ Path does NOT exist")
    
    # Try to create notes directory
    print()
    notes_dir = os.path.join(project_path, "notes")
    print(f"Attempting to create notes directory: {notes_dir}")
    
    try:
        os.makedirs(notes_dir, exist_ok=True)
        print(f"✓ Successfully created/verified notes directory")
        
        # Try to create a test file
        test_file = os.path.join(notes_dir, "test.md")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("# Test\n\nThis is a test file.")
        print(f"✓ Successfully created test file: {test_file}")
        
        # Clean up test file
        os.remove(test_file)
        print(f"✓ Cleaned up test file")
    except PermissionError as e:
        print(f"✗ Permission denied: {e}")
    except Exception as e:
        print(f"✗ Error: {e}")
else:
    print(f"✗ Failed to retrieve project path")
    print(f"Error: {result.get('error')}")

print()
print("=" * 60)
