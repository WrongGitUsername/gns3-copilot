# UI Utils 模块使用说明

本目录包含可重用的 UI 组件模块，可以在任何 Streamlit 页面中使用。

## 可用模块

### 1. iframe_viewer.py - Iframe 查看器组件

用于在页面中嵌入外部网页内容的可重用组件。

#### 使用示例

```python
import streamlit as st
from gns3_copilot.ui_model.utils.iframe_viewer import render_iframe_viewer

# 使用默认 URL（从 session state 中的 CALIBRE_SERVER_URL 获取）
render_iframe_viewer()

# 自定义 URL
render_iframe_viewer(url="https://example.com")

# 自定义高度和标题
render_iframe_viewer(
    url="https://example.com",
    height=800,
    title="我的网站"
)
```

#### 参数说明

- `url` (str | None): iframe 中显示的 URL。如果为 None，则从 session state 的 `CALIBRE_SERVER_URL` 获取。
- `height` (int): iframe 高度（像素）。默认为 1000。如果 session state 中存在 `CONTAINER_HEIGHT`，则使用该值。
- `title` (str): 在 iframe 上方显示的标题。默认为空字符串。

---

### 2. notes_manager.py - 笔记管理组件

用于创建和管理 Markdown 笔记的完整系统，包括编辑器、列表管理、下载和删除功能。

#### 使用示例

```python
import streamlit as st
from gns3_copilot.ui_model.utils.notes_manager import render_notes_editor

# 使用默认设置
render_notes_editor()

# 自定义容器高度
render_notes_editor(container_height=900)
```

#### 参数说明

- `container_height` (int | None): 编辑器容器高度。如果为 None，则从 session state 的 `CONTAINER_HEIGHT` 获取。
- `show_title` (bool): 是否显示笔记管理标题。默认为 True。

#### 其他可用函数

除了主要的 `render_notes_editor()` 函数外，您还可以使用以下辅助函数：

```python
from gns3_copilot.ui_model.utils.notes_manager import (
    get_notes_directory,
    ensure_notes_directory,
    list_note_files,
    load_note_content,
    save_note_content,
    delete_note_file,
)

# 获取笔记目录
notes_dir = get_notes_directory()

# 确保笔记目录存在
notes_dir = ensure_notes_directory()

# 列出所有笔记文件
note_files = list_note_files()

# 加载笔记内容
content = load_note_content("my_note.md")

# 保存笔记内容
success = save_note_content("my_note.md", "新的笔记内容")

# 删除笔记文件
success = delete_note_file("my_note.md")
```

#### Session State 变量

笔记管理组件使用以下 session state 变量：

- `current_note_filename`: 当前选中的笔记文件名
- `current_note_content`: 当前笔记的内容
- `new_note_name`: 新笔记的名称
- `READING_NOTES_DIR`: 笔记目录路径（可选，默认为 "notes"）

#### AI 整理笔记功能

笔记管理组件内置了 AI 整理功能，可以使用 LLM 自动优化笔记的排版和格式。

**功能特点**：
- 优化排版和结构
- 修正错别字和语法错误
- 使用标准的 Markdown 格式
- 保持原始内容和风格
- 支持中英文笔记

**使用方法**：
1. 在笔记编辑器中，点击 `:material/auto_fix_high: AI Organize` 按钮
2. AI 会自动整理笔记内容
3. 在弹出的对话框中预览整理前后的对比
4. 点击"确认覆盖"应用整理结果，或"重新整理"再次尝试

**注意事项**：
- 需要在 Settings 中配置好 LLM 模型
- AI 使用 temperature=0.3 进行整理，以获得更一致的结果
- 如果笔记内容为空，则不会执行整理
- 整理结果会自动保存到文件

**自定义整理提示词**：
如需修改 AI 整理的行为，可以编辑 `src/gns3_copilot/prompts/notes_prompt.py` 文件中的 `SYSTEM_PROMPT`。

---

## 在其他页面中使用示例

### 在 chat.py 中添加笔记功能

```python
import streamlit as st
from gns3_copilot.ui_model.utils.notes_manager import render_notes_editor

# 在聊天页面底部添加笔记编辑器
st.markdown("---")
st.subheader("我的笔记")
render_notes_editor(container_height=600)
```

### 在 settings.py 中添加 iframe 查看器

```python
import streamlit as st
from gns3_copilot.ui_model.utils.iframe_viewer import render_iframe_viewer

# 在设置页面中显示帮助文档 iframe
render_iframe_viewer(
    url="https://docs.example.com",
    height=500,
    title="帮助文档"
)
```

### 创建自定义页面

```python
import streamlit as st
from gns3_copilot.ui_model.utils.iframe_viewer import render_iframe_viewer
from gns3_copilot.ui_model.utils.notes_manager import render_notes_editor

st.title("学习中心")

# 左右分栏布局
col1, col2 = st.columns([1, 1])

with col1:
    render_iframe_viewer(
        url="https://learning.example.com",
        title="在线课程"
    )

with col2:
    render_notes_editor()
```

---

## 注意事项

1. **Session State**: 这些组件使用 Streamlit 的 session state 来存储状态。确保在不同页面间使用时，session state 变量名称不会冲突。

2. **按键冲突**: 如果在多个页面中使用相同的组件，确保为每个组件使用唯一的 key 参数（如果组件支持）。

3. **笔记目录**: 笔记默认保存在 `notes` 目录中。可以通过设置 `st.session_state["READING_NOTES_DIR"]` 来更改。

4. **Iframe 安全性**: 确保 iframe 中嵌入的 URL 是可信的，避免安全风险。
