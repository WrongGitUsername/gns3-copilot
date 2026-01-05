# Documentation Auto-Update Script Improvements

## Problem Background

The original `scripts/auto_update_docs.py` script has the following issues when handling multiple commits:

1. **Only analyzes git diff**: The script only looks at the differences between the current branch and `origin/Development`
2. **Lacks context**: Doesn't retrieve commit messages and existing documentation content
3. **Duplicate functionality**: AI might repeatedly add already documented features
4. **Insufficient aggregation**: Cannot intelligently merge feature descriptions from multiple related commits
5. **Local mode defects**: Local mode only focuses on documentation changes, ignoring new tool code features

## Improvement Plan

### 1. New Context Collection Functions

#### `get_commit_messages()` Function
```python
def get_commit_messages(base_ref: str = 'origin/Development') -> List[str]:
    """Get all commit messages in the PR"""
```

- **Function**: Retrieve all commit messages from `origin/Development` to current HEAD
- **Purpose**: Help AI understand complete feature development history

#### `read_existing_documentation()` Function
```python
def read_existing_documentation(doc_file: str, section: str) -> str:
    """Read existing content from documentation section"""
```

- **Function**: Read existing content in the "Core Features" section of README.md and README_ZH.md
- **Purpose**: Let AI know which features are already documented to avoid duplicates

### 2. Enhanced AI Prompts

The updated `call_zhipu_api_for_docs()` function now accepts additional context parameters:

```python
def call_zhipu_api_for_docs(
    prompt: str,
    commit_messages: List[str],
    existing_features_en: str = "",
    existing_features_zh: str = ""
) -> Optional[Dict]:
```

**System Prompt Improvements**:
- Explicitly instruct AI to compare with existing documentation
- Only add undocumented new features
- Merge related features from multiple commits
- Return empty string if all features are already documented

### 3. Improved Workflow

In GitHub Actions mode, the script now performs the following steps:

```
1. Analyze code changes
   ↓
2. Get all commit messages (get_commit_messages)
   ↓
3. Read existing documentation (read_existing_documentation)
   ↓
4. Build comprehensive prompt (includes commit messages, diff, existing documentation)
   ↓
5. Call AI to generate documentation update suggestions
   ↓
6. Record update suggestions (display preview)
   ↓
7. Apply documentation updates
   ↓
8. Commit changes and create PR comment
```

### 4. Local Mode Improvements

**Problem**: Local mode only focuses on documentation changes, ignoring new tool code features

**Solution**:
- Local mode now also retrieves commit messages
- Enhanced AI prompts explicitly instruct to prioritize code feature characteristics
- Priority instructions in the prompt:
  1. New tools or functions
  2. Major refactoring or architecture changes
  3. Bug fixes and improvements
  4. Configuration or dependency changes

**Improved local mode output**:
```
🤖 Local mode detected (creating PR)
📜 Fetching commit messages...
✓ Found 8 commits

🤖 Calling Zhipu GLM-4.5-X API for PR generation...
✓ Received response from Zhipu API

📄 PR Title:
  Add voice interaction tools and TTS/STT support

📄 PR Description (first 500 chars):
  ## 🚀 Change Type
  - [x] ✨ New Feature
  - [ ] 🐞 Bug Fix
  - [ ] 🔧 Refactor/Maintenance
  - [ ] 📚 Documentation
  
  ## 📝 Description of Changes
  Added comprehensive voice interaction support to GNS3 Copilot:
  
  1. **New Tools**:
     - `voice_tools.py`: New tool for voice command execution
     - Enhanced prompt templates for voice interactions
  ...
```

### 5. Enhanced Logging

The script now provides more detailed output:

```
📋 Analyzing code changes...
✓ Found 15 changed files
  Files: src/gns3_copilot/tools_v2/voice_tools.py, src/gns3_copilot/...

✓ Found 12 source code

📜 Fetching commit messages...
✓ Found 8 commits

📖 Reading existing documentation...
✓ Found 450 characters in existing English features
✓ Found 380 characters in existing Chinese features

🤖 Calling Zhipu GLM-4.5-X API for documentation updates...
✓ Received response from Zhipu API

📄 English Summary:
Added voice interaction support with TTS/STT functionality

📝 Chinese Summary:
添加语音交互支持，包括TTS/STT功能

📝 Documentation update suggestions:
  README.md (Core Features):
    - 🗣️ **Voice Interaction**: Text-to-speech and speech-to-text support...
    (156 characters total)
  README_ZH.md (核心功能):
    - 🗣️ **语音交互**：支持文本转语音和语音转文本，实现免提操作...
    (132 characters total)

📚 Updating documentation...
✓ Updated README.md
✓ Updated README_ZH.md

✓ Changes committed successfully
💬 Creating PR comment...
✓ PR comment created (#123)
```

## Usage Examples

### Local Mode (Creating PR)

```bash
export ZHIPU_API_KEY="your-api-key"
export GITHUB_TOKEN="your-github-token"
export REPO_OWNER="yueguobin"
export REPO_NAME="gns3-copilot"
python scripts/auto_update_docs.py
```

### GitHub Actions Mode (Auto-triggered)

When a PR is created or updated to the `Development` branch, the workflow will automatically:
1. Analyze code changes
2. Get commit history
3. Compare with existing documentation
4. Generate and apply documentation updates
5. Add a comment in the PR explaining the updates

## Key Improvements

| Aspect | Before | After |
|--------|--------|-------|
| Context Information | Only git diff | Commit messages + git diff + existing documentation |
| Feature Aggregation | Only looks at current diff | Merges related features from multiple commits |
| Duplicate Detection | None | Compares with existing documentation, avoids duplicates |
| Log Output | Simple | Detailed, including preview and verification |
| Documentation Updates | May duplicate | Only adds new features |
| Local Mode PR Generation | Only focuses on documentation changes | Prioritizes code feature characteristics |

## Important Notes

1. **API Key**: Ensure `ZHIPU_API_KEY` is configured in GitHub Secrets
2. **Model Selection**: Defaults to `glm-4-flash`, can be modified via `ZHIPU_MODEL` in Secrets
3. **Branch Strategy**: PR must target the `Development` branch
4. **Commit Frequency**: Triggered on each PR update (opened/synchronize/reopened)

## Future Possible Improvements

1. Support more documentation sections (e.g., architecture, installation guide)
2. Add manual review step, allowing confirmation before committing changes
3. Support synchronous multi-language documentation updates
4. Add more intelligent feature deduplication algorithms
5. Support custom documentation templates
