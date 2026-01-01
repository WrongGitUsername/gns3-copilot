# Notes Feature - 使用指南

## 概述

GNS3 Copilot 的 Notes 功能提供了一个集成的 Markdown 编辑器，让您可以在同一个界面中记录网络配置、拓扑文档和故障排除过程，无需切换到外部笔记应用（如 Obsidian、Notion 等）。

## 主要特性

### 1. Markdown 编辑器
- 基于Ace编辑器的全功能Markdown编辑器
- 语法高亮支持
- Monokai 主题
- 实时预览功能

### 2. 文件管理
- 创建新的 Markdown 笔记文件
- 加载和编辑现有笔记
- 删除不需要的笔记
- 侧边栏文件列表导航

### 3. 自动保存
- 智能防抖自动保存（2秒延迟）
- 自动保存状态指示器
- 手动保存按钮
- 实时显示保存状态

### 4. 项目集成
- 笔记自动保存到 GNS3 项目目录
- 项目级别的笔记隔离
- 使用 `GNS3ProjectPath` 工具获取项目路径

## 使用方法

### 1. 启用 Notes 功能

Notes 功能在 GNS3 Copilot 界面中以标签页形式呈现，位于 Topology 旁边。

**步骤：**
1. 选择一个 GNS3 项目
2. 点击 "Show" 按钮显示 Topology 面板
3. 在右侧面板中，您会看到两个标签页：
   - 🌐 **Topology** - 显示 GNS3 拓扑
   - 📝 **Notes** - Markdown 笔记编辑器
4. 点击 "📝 Notes" 标签页进入编辑器

### 2. 创建新笔记

**步骤：**
1. 在 Notes 页面的侧边栏中，点击 "Create New Note" 展开区域
2. 输入文件名（例如：`config-notes`）
3. 点击 "➕" 按钮创建文件
4. 系统会自动创建文件并添加基本标题

**示例：**
```
输入：config-notes
创建文件：config-notes.md
初始内容：
# config-notes

```

### 3. 编辑笔记

**步骤：**
1. 在侧边栏文件列表中选择要编辑的笔记
2. 在左侧编辑器中输入或修改内容
3. 右侧预览面板会实时显示渲染结果
4. 系统会在停止输入 2 秒后自动保存

**快捷操作：**
- 使用编辑器的语法高亮功能
- 支持标准 Markdown 语法
- 可以手动点击 "💾" 按钮立即保存

### 4. 删除笔记

**步骤：**
1. 在侧边栏中选中要删除的笔记
2. 点击 "🗑️" 按钮
3. 确认删除操作
4. 文件将被永久删除

## 笔记存储位置

笔记文件存储在 GNS3 项目的子目录中：

```
/home/user/GNS3/projects/{project_name}/notes/
├── config-notes.md
├── troubleshooting.md
└── deployment-guide.md
```

## 技术实现

### GNS3ProjectPath 工具

`GNS3ProjectPath` 是一个 LangChain 工具，用于获取 GNS3 项目的本地文件系统路径。

**工具信息：**
- **名称**: `get_gns3_project_path`
- **输入参数**:
  - `project_name`: GNS3 项目名称
  - `project_id`: GNS3 项目 UUID
- **输出**:
  ```python
  {
      "success": true,
      "project_path": "/home/user/GNS3/projects/mylab",
      "project_name": "mylab",
      "project_id": "ff8e059c-c33d-47f4-bc11-c7dda8a1d500",
      "message": "Successfully retrieved project path"
  }
  ```

**使用示例：**
```python
from gns3_copilot.gns3_client import GNS3ProjectPath

tool = GNS3ProjectPath()
result = tool._run({
    "project_name": "mylab",
    "project_id": "ff8e059c-c33d-47f4-bc11-c7dda8a1d500"
})

if result["success"]:
    project_path = result["project_path"]
    print(f"Project path: {project_path}")
```

### 模块结构

```
src/gns3_copilot/
├── gns3_client/
│   └── gns3_project_path.py    # GNS3ProjectPath 工具类
└── ui_model/
    └── notes.py                 # Notes 编辑器 UI 组件
```

### 依赖项

Notes 功能依赖于以下包：

- `streamlit-ace`: Streamlit 的 Ace 编辑器组件

**安装依赖：**
```bash
pip install streamlit-ace
```

## API 参考

### render_notes_editor()

渲染集成的 Markdown 笔记编辑器。

**参数：**
- `project_path` (str | None): GNS3 项目目录路径

**返回：**
- None

**使用示例：**
```python
from gns3_copilot.ui_model.notes import render_notes_editor

project_path = "/home/user/GNS3/projects/mylab"
render_notes_editor(project_path)
```

### get_notes_summary()

获取项目的笔记摘要信息。

**参数：**
- `project_path` (str | None): GNS3 项目目录路径

**返回：**
- dict: 笔记摘要信息
  ```python
  {
      "notes_count": 3,
      "notes_dir_exists": True,
      "notes_files": ["config-notes.md", "troubleshooting.md"]
  }
  ```

**使用示例：**
```python
from gns3_copilot.ui_model.notes import get_notes_summary

summary = get_notes_summary(project_path)
print(f"Total notes: {summary['notes_count']}")
```

## 最佳实践

### 1. 笔记组织

建议按以下方式组织笔记：

- `project-overview.md` - 项目总体说明
- `config-notes.md` - 配置记录
- `troubleshooting.md` - 故障排除记录
- `deployment-guide.md` - 部署指南
- `test-results.md` - 测试结果

### 2. Markdown 格式建议

使用标准 Markdown 语法：

```markdown
# 主标题
## 二级标题
### 三级标题

**粗体文本**
*斜体文本*

- 无序列表项
- 另一个列表项

1. 有序列表项
2. 另一个有序项

`代码片段`

```python
def hello():
    print("Hello, GNS3!")
```

> 引用文本

[链接文本](https://example.com)
```

### 3. 自动保存注意事项

- 系统会在停止输入 2 秒后自动保存
- 建议在重要更改后手动保存
- 查看保存状态指示器确认保存完成

## 故障排除

### 问题：无法访问 Notes 功能

**原因：**
- 未选择 GNS3 项目
- GNS3 服务器连接失败

**解决方案：**
1. 确保已选择一个 GNS3 项目
2. 检查 GNS3 服务器连接状态
3. 查看 Settings 页面确认 GNS3 服务器配置正确

### 问题：笔记无法保存

**原因：**
- GNS3 项目目录权限不足
- 磁盘空间不足

**解决方案：**
1. 检查 GNS3 项目目录的写权限
2. 确保磁盘有足够空间
3. 查看应用日志获取详细错误信息

### 问题：编辑器显示异常

**原因：**
- streamlit-ace 组件未正确安装
- 浏览器兼容性问题

**解决方案：**
1. 重新安装 streamlit-ace：`pip install --upgrade streamlit-ace`
2. 尝试使用现代浏览器（Chrome、Firefox、Edge）
3. 清除浏览器缓存

## 未来改进计划

- [ ] 支持笔记搜索功能
- [ ] 添加笔记模板
- [ ] 支持笔记导出（PDF、HTML）
- [ ] 添加笔记版本历史
- [ ] 支持图片上传和插入
- [ ] 添加协作编辑功能

## 反馈与支持

如果您在使用 Notes 功能时遇到问题或有改进建议，请：

1. 提交 Issue 到 GitHub: https://github.com/yueguobin/gns3-copilot/issues
2. 查看文档目录获取更多信息
3. 参考代码示例和测试用例

## 许可证

本功能遵循 GNS3 Copilot 项目的开源许可证。
