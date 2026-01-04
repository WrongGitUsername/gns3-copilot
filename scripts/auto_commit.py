#!/usr/bin/env python3
"""
Automatic Commit Message Generator using Zhipu GLM-4.5-X API

This script analyzes current git changes and generates an appropriate commit message,
then executes git commit with the AI-generated message.

Usage:
    export ZHIPU_API_KEY="your-api-key"
    python scripts/auto_commit.py
    
    # Dry run mode (generate message without committing)
    python scripts/auto_commit.py --dry-run
"""

import os
import sys
import subprocess
import json
import argparse
import re
from typing import Optional, List, Dict

# Configuration
ZHIPU_API_KEY = os.getenv('ZHIPU_API_KEY')
ZHIPU_MODEL = os.getenv('ZHIPU_MODEL', 'GLM-4.5-X')


def get_staged_files() -> List[str]:
    """Get list of staged files"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached', '--name-only'],
            capture_output=True,
            text=True,
            check=True
        )
        return [f for f in result.stdout.split('\n') if f]
    except subprocess.CalledProcessError as e:
        print(f"Error getting staged files: {e}")
        return []


def get_staged_diff() -> str:
    """Get git diff for staged files"""
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached'],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error getting diff: {e}")
        return ""


def call_zhipu_api(prompt: str) -> Optional[Dict]:
    """Call Zhipu API for commit message generation"""
    if not ZHIPU_API_KEY:
        print("ERROR: ZHIPU_API_KEY not found")
        print("Please set environment variable: export ZHIPU_API_KEY='your-api-key'")
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
                "content": """You are generating git commit messages for the GNS3 Copilot project.
Follow the Conventional Commits specification:

Format: <type>(<scope>): <subject>

Types:
- feat: A new feature
- fix: A bug fix
- docs: Documentation only changes
- style: Code style changes (formatting, etc.)
- refactor: Code refactoring
- perf: Performance improvements
- test: Adding or updating tests
- chore: Maintenance tasks
- ci: CI/CD changes

Rules:
1. Use imperative mood in subject (e.g., "add" not "added")
2. Subject must be <= 72 characters
3. Body can explain "what" and "why" (max 100 chars per line)
4. Body should reference related issues with (#xxx) format
5. Focus on code functionality, not just file changes
6. If multiple files changed, group them logically

Output ONLY valid JSON:
{
    "commit_message": "Complete commit message including subject and optional body"
}"""
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.3,
        "max_tokens": 500
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


def execute_commit(message: str, amend: bool = False) -> bool:
    """Execute git commit with the generated message"""
    try:
        args = ['git', 'commit']
        if amend:
            args.append('--amend')
        args.extend(['-m', message])
        
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=False
        )
        
        if result.returncode == 0:
            return True
        else:
            print(f"Commit failed: {result.stderr}")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"Error committing changes: {e}")
        return False


def generate_commit_message(staged_files: List[str], diff_content: str) -> Optional[str]:
    """Generate commit message using AI"""
    print("🤖 Calling Zhipu API for commit message generation...")
    
    # Build prompt
    prompt = f"""Analyze the following staged changes in the GNS3 Copilot project:

Staged files ({len(staged_files)}):
{chr(10).join(f"- {f}" for f in staged_files)}

Git diff (for detailed analysis):
{diff_content[:8000]}

Generate a commit message following Conventional Commits format.
Focus on the actual functionality changes, not just file modifications."""
    
    api_response = call_zhipu_api(prompt)
    
    if not api_response:
        return None
    
    commit_message = api_response.get('commit_message', '').strip()
    return commit_message


def validate_commit_message(message: str) -> bool:
    """Validate commit message format"""
    if not message:
        return False
    
    # Check for conventional commits format
    pattern = r'^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\(.+\))?\:.+'
    return bool(re.match(pattern, message))


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(
        description='Generate and execute git commit messages using AI'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Generate commit message without committing'
    )
    parser.add_argument(
        '--amend',
        action='store_true',
        help='Amend the last commit'
    )
    parser.add_argument(
        '--allow-empty',
        action='store_true',
        help='Allow empty commit message'
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("GNS3 Copilot - Automatic Commit Message Generator")
    print("=" * 60)
    print()
    
    # Get staged changes
    print("📋 Analyzing staged changes...")
    staged_files = get_staged_files()
    diff_content = get_staged_diff()
    
    if not staged_files:
        print("No staged files detected. Exiting.")
        print()
        print("Hint: Use 'git add <files>' to stage changes first.")
        return 0
    
    print(f"✓ Found {len(staged_files)} staged files:")
    for f in staged_files[:10]:
        print(f"  - {f}")
    if len(staged_files) > 10:
        print(f"  ... and {len(staged_files) - 10} more files")
    print()
    
    # Generate commit message
    commit_message = generate_commit_message(staged_files, diff_content)
    
    if not commit_message:
        print("✗ Failed to generate commit message")
        return 1
    
    print("✓ Generated commit message:")
    print()
    print("─" * 60)
    print(commit_message)
    print("─" * 60)
    print()
    
    # Validate commit message
    if not validate_commit_message(commit_message) and not args.allow_empty:
        print("⚠️  Warning: Commit message may not follow Conventional Commits format")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response != 'y':
            print("Cancelled.")
            return 0
    
    # Dry run mode
    if args.dry_run:
        print("✓ Dry run mode - no commit executed")
        print()
        print("To commit, run:")
        print(f"  git commit -m \"{commit_message}\"")
        return 0
    
    # Confirm commit
    response = input("Commit with this message? (Y/n): ").strip().lower()
    if response == 'n':
        print("Cancelled.")
        return 0
    
    # Execute commit
    print()
    print("🔨 Committing changes...")
    success = execute_commit(commit_message, amend=args.amend)
    
    if success:
        print()
        if args.amend:
            print("✓ Last commit amended successfully")
            print("  Note: Use 'git push --force' to update remote")
        else:
            print("✓ Changes committed successfully")
            print("  Next: Use 'git push' to upload changes")
        
        print()
        print("Recent commits:")
        subprocess.run(['git', 'log', '--oneline', '-3'])
    else:
        print()
        print("✗ Commit failed")
        print("  You can commit manually with:")
        print(f"  git commit -m \"{commit_message}\"")
    
    print()
    print("=" * 60)
    print("✓ Operation completed")
    print("=" * 60)
    
    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
