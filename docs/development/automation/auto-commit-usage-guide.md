# Auto Commit Script Usage Guide

## Overview

`scripts/auto_commit.py` is an intelligent commit message generation tool based on Zhipu GLM-4.5-X API that can automatically analyze code changes and generate commit messages following Conventional Commits specification.

## Features

- 🤖 **AI-Powered**: Uses Zhipu GLM-4.5-X model to analyze code changes
- 📝 **Standard Format**: Automatically generates commit messages following Conventional Commits specification
- 🔍 **Intelligent Analysis**: Understands actual functionality of code changes, not just file lists
- ✅ **Format Validation**: Automatically validates commit message format
- 🎯 **Flexible Options**: Supports dry-run, amend, and various modes

## Installation & Configuration

### 1. Requirements

- Python 3.7+
- Git
- Zhipu AI API Key

### 2. Configure API Key

```bash
export ZHIPU_API_KEY="your-api-key-here"

# Optional: Custom model (defaults to GLM-4.5-X)
export ZHIPU_MODEL="glm-4-flash"
```

### 3. Verify Installation

```bash
python scripts/auto_commit.py --help
```

## Usage

### Basic Usage

```bash
# 1. Stage files to commit
git add <file1> <file2> ...
# or
git add .

# 2. Run script to generate and execute commit
python scripts/auto_commit.py
```

### Dry Run Mode

Only generates commit message without executing commit:

```bash
python scripts/auto_commit.py --dry-run
```

Output example:
```
============================================================
GNS3 Copilot - Automatic Commit Message Generator
============================================================

📋 Analyzing staged changes...
✓ Found 3 staged files:
  - src/gns3_copilot/tools_v2/voice_tools.py
  - src/gns3_copilot/prompts/voice_prompt.py
  - docs/voice-interaction-guide.md

🤖 Calling Zhipu API for commit message generation...
✓ Generated commit message:

────────────────────────────────────────────────────────────
feat(voice): add TTS/STT voice interaction support

Implement text-to-speech and speech-to-text functionality
for hands-free operation with GNS3 Copilot.
────────────────────────────────────────────────────────────

✓ Dry run mode - no commit executed

To commit, run:
  git commit -m "feat(voice): add TTS/STT voice interaction support"
```

### Amend Mode

Modify the last commit:

```bash
python scripts/auto_commit.py --amend
```

**Note**: After amending, you need to force push:
```bash
git push --force
```

### Combined Options

```bash
# Dry run + amend (preview commit message to amend)
python scripts/auto_commit.py --amend --dry-run
```

## Conventional Commits Specification

The script follows Conventional Commits specification:

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login support` |
| `fix` | Bug fix | `fix(api): resolve timeout issue on slow connections` |
| `docs` | Documentation changes | `docs(readme): update installation instructions` |
| `style` | Code style (no functional changes) | `style(format): apply black formatting` |
| `refactor` | Code refactoring | `refactor(agent): simplify state machine logic` |
| `perf` | Performance optimization | `perf(caching): add LRU cache for config` |
| `test` | Test related | `test(tools): add unit tests for config tools` |
| `chore` | Build/tool/dependency changes | `chore(deps): upgrade nornir to 0.5.0` |
| `ci` | CI/CD configuration | `ci(github): add automated testing workflow` |

### Common Scopes

- `tools`: Tool layer (tools_v2/)
- `agent`: Agent layer (agent/)
- `ui`: UI layer (ui_model/)
- `client`: GNS3 client (gns3_client/)
- `docs`: Documentation (docs/)
- `test`: Tests (tests/)

### Example Commit Messages

**Simple commit:**
```
feat(tools): add network discovery tool
```

**With detailed description:**
```
feat(voice): add TTS/STT voice interaction support

Implement text-to-speech and speech-to-text functionality
for hands-free operation with GNS3 Copilot.

Closes #123
```

**Bug fix:**
```
fix(api): resolve connection timeout on slow networks

Increase timeout from 30s to 60s for network operations.
Add retry logic for transient failures.

Fixes #456
```

## Workflow

### Recommended Development Workflow

```bash
# 1. Make code changes
vim src/gns3_copilot/tools_v2/new_tool.py

# 2. Review changes
git status
git diff

# 3. Stage relevant files
git add src/gns3_copilot/tools_v2/new_tool.py

# 4. Use script to generate commit message
python scripts/auto_commit.py

# 5. Press Enter (or Y) to confirm commit message
Commit with this message? (Y/n): [Enter]

# 6. Push to remote
git push
```

### Complete Example

```bash
$ git add .
$ python scripts/auto_commit.py
============================================================
GNS3 Copilot - Automatic Commit Message Generator
============================================================

📋 Analyzing staged changes...
✓ Found 5 staged files:
  - src/gns3_copilot/tools_v2/network_discovery.py
  - src/gns3_copilot/agent/gns3_copilot.py
  - tests/tools_v2/test_network_discovery.py
  - README.md
  - docs/network-discovery-guide.md

🤖 Calling Zhipu API for commit message generation...
✓ Generated commit message:

────────────────────────────────────────────────────────────
feat(tools): add network discovery functionality

Implement automatic network discovery tool that can detect
and catalog network devices in GNS3 topology.

- Add discovery tool with SNMP support
- Integrate with existing agent workflow
- Add comprehensive test coverage
- Update documentation with usage examples
────────────────────────────────────────────────────────────

Commit with this message? (Y/n): 

🔨 Committing changes...

✓ Changes committed successfully
  Next: Use 'git push' to upload changes

Recent commits:
a1b2c3d feat(tools): add network discovery functionality
e4f5g6h fix(api): resolve connection timeout
h7i8j9k docs(readme): update setup instructions

============================================================
✓ Operation completed
============================================================
```

## Advanced Usage

### Custom Model

```bash
export ZHIPU_MODEL="glm-4-flash"
python scripts/auto_commit.py
```

### Batch Committing Multiple Features

```bash
# Commit feature 1
git add feature1.py
python scripts/auto_commit.py --dry-run
git commit -m "$(python scripts/auto_commit.py --dry-run 2>&1 | grep -A 10 '─' | head -12 | tail -10)"

# Commit feature 2
git add feature2.py
python scripts/auto_commit.py
```

### Integration with Makefile

Add shortcuts to `Makefile`:

```makefile
.PHONY: commit
commit:
	@python scripts/auto_commit.py

.PHONY: commit-dry
commit-dry:
	@python scripts/auto_commit.py --dry-run

.PHONY: commit-amend
commit-amend:
	@python scripts/auto_commit.py --amend
```

Usage:
```bash
make commit      # Generate and commit
make commit-dry  # Preview commit message only
make commit-amend # Amend last commit
```

## Troubleshooting

### Issue: API Key Not Set

**Error message:**
```
ERROR: ZHIPU_API_KEY not found
Please set environment variable: export ZHIPU_API_KEY='your-api-key'
```

**Solution:**
```bash
export ZHIPU_API_KEY="your-api-key"
```

Or add to `~/.bashrc`:
```bash
echo 'export ZHIPU_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

### Issue: No Staged Files

**Error message:**
```
No staged files detected. Exiting.
Hint: Use 'git add <files>' to stage changes first.
```

**Solution:**
```bash
# Stage all changes
git add .

# Or stage specific files
git add path/to/file.py
```

### Issue: Commit Message Doesn't Follow Format

**Warning message:**
```
⚠️  Warning: Commit message may not follow Conventional Commits format
Continue anyway? (y/N):
```

**Solution:**
- Enter `y` to continue with the commit message
- Or enter `N` to cancel and regenerate

If AI-generated message is not ideal, you can use `--allow-empty` to skip validation:
```bash
python scripts/auto_commit.py --allow-empty
```

### Issue: API Call Failed

**Error message:**
```
API Error 401: Invalid API key
```

Or

```
Error calling Zhipu API: <error details>
```

**Solution:**
1. Check if API key is correct
2. Check network connection
3. Check if API quota is sufficient
4. Try using a different model (such as `glm-4-flash`)

## Best Practices

### 1. Commit Granularity

**Recommended:** Each commit contains one independent feature or fix

```bash
# Good practice: Each commit focuses on one feature
git add auth.py
python scripts/auto_commit.py

git add user.py
python scripts/auto_commit.py
```

**Not recommended:** One commit contains multiple unrelated features

```bash
# Not recommended: Mixing multiple features
git add auth.py user.py payment.py
python scripts/auto_commit.py
```

### 2. Commit Timing

- ✅ Commit immediately after completing a feature
- ✅ Commit immediately after fixing a bug
- ✅ Commit immediately after refactoring
- ❌ Don't wait until massive changes to commit all at once

### 3. Use Dry-run for Preview

Preview before important commits:

```bash
python scripts/auto_commit.py --dry-run
```

### 4. Regularly Review Commit History

```bash
git log --oneline -10
git log --graph --all --decorate
```

### 5. Team Collaboration

Ensure team members understand Conventional Commits specification and use this script to maintain consistent commit style.

## Integration with auto_update_docs.py

### Complete Workflow

```bash
# 1. Develop feature
vim src/gns3_copilot/tools_v2/new_tool.py
vim tests/test_new_tool.py
vim docs/new-tool-guide.md

# 2. Commit code using auto_commit.py
git add .
python scripts/auto_commit.py

# 3. Push branch
git push origin feature-branch

# 4. Create PR (using auto_update_docs.py)
python scripts/auto_update_docs.py
```

### Command Comparison

| Script | Purpose | Trigger Timing | Output |
|--------|---------|---------------|--------|
| `auto_commit.py` | Generate commit message | Each local commit | Git commit |
| `auto_update_docs.py` | Update docs and create PR | When preparing to create PR | GitHub PR |

## FAQ

**Q: Can I commit multiple features at once?**

A: Technically yes, but not recommended. It's better to commit each feature separately for clarity and easier rollback.

**Q: What if AI-generated commit message is not ideal?**

A: You can use `--dry-run` to preview, then manually modify:
```bash
python scripts/auto_commit.py --dry-run
git commit -m "your-custom-message"
```

**Q: How do I modify a commit that has already been pushed?**

A: Use amend mode:
```bash
# Modify commit
python scripts/auto_commit.py --amend

# Force push
git push --force
```

**Q: Which commit types are supported?**

A: All types from Conventional Commits specification are supported: feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert

**Q: Can I customize commit message format?**

A: Yes, you can modify the `system_prompt` in the `call_zhipu_api()` function to customize the format.

## Related Resources

- [Conventional Commits Specification](https://www.conventionalcommits.org/)
- [auto_update_docs.py Documentation](./auto-doc-automation-guide.md)
- [GNS3 Copilot Project Home](../README.md)

## Version History

- **v1.0.0** (2025-01-05): Initial version
  - Basic commit message generation
  - Support for dry-run and amend modes
  - Integration with Zhipu GLM-4.5-X API
