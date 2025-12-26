#!/usr/bin/env python3
"""
Automatic Documentation Update Script using Zhipu GLM-4.5-X API

This script:
1. Analyzes git diff to detect code changes
2. Calls Zhipu GLM-4.5-X API to generate documentation updates
3. Updates both English and Chinese documentation
4. Commits changes to the PR branch
5. Generates English PR comment

Usage:
    python scripts/auto_update_docs.py
"""

import os
import sys
import subprocess
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import re

# Configuration
ZHIPU_API_KEY = os.getenv('ZHIPU_API_KEY')
ZHIPU_MODEL = os.getenv('ZHIPU_MODEL', 'glm-4-flash')
PR_NUMBER = os.getenv('PR_NUMBER')
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
REPO_OWNER = os.getenv('REPO_OWNER')
REPO_NAME = os.getenv('REPO_NAME')


def get_changed_files(base_ref: str = 'origin/Development') -> List[str]:
    """Get list of changed files in the PR"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', f'{base_ref}...HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return [f for f in result.stdout.split('\n') if f]
    except subprocess.CalledProcessError as e:
        print(f"Error getting changed files: {e}")
        return []


def get_diff_content(base_ref: str = 'origin/Development') -> str:
    """Get git diff content"""
    try:
        result = subprocess.run(
            ['git', 'diff', f'{base_ref}...HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting diff: {e}")
        return ""


def call_zhipu_api(prompt: str) -> Optional[Dict]:
    """Call Zhipu GLM-4.5-X API"""
    if not ZHIPU_API_KEY:
        print("ERROR: ZHIPU_API_KEY not found")
        return None
    
    import urllib.request
    import urllib.error
    
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {ZHIPU_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": ZHIPU_MODEL,
        "messages": [
            {
                "role": "system",
                "content": """You are a documentation assistant for GNS3 Copilot project. 
Analyze code changes and provide:
1. English change summary and documentation updates
2. Chinese change summary for README_ZH.md

Output in JSON format:
{
    "english_summary": "English change summary",
    "chinese_summary": "Chinese change summary",
    "doc_updates": {
        "README.md": {"section": "Features", "content": "new content to add"},
        "README_ZH.md": {"section": "功能列表", "content": "新功能内容"}
    }
}"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 4000
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode('utf-8'))
            content = result['choices'][0]['message']['content']
            
            # Parse JSON from content
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                return json.loads(json_match.group())
            return None
            
    except urllib.error.HTTPError as e:
        print(f"API Error {e.code}: {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Error calling Zhipu API: {e}")
        return None


def update_documentation(doc_updates: Dict) -> Dict[str, str]:
    """Update documentation files"""
    updated_files = {}
    
    for doc_file, update_info in doc_updates.items():
        doc_path = Path(doc_file)
        
        if not doc_path.exists():
            print(f"Warning: {doc_file} not found, skipping")
            continue
        
        content = doc_path.read_text(encoding='utf-8')
        section = update_info.get('section', '')
        new_content = update_info.get('content', '')
        
        # Find and update section
        if section:
            # Look for section header (e.g., "## Features")
            pattern = rf'(##\s+{re.escape(section)}.*?\n)'
            match = re.search(pattern, content, re.IGNORECASE)
            
            if match:
                # Insert new content after the section header
                insert_pos = match.end()
                updated_content = content[:insert_pos] + new_content + '\n' + content[insert_pos:]
                doc_path.write_text(updated_content, encoding='utf-8')
                updated_files[doc_file] = "Section updated"
                print(f"✓ Updated {doc_file}")
            else:
                print(f"✗ Section '{section}' not found in {doc_file}")
                updated_files[doc_file] = "Section not found"
    
    return updated_files


def commit_changes(message: str) -> bool:
    """Commit changes to git"""
    try:
        subprocess.run(['git', 'add', '.'], check=True)
        result = subprocess.run(
            ['git', 'commit', '-m', message],
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            print("✓ Changes committed successfully")
            # Push changes
            subprocess.run(['git', 'push'], check=True)
            print("✓ Changes pushed successfully")
            return True
        elif 'nothing to commit' in result.stdout.lower():
            print("No changes to commit")
            return True
        else:
            print(f"Commit failed: {result.stdout}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error committing changes: {e}")
        return False


def create_pr_comment(summary: str) -> bool:
    """Create PR comment using GitHub API"""
    if not GITHUB_TOKEN or not PR_NUMBER:
        print("Missing GITHUB_TOKEN or PR_NUMBER, skipping PR comment")
        return False
    
    import urllib.request
    
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{PR_NUMBER}/comments"
    
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json"
    }
    
    data = {
        "body": f"""## 📝 Documentation Update Summary

{summary}

---
*This comment was automatically generated by Zhipu GLM-4.5-X API*"""
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            print(f"✓ PR comment created (#{PR_NUMBER})")
            return True
            
    except Exception as e:
        print(f"Error creating PR comment: {e}")
        return False


def main():
    """Main execution"""
    print("=" * 60)
    print("GNS3 Copilot - Automatic Documentation Update")
    print("=" * 60)
    print()
    
    # Get code changes
    print("📋 Analyzing code changes...")
    changed_files = get_changed_files()
    diff_content = get_diff_content()
    
    if not changed_files:
        print("No changed files detected. Exiting.")
        return 0
    
    print(f"✓ Found {len(changed_files)} changed files")
    print(f"  Files: {', '.join(changed_files[:5])}...")
    print()
    
    # Filter relevant files
    relevant_files = [f for f in changed_files if f.startswith('src/')]
    if not relevant_files:
        print("No source code changes detected. Exiting.")
        return 0
    
    print(f"✓ Found {len(relevant_files)} source code changes")
    print()
    
    # Call Zhipu API
    print(f"🤖 Calling Zhipu {ZHIPU_MODEL} API...")
    prompt = f"""Analyze the following code changes in the GNS3 Copilot project:

Changed files: {', '.join(relevant_files)}

Git diff:
{diff_content[:5000]}

Provide:
1. English summary of changes
2. Chinese summary for README_ZH.md
3. Suggested documentation updates for README.md and README_ZH.md
"""
    
    api_response = call_zhipu_api(prompt)
    
    if not api_response:
        print("✗ Failed to get response from Zhipu API")
        return 1
    
    print("✓ Received response from Zhipu API")
    print()
    
    # Extract information
    english_summary = api_response.get('english_summary', 'No summary available')
    chinese_summary = api_response.get('chinese_summary', '')
    doc_updates = api_response.get('doc_updates', {})
    
    print("📄 English Summary:")
    print(english_summary)
    print()
    
    if chinese_summary:
        print("📝 Chinese Summary:")
        print(chinese_summary)
        print()
    
    # Update documentation
    if doc_updates:
        print("📚 Updating documentation...")
        updated_files = update_documentation(doc_updates)
        print()
        
        if updated_files:
            # Commit changes
            commit_msg = f"docs: auto-update documentation\n\n[skip ci]\nSummary: {english_summary[:100]}"
            commit_changes(commit_msg)
        else:
            print("No documentation updates applied")
    else:
        print("No documentation updates suggested")
    
    # Create PR comment
    print("💬 Creating PR comment...")
    create_pr_comment(english_summary)
    print()
    
    print("=" * 60)
    print("✓ Documentation update completed successfully")
    print("=" * 60)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
