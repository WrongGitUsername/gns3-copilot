# Notes Feature - User Guide

## Overview

GNS3 Copilot's Notes feature provides an integrated Markdown editor that allows you to document network configurations, topology documentation, and troubleshooting processes within the same interface, without switching to external note-taking applications (such as Obsidian, Notion, etc.).

## Key Features

### 1. Markdown Editor
- Full-featured Markdown editor based on Ace editor
- Syntax highlighting support
- Monokai theme
- Real-time preview functionality

### 2. File Management
- Create new Markdown note files
- Load and edit existing notes
- Delete unwanted notes
- Sidebar file list navigation

### 3. Auto-save
- Intelligent debounce auto-save (2-second delay)
- Auto-save status indicator
- Manual save button
- Real-time save status display

### 4. Project Integration
- Notes automatically saved to GNS3 project directory
- Project-level note isolation
- Uses `GNS3ProjectPath` tool to get project path

## Usage

### 1. Enable Notes Feature

The Notes feature is presented as a tab in the GNS3 Copilot interface, located next to Topology.

**Steps:**
1. Select a GNS3 project
2. Click the "Show" button to display the Topology panel
3. In the right panel, you will see two tabs:
   - 🌐 **Topology** - Displays GNS3 topology
   - 📝 **Notes** - Markdown note editor
4. Click the "📝 Notes" tab to enter the editor

### 2. Create New Note

**Steps:**
1. In the sidebar of the Notes page, click "Create New Note" to expand the area
2. Enter a filename (e.g., `config-notes`)
3. Click the "➕" button to create the file
4. The system will automatically create the file and add a basic heading

**Example:**
```
Input: config-notes
Created file: config-notes.md
Initial content:
# config-notes

```

### 3. Edit Notes

**Steps:**
1. Select the note to edit from the sidebar file list
2. Enter or modify content in the left editor
3. The right preview panel will display the rendered result in real-time
4. The system will automatically save 2 seconds after you stop typing

**Quick Actions:**
- Use the editor's syntax highlighting feature
- Supports standard Markdown syntax
- Manually click the "💾" button to save immediately

### 4. Delete Notes

**Steps:**
1. Select the note to delete in the sidebar
2. Click the "🗑️" button
3. Confirm the delete operation
4. The file will be permanently deleted

## Note Storage Location

Note files are stored in a subdirectory of the GNS3 project:

```
/home/user/GNS3/projects/{project_name}/notes/
├── config-notes.md
├── troubleshooting.md
└── deployment-guide.md
```

## Technical Implementation

### GNS3ProjectPath Tool

`GNS3ProjectPath` is a LangChain tool used to retrieve the local filesystem path of a GNS3 project.

**Tool Information:**
- **Name**: `get_gns3_project_path`
- **Input Parameters**:
  - `project_name`: GNS3 project name
  - `project_id`: GNS3 project UUID
- **Output**:
  ```python
  {
      "success": true,
      "project_path": "/home/user/GNS3/projects/mylab",
      "project_name": "mylab",
      "project_id": "ff8e059c-c33d-47f4-bc11-c7dda8a1d500",
      "message": "Successfully retrieved project path"
  }
  ```

**Usage Example:**
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

### Module Structure

```
src/gns3_copilot/
├── gns3_client/
│   └── gns3_project_path.py    # GNS3ProjectPath tool class
└── ui_model/
    └── notes.py                 # Notes editor UI component
```

### Dependencies

The Notes feature depends on the following packages:

- `streamlit-ace`: Streamlit's Ace editor component

**Install dependencies:**
```bash
pip install streamlit-ace
```

## API Reference

### render_notes_editor()

Renders the integrated Markdown note editor.

**Parameters:**
- `project_path` (str | None): GNS3 project directory path

**Returns:**
- None

**Usage Example:**
```python
from gns3_copilot.ui_model.notes import render_notes_editor

project_path = "/home/user/GNS3/projects/mylab"
render_notes_editor(project_path)
```

### get_notes_summary()

Gets note summary information for the project.

**Parameters:**
- `project_path` (str | None): GNS3 project directory path

**Returns:**
- dict: Note summary information
  ```python
  {
      "notes_count": 3,
      "notes_dir_exists": True,
      "notes_files": ["config-notes.md", "troubleshooting.md"]
  }
  ```

**Usage Example:**
```python
from gns3_copilot.ui_model.notes import get_notes_summary

summary = get_notes_summary(project_path)
print(f"Total notes: {summary['notes_count']}")
```

## Best Practices

### 1. Note Organization

Recommended way to organize notes:

- `project-overview.md` - Overall project description
- `config-notes.md` - Configuration records
- `troubleshooting.md` - Troubleshooting records
- `deployment-guide.md` - Deployment guide
- `test-results.md` - Test results

### 2. Markdown Format Recommendations

Use standard Markdown syntax:

```markdown
# Main Heading
## Subheading
### Third-level Heading

**Bold text**
*Italic text*

- Unordered list item
- Another list item

1. Ordered list item
2. Another ordered item

`Code snippet`

```python
def hello():
    print("Hello, GNS3!")
```

> Quoted text

[Link text](https://example.com)
```

### 3. Auto-save Notes

- The system will automatically save 2 seconds after you stop typing
- It is recommended to manually save after important changes
- Check the save status indicator to confirm save completion

## Troubleshooting

### Issue: Unable to access Notes feature

**Cause:**
- No GNS3 project selected
- GNS3 server connection failed

**Solution:**
1. Ensure a GNS3 project is selected
2. Check GNS3 server connection status
3. Visit Settings page to verify GNS3 server configuration is correct

### Issue: Notes cannot be saved

**Cause:**
- Insufficient GNS3 project directory permissions
- Insufficient disk space

**Solution:**
1. Check write permissions for GNS3 project directory
2. Ensure sufficient disk space
3. Check application logs for detailed error information

### Issue: Editor display issues

**Cause:**
- streamlit-ace component not properly installed
- Browser compatibility issues

**Solution:**
1. Reinstall streamlit-ace: `pip install --upgrade streamlit-ace`
2. Try using a modern browser (Chrome, Firefox, Edge)
3. Clear browser cache

## Future Improvement Plans

- [ ] Support note search functionality
- [ ] Add note templates
- [ ] Support note export (PDF, HTML)
- [ ] Add note version history
- [ ] Support image upload and insertion
- [ ] Add collaborative editing feature

## Feedback and Support

If you encounter issues or have improvement suggestions while using the Notes feature, please:

1. Submit an Issue to GitHub: https://github.com/yueguobin/gns3-copilot/issues
2. Check the documentation directory for more information
3. Refer to code examples and test cases

## License

This feature follows the open-source license of the GNS3 Copilot project.
