# LLM 快速配置指南

## 概述

GNS3 Copilot 通过预定义的提供商配置，提供了简化的 LLM 配置体验。这一功能显著降低了设置 LLM 提供商的复杂性，特别是对于新用户。

## 快速配置功能

设置页面现在包含"快速配置"部分，允许您从预定义的 LLM 提供商中选择，并自动填充配置。

### 支持的提供商类别

#### 🔗 聚合平台
- **OpenRouter**: 多提供商聚合器
  - 基础 URL: `https://openrouter.ai/api/v1`
  - 需要 API 密钥
  - 热门模型:
    - openai/gpt-4o-mini
    - openai/gpt-4o
    - anthropic/claude-3.5-sonnet
    - deepseek/deepseek-chat
    - google/gemini-flash-1.5

#### 🏢 第一方提供商
- **OpenAI**: 官方 OpenAI API
  - 基础 URL: `https://api.openai.com/v1`
  - 需要 API 密钥
  - 模型: gpt-4o-mini, gpt-4o, gpt-4-turbo, gpt-3.5-turbo, o1-mini, o1-preview

- **DeepSeek**: DeepSeek AI
  - 基础 URL: `https://api.deepseek.com/v1`
  - 需要 API 密钥
  - 模型: deepseek-chat, deepseek-coder

- **Anthropic**: Claude 模型
  - 基础 URL: `https://api.anthropic.com/v1`
  - 需要 API 密钥
  - 模型: claude-3.5-sonnet, claude-3.5-haiku, claude-3-opus

- **Google**: Gemini 模型
  - 基础 URL: `https://generativelanguage.googleapis.com/v1beta`
  - 需要 API 密钥
  - 模型: gemini-1.5-flash, gemini-1.5-pro, gemini-1.0-pro

- **xAI**: Grok 模型
  - 基础 URL: `https://api.x.ai/v1`
  - 需要 API 密钥
  - 模型: grok-beta, grok-2-vision

## 如何使用快速配置

### 步骤 1: 导航到设置页面
1. 打开 GNS3 Copilot
2. 在侧边栏中点击"设置"页面

### 步骤 2: 选择提供商
1. 在"LLM 模型配置"部分，找到"快速配置"
2. 点击"选择 LLM 提供商"下拉菜单
3. 从列表中选择您想要的提供商

### 步骤 3: 选择模型
1. 选择提供商后，会出现模型列表
2. 从下拉菜单中选择模型，或选择"自定义模型名称..."手动输入

### 步骤 4: 输入 API 密钥
1. 所有提供商都需要 API 密钥
2. 在"模型 API 密钥"字段中输入您的 API 密钥

### 步骤 5: 保存配置
1. 点击"保存设置到 .env"
2. 您的配置现已保存并准备使用

## 手动配置

对于需要自定义配置的高级用户：

1. 从提供商下拉菜单中选择"自定义"
2. 或使用快速配置下方的"手动配置"部分
3. 手动输入:
   - 模型提供商 (例如: openai, anthropic, deepseek)
   - 模型名称 (例如: gpt-4o-mini, claude-3.5-sonnet)
   - 基础 URL (如适用)
   - 模型 API 密钥 (如需要)
   - 模型温度 (可选，默认为 0.7)

## 添加新提供商

要添加新的预定义提供商，编辑 `src/gns3_copilot/ui_model/utils/llm_providers.py`:

```python
from gns3_copilot.ui_model.utils.llm_providers import LLM_PROVIDERS

LLM_PROVIDERS["新提供商"] = ProviderConfig(
    provider="provider_type",  # 例如: openai, anthropic
    base_url="https://api.provider.com/v1",
    models=["model1", "model2", "model3"],
    requires_api_key=True,
    category="first_party",  # 或 "aggregator"
)
```

## 故障排除

### 提供商无法工作
- 验证基础 URL 是否正确
- 检查 API 密钥是否有效（如需要）
- 确保服务可从您的网络访问
- 检查提供商文档是否有任何变更

### API 密钥问题
- 确保您已复制完整的 API 密钥
- 检查密钥是否有足够的权限
- 验证密钥是否未过期
- 检查提供商文档的密钥格式要求

## 最佳实践

1. **从入门级模型开始**: 使用 gpt-4o-mini 等模型进行测试和初始设置
2. **查看文档**: 始终查看提供商文档以了解模型功能
3. **保存配置**: 保存工作配置，以便需要时恢复
4. **监控使用情况**: 跟踪 token 使用情况以管理成本

## 配置持久化

所有配置都保存到项目目录中的 `.env` 文件。该文件包括:
- MODE_PROVIDER
- MODEL_NAME
- BASE_URL
- MODEL_API_KEY
- TEMPERATURE

您也可以根据需要手动编辑 `.env` 文件。

## 相关文档

- [GNS3 Copilot 用户指南](../README_ZH.md)
- [API 文档](../docs/)
- [贡献指南](../CONTRIBUTING.md)
