# 文档自动更新脚本改进说明

## 问题背景

原始的 `scripts/auto_update_docs.py` 脚本在处理多个提交时存在以下问题：

1. **只分析 git diff**：脚本只查看当前分支与 `origin/Development` 之间的差异
2. **缺少上下文**：没有获取提交信息和现有文档内容
3. **重复功能**：AI 可能重复添加已存在的功能
4. **聚合不足**：无法智能合并多个相关提交的功能描述
5. **本地模式缺陷**：本地模式只关注文档变更，忽略了工具代码的新特性

## 改进方案

### 1. 新增上下文收集功能

#### `get_commit_messages()` 函数
```python
def get_commit_messages(base_ref: str = 'origin/Development') -> List[str]:
    """获取 PR 中的所有提交信息"""
```

- 功能：获取从 `origin/Development` 到当前 HEAD 的所有提交信息
- 用途：帮助 AI 理解完整的功能开发历史

#### `read_existing_documentation()` 函数
```python
def read_existing_documentation(doc_file: str, section: str) -> str:
    """从文档部分读取现有内容"""
```

- 功能：读取 README.md 和 README_ZH.md 中"核心功能"部分的现有内容
- 用途：让 AI 知道哪些功能已经记录，避免重复

### 2. 增强的 AI 提示词

更新后的 `call_zhipu_api_for_docs()` 函数现在接受额外的上下文参数：

```python
def call_zhipu_api_for_docs(
    prompt: str,
    commit_messages: List[str],
    existing_features_en: str = "",
    existing_features_zh: str = ""
) -> Optional[Dict]:
```

**系统提示词改进**：
- 明确指示 AI 对比现有文档
- 只添加未记录的新功能
- 合并多个提交的相关功能
- 返回空字符串如果所有功能都已记录

### 3. 改进的工作流程

在 GitHub Actions 模式下，脚本现在执行以下步骤：

```
1. 分析代码变更
   ↓
2. 获取所有提交信息 (get_commit_messages)
   ↓
3. 读取现有文档 (read_existing_documentation)
   ↓
4. 构建综合提示词（包含提交信息、diff、现有文档）
   ↓
5. 调用 AI 生成文档更新建议
   ↓
6. 记录更新建议（显示预览）
   ↓
7. 应用文档更新
   ↓
8. 提交更改并创建 PR 评论
```

### 4. 本地模式改进

**问题**：本地模式只关注文档变更，忽略了工具代码的新特性

**解决方案**：
- 本地模式现在也会获取提交信息
- 增强的 AI 提示词明确指示优先关注代码功能特性
- 提示词中的优先级说明：
  1. 新增的工具或函数
  2. 主要重构或架构变更
  3. Bug 修复和改进
  4. 配置或依赖变更

**改进后的本地模式输出**：
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

### 5. 增强的日志记录

脚本现在提供更详细的输出：

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

## 使用示例

### 本地模式（创建 PR）

```bash
export ZHIPU_API_KEY="your-api-key"
export GITHUB_TOKEN="your-github-token"
export REPO_OWNER="yueguobin"
export REPO_NAME="gns3-copilot"
python scripts/auto_update_docs.py
```

### GitHub Actions 模式（自动触发）

当 PR 创建或更新到 `Development` 分支时，工作流会自动：
1. 分析代码变更
2. 获取提交历史
3. 对比现有文档
4. 生成并应用文档更新
5. 在 PR 中添加评论说明更新内容

## 关键改进点

| 方面 | 改进前 | 改进后 |
|------|--------|--------|
| 上下文信息 | 只有 git diff | 提交信息 + git diff + 现有文档 |
| 功能聚合 | 只看当前 diff | 合并多个提交的相关功能 |
| 重复检测 | 无 | 对比现有文档，避免重复 |
| 日志输出 | 简单 | 详细，包括预览和验证 |
| 文档更新 | 可能重复 | 只添加新功能 |
| 本地模式 PR 生成 | 只关注文档变更 | 优先关注代码功能特性 |

## 注意事项

1. **API 密钥**：确保在 GitHub Secrets 中配置了 `ZHIPU_API_KEY`
2. **模型选择**：默认使用 `glm-4-flash`，可在 Secrets 中通过 `ZHIPU_MODEL` 修改
3. **分支策略**：PR 必须指向 `Development` 分支
4. **提交频率**：每次 PR 更新（opened/synchronize/reopened）都会触发

## 未来可能的改进

1. 支持更多文档部分（如架构、安装指南等）
2. 添加人工审查步骤，允许在提交前确认更改
3. 支持多语言文档同步更新
4. 添加更智能的功能去重算法
5. 支持自定义文档模板
