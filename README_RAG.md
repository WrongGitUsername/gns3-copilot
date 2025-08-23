# 🧠 RAG增强的网络智能代理

## 概述

这个增强版本集成了RAG（Retrieval-Augmented Generation）技术，可以将网络排错书籍、文档向量化，根据用户问题智能检索相关命令和解决方案。

## 🚀 主要特性

### 1. 多知识源融合
- **RAG知识库**: 向量化的网络排错文档
- **基础命令库**: 预定义的网络命令集合  
- **关键词搜索**: 传统的关键词匹配

### 2. 智能命令选择
- LLM根据问题复杂度自动选择命令数量
- 考虑RAG上下文进行更准确的命令推荐
- 支持多设备批量执行

### 3. 灵活配置
- 可通过配置文件启用/禁用RAG功能
- 支持多种文档格式（PDF、TXT、MD、DOCX）
- 自定义向量模型和参数

## 📚 安装和配置

### 1. 快速安装
```bash
# 安装所有依赖并初始化系统
python setup_rag.py --all
```

### 2. 分步安装
```bash
# 1. 安装RAG依赖
python setup_rag.py --install

# 2. 初始化RAG系统
python setup_rag.py --init

# 3. 启用RAG配置
python setup_rag.py --enable

# 4. 测试系统
python setup_rag.py --test
```

### 3. 添加知识库文档

将您的网络排错书籍和文档放入 `knowledge_base/` 目录：

```
knowledge_base/
├── cisco_troubleshooting_guide.pdf
├── ospf_complete_guide.pdf
├── bgp_best_practices.md
├── network_protocols_handbook.txt
└── routing_troubleshooting.docx
```

支持的格式：
- PDF文件 (`.pdf`)
- 文本文件 (`.txt`) 
- Markdown文件 (`.md`)
- Word文档 (`.docx`)

### 4. 配置文件说明

编辑 `rag_config.ini` 自定义设置：

```ini
[rag]
# 启用RAG功能
enabled = true

# 知识库路径
knowledge_base_path = ./knowledge_base

# 向量存储路径
vector_store_path = ./vector_store

# 向量模型（中文支持）
embedding_model = shibing624/text2vec-base-chinese

[knowledge_sources]
# 知识源优先级
rag_kb_priority = 10
base_kb_priority = 5
keyword_search_priority = 1
```

## 💡 使用示例

### 1. 基础查询
```
🙋 您: R-1的OSPF邻居状态如何？

🤖 助手: [执行 show ip ospf neighbor，基于基础知识库]
```

### 2. 复杂故障排除
```
🙋 您: OSPF邻居无法建立，可能是什么原因？

🤖 助手: [RAG检索相关文档，执行多个诊断命令]
- show ip ospf neighbor
- show ip ospf interface  
- debug ip ospf adj
[提供详细的故障排除建议]
```

### 3. 路由宣告问题
```
🙋 您: R-5向R-4宣告了哪些路由？

🤖 助手: [结合RAG建议和命令执行]
- show ip ospf neighbor
- show ip route ospf
[分析路由宣告详情]
```

## 🔧 高级功能

### 1. 自定义知识库
添加您的专有文档到知识库：

```python
from core.network_rag_kb import NetworkTroubleshootingRAG

# 初始化RAG系统
rag = NetworkTroubleshootingRAG()

# 重新加载文档（当添加新文档时）
rag.add_documents_from_directory("./knowledge_base")
```

### 2. 手动查询RAG
```python
# 直接查询RAG知识库
results = rag.search_commands("BGP路由黑洞问题", k=5)

for result in results:
    print(f"相关性: {result['score']:.2f}")
    print(f"建议命令: {result['commands']}")
    print(f"上下文: {result['summary']}")
```

### 3. 性能优化
- 使用GPU加速向量计算（如果可用）
- 调整文档分块大小优化检索精度
- 自定义相似度阈值过滤无关结果

## 🆚 RAG vs 传统方法对比

| 特性 | 传统硬编码 | RAG增强 |
|------|-----------|---------|
| 命令覆盖范围 | 有限，需手动添加 | 广泛，基于文档内容 |
| 故障诊断能力 | 基础 | 专业，基于最佳实践 |
| 维护成本 | 高，需要代码修改 | 低，只需更新文档 |
| 上下文理解 | 弱 | 强，理解问题背景 |
| 扩展性 | 差 | 好，支持新协议/技术 |

## 🛠️ 故障排除

### 1. RAG依赖安装失败
```bash
# 单独安装问题包
pip install faiss-cpu sentence-transformers
pip install langchain langchain-community
```

### 2. 向量模型下载慢
```python
# 使用国内镜像
export HF_ENDPOINT=https://hf-mirror.com
```

### 3. 内存不足
```ini
# 在配置文件中调整参数
[rag]
chunk_size = 500
search_results = 3
```

### 4. 检索结果不准确
- 检查文档质量和格式
- 调整相似度阈值
- 增加相关文档到知识库

## 📈 性能监控

系统会显示详细的执行信息：
```
🧠 RAG知识库返回了 3 个相关命令
📚 找到 8 个相关命令（来源：RAG + 基础知识库）  
🤖 LLM选择的命令: ['show ip ospf neighbor', 'show ip route ospf']
```

## 🔮 未来计划

1. **多模态支持**: 处理网络拓扑图片
2. **实时学习**: 从执行结果中学习优化
3. **协作知识库**: 支持团队共享知识
4. **云端同步**: 知识库云端备份和同步

## 🙋‍♂️ 常见问题

**Q: 需要什么样的文档质量？**
A: 建议使用结构化好的技术文档，包含明确的命令示例和故障排除步骤。

**Q: 支持中文文档吗？**
A: 是的，系统使用中文向量模型，完全支持中文文档。

**Q: 如何更新知识库？**
A: 只需将新文档放入knowledge_base目录，系统会自动重新向量化。

**Q: 可以禁用RAG功能吗？**
A: 可以，在rag_config.ini中设置enabled=false即可回退到基础模式。

---

🎯 **现在您有了一个真正智能的网络故障排除助手！**

只需要将您的网络技术书籍和文档放入知识库，系统就能基于专业文档提供准确的命令建议和故障排除方案。
