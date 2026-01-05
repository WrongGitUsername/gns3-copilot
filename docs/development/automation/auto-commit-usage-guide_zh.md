# 自动提交脚本使用说明

## 概述

`scripts/auto_commit.py` 是一个基于 Zhipu GLM-4.5-X API 的智能提交信息生成工具，可以自动分析代码变更并生成符合 Conventional Commits 规范的提交信息。

## 功能特性

- 🤖 **AI 驱动**：使用 Zhipu GLM-4.5-X 模型分析代码变更
- 📝 **规范格式**：自动生成符合 Conventional Commits 规范的提交信息
- 🔍 **智能分析**：理解代码变更的实际功能，而非仅文件列表
- ✅ **格式验证**：自动验证提交信息格式
- 🎯 **灵活选项**：支持 dry-run、amend 等多种模式

## 安装与配置

### 1. 环境要求

- Python 3.7+
- Git
- Zhipu AI API Key

### 2. 配置 API Key

```bash
export ZHIPU_API_KEY="your-api-key-here"

# 可选：自定义模型（默认使用 GLM-4.5-X）
export ZHIPU_MODEL="glm-4-flash"
```

### 3. 验证安装

```bash
python scripts/auto_commit.py --help
```

## 使用方法

### 基本用法

```bash
# 1. 暂存要提交的文件
git add <file1> <file2> ...
# 或
git add .

# 2. 运行脚本生成并执行提交
python scripts/auto_commit.py
```

### Dry Run 模式

只生成提交信息，不执行提交：

```bash
python scripts/auto_commit.py --dry-run
```

输出示例：
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

### Amend 模式

修改最后一次提交：

```bash
python scripts/auto_commit.py --amend
```

**注意**：修改提交后需要强制推送：
```bash
git push --force
```

### 组合选项

```bash
# Dry run + amend（预览要修改的提交信息）
python scripts/auto_commit.py --amend --dry-run
```

## Conventional Commits 规范

脚本遵循 Conventional Commits 规范：

### 格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 提交类型 (Type)

| 类型 | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): add OAuth2 login support` |
| `fix` | Bug 修复 | `fix(api): resolve timeout issue on slow connections` |
| `docs` | 文档变更 | `docs(readme): update installation instructions` |
| `style` | 代码风格（不影响功能） | `style(format): apply black formatting` |
| `refactor` | 代码重构 | `refactor(agent): simplify state machine logic` |
| `perf` | 性能优化 | `perf(caching): add LRU cache for config` |
| `test` | 测试相关 | `test(tools): add unit tests for config tools` |
| `chore` | 构建/工具/依赖等 | `chore(deps): upgrade nornir to 0.5.0` |
| `ci` | CI/CD 配置 | `ci(github): add automated testing workflow` |

### 范围 (Scope)

常用范围：
- `tools`: 工具层 (tools_v2/)
- `agent`: Agent 层 (agent/)
- `ui`: UI 层 (ui_model/)
- `client`: GNS3 客户端 (gns3_client/)
- `docs`: 文档 (docs/)
- `test`: 测试 (tests/)

### 示例提交信息

**简单提交：**
```
feat(tools): add network discovery tool
```

**带详细说明的提交：**
```
feat(voice): add TTS/STT voice interaction support

Implement text-to-speech and speech-to-text functionality
for hands-free operation with GNS3 Copilot.

Closes #123
```

**Bug 修复：**
```
fix(api): resolve connection timeout on slow networks

Increase timeout from 30s to 60s for network operations.
Add retry logic for transient failures.

Fixes #456
```

## 工作流程

### 推荐的开发流程

```bash
# 1. 进行代码更改
vim src/gns3_copilot/tools_v2/new_tool.py

# 2. 查看变更
git status
git diff

# 3. 暂存相关文件
git add src/gns3_copilot/tools_v2/new_tool.py

# 4. 使用脚本生成提交信息
python scripts/auto_commit.py

# 5. 确认提交信息后按 Enter（或输入 Y）
Commit with this message? (Y/n): [Enter]

# 6. 推送到远程
git push
```

### 完整示例

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

## 高级用法

### 自定义模型

```bash
export ZHIPU_MODEL="glm-4-flash"
python scripts/auto_commit.py
```

### 批量提交多个功能

```bash
# 提交功能 1
git add feature1.py
python scripts/auto_commit.py --dry-run
git commit -m "$(python scripts/auto_commit.py --dry-run 2>&1 | grep -A 10 '─' | head -12 | tail -10)"

# 提交功能 2
git add feature2.py
python scripts/auto_commit.py
```

### 集成到 Makefile

在 `Makefile` 中添加快捷命令：

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

使用：
```bash
make commit      # 生成并提交
make commit-dry  # 只预览提交信息
make commit-amend # 修改最后一次提交
```

## 故障排除

### 问题：API Key 未设置

**错误信息：**
```
ERROR: ZHIPU_API_KEY not found
Please set environment variable: export ZHIPU_API_KEY='your-api-key'
```

**解决方案：**
```bash
export ZHIPU_API_KEY="your-api-key"
```

或在 `~/.bashrc` 中添加：
```bash
echo 'export ZHIPU_API_KEY="your-api-key"' >> ~/.bashrc
source ~/.bashrc
```

### 问题：没有暂存的文件

**错误信息：**
```
No staged files detected. Exiting.
Hint: Use 'git add <files>' to stage changes first.
```

**解决方案：**
```bash
# 暂存所有变更
git add .

# 或暂存特定文件
git add path/to/file.py
```

### 问题：提交信息格式不符合规范

**警告信息：**
```
⚠️  Warning: Commit message may not follow Conventional Commits format
Continue anyway? (y/N):
```

**解决方案：**
- 输入 `y` 继续使用该提交信息
- 或输入 `N` 取消，重新生成

如果 AI 生成的信息不理想，可以使用 `--allow-empty` 跳过验证：
```bash
python scripts/auto_commit.py --allow-empty
```

### 问题：API 调用失败

**错误信息：**
```
API Error 401: Invalid API key
```

或

```
Error calling Zhipu API: <error details>
```

**解决方案：**
1. 检查 API Key 是否正确
2. 检查网络连接
3. 检查 API 额度是否充足
4. 尝试使用其他模型（如 `glm-4-flash`）

## 最佳实践

### 1. 提交粒度

**推荐：** 每次提交包含一个独立的功能或修复

```bash
# 好的做法：每个提交聚焦一个功能
git add auth.py
python scripts/auto_commit.py

git add user.py
python scripts/auto_commit.py
```

**不推荐：** 一次提交包含多个无关的功能

```bash
# 不推荐：混合多个功能
git add auth.py user.py payment.py
python scripts/auto_commit.py
```

### 2. 提交时机

- ✅ 完成一个功能后立即提交
- ✅ 修复 bug 后立即提交
- ✅ 重构完成后立即提交
- ❌ 不要等到大量变更后一次性提交

### 3. 使用 dry-run 预览

在重要提交前使用 dry-run 预览：

```bash
python scripts/auto_commit.py --dry-run
```

### 4. 定期查看提交历史

```bash
git log --oneline -10
git log --graph --all --decorate
```

### 5. 与团队协作

确保团队成员了解 Conventional Commits 规范，可以使用此脚本保持一致的提交风格。

## 与 auto_update_docs.py 配合使用

### 完整工作流

```bash
# 1. 开发功能
vim src/gns3_copilot/tools_v2/new_tool.py
vim tests/test_new_tool.py
vim docs/new-tool-guide.md

# 2. 使用 auto_commit.py 提交代码
git add .
python scripts/auto_commit.py

# 3. 推送分支
git push origin feature-branch

# 4. 创建 PR（使用 auto_update_docs.py）
python scripts/auto_update_docs.py
```

### 命令对比

| 脚本 | 用途 | 触发时机 | 输出 |
|------|------|----------|------|
| `auto_commit.py` | 生成提交信息 | 每次本地提交 | Git commit |
| `auto_update_docs.py` | 更新文档和创建 PR | 准备创建 PR 时 | GitHub PR |

## 常见问题 (FAQ)

**Q: 可以同时提交多个功能吗？**

A: 技术上可以，但不推荐。建议每个功能单独提交，这样更清晰且便于回滚。

**Q: AI 生成的提交信息不理想怎么办？**

A: 可以使用 `--dry-run` 预览，然后手动修改：
```bash
python scripts/auto_commit.py --dry-run
git commit -m "your-custom-message"
```

**Q: 如何修改已经推送的提交？**

A: 使用 amend 模式：
```bash
# 修改提交
python scripts/auto_commit.py --amend

# 强制推送
git push --force
```

**Q: 支持哪些提交类型？**

A: 支持 Conventional Commits 规范的所有类型：feat, fix, docs, style, refactor, perf, test, chore, ci, build, revert

**Q: 可以自定义提交信息格式吗？**

A: 可以修改 `call_zhipu_api()` 函数中的 `system_prompt` 来自定义格式。

## 相关资源

- [Conventional Commits 规范](https://www.conventionalcommits.org/)
- [auto_update_docs.py 文档](./auto-doc-automation-guide_zh.md)
- [GNS3 Copilot 项目主页](../README.md)

## 版本历史

- **v1.0.0** (2025-01-05): 初始版本
  - 支持基本的提交信息生成
  - 支持 dry-run 和 amend 模式
  - 集成 Zhipu GLM-4.5-X API
