# Development Guide

## 🚀 Getting Started

### 1. Open Project in VS Code
```bash
cd ~/Desktop/Timesheet_Processor_Dashboard
code .
```

### 2. Activate Virtual Environment
```bash
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## 🛠️ VS Code Features

### Quick Actions

**F5** - Start debugging the dashboard
**Ctrl+Shift+P** - Command Palette
**Ctrl+`** - Toggle Terminal
**Ctrl+B** - Toggle Sidebar
**Ctrl+Shift+E** - Explorer
**Ctrl+Shift+F** - Search
**Ctrl+Shift+G** - Git
**Ctrl+Shift+X** - Extensions

### Running the Dashboard

**Method 1: Debug Mode (Recommended)**
- Press `F5` or go to Run & Debug panel
- Select "Python: Streamlit Dashboard"
- Dashboard will open in browser

**Method 2: Terminal**
```bash
streamlit run src/timesheet_dashboard.py
```

**Method 3: Task Runner**
- Press `Ctrl+Shift+P`
- Type "Tasks: Run Task"
- Select "Run Dashboard"

### Code Formatting

**Auto-format on save** is enabled with Black formatter
**Manual format**: `Ctrl+Shift+I` or `Alt+Shift+F`

### Git Integration

**GitLens Features:**
- Inline blame annotations
- File history
- Compare changes
- Repository graph

**Git Graph:**
- Visual commit history
- Branch visualization
- Easy merging and rebasing

### Code Navigation

**Bookmarks:**
- `Ctrl+Alt+K` - Toggle bookmark
- `Ctrl+Alt+L` - Jump to next bookmark
- `Ctrl+Alt+J` - Jump to previous bookmark

**TODO Management:**
- Add `# TODO:` comments in code
- View all TODOs in "TODO Tree" panel

### IntelliSense Features

- **Auto-completion**: Start typing and press `Ctrl+Space`
- **Parameter hints**: `Ctrl+Shift+Space`
- **Quick info**: Hover over any symbol
- **Go to definition**: `F12`
- **Find all references**: `Shift+F12`

## 📁 Project Structure

```
src/
├── core/              # Business logic
│   └── timesheet_business_rules.py
├── ui/                # UI components (future)
├── utils/             # Helper functions (future)
└── timesheet_dashboard.py

data/
├── samples/           # Sample input files
└── output/            # Generated output

docs/                  # Documentation
assets/                # Images and screenshots
```

## 🎨 Customization

### Change Theme
1. `Ctrl+K` `Ctrl+T`
2. Select your preferred theme

### Change File Icons
- Current: Material Icon Theme (installed)
- Shows beautiful icons for Python, CSV, JSON, etc.

### Customize Colors
Edit `.vscode/settings.json`:
```json
"workbench.colorCustomizations": {
    "activityBar.background": "#your-color"
}
```

## 🧪 Testing

### Manual Testing
Run individual test functions in the dashboard:
1. Navigate to Unit Tests tab
2. Click "Run Unit Tests"

### Python Debugging
- Set breakpoints: Click left of line number
- Start debugging: `F5`
- Step over: `F10`
- Step into: `F11`
- Continue: `F5`

## 📊 Productivity Tips

### Multi-Cursor Editing
- `Alt+Click` - Add cursor
- `Ctrl+Alt+↑/↓` - Add cursor above/below
- `Ctrl+D` - Select next occurrence

### Quick File Navigation
- `Ctrl+P` - Quick open file
- `Ctrl+Shift+O` - Go to symbol in file
- `Ctrl+T` - Go to symbol in workspace

### Code Snippets
Type these prefixes and press Tab:
- `def` - Function definition
- `class` - Class definition
- `if` - If statement
- `for` - For loop

### Error Detection
- **Error Lens** shows errors inline
- Red underlines = errors
- Yellow underlines = warnings
- Hover for details

## 🔍 Search & Replace

- `Ctrl+F` - Find in current file
- `Ctrl+H` - Find and replace in current file
- `Ctrl+Shift+F` - Find in all files
- `Ctrl+Shift+H` - Find and replace in all files

## 📝 Code Documentation

### Add Docstrings
```python
def function_name(param1, param2):
    """Brief description.
    
    Args:
        param1: Description
        param2: Description
        
    Returns:
        Description of return value
    """
    pass
```

### Type Hints
```python
def calculate_overtime(hours: float) -> float:
    return max(0, hours - 8)
```

## 🎯 Best Practices

1. **Format code** before committing (`Ctrl+Shift+I`)
2. **Write docstrings** for all functions
3. **Use type hints** for better IntelliSense
4. **Add TODO comments** for future improvements
5. **Commit frequently** with meaningful messages
6. **Use bookmarks** for important code sections

## 🚨 Troubleshooting

### IntelliSense Not Working
1. Check Python interpreter: Click bottom-left status bar
2. Select correct venv: `venv/bin/python`
3. Reload window: `Ctrl+Shift+P` → "Reload Window"

### Import Errors
1. Verify `PYTHONPATH` includes `src/` directory
2. Check `.vscode/settings.json` has correct paths
3. Restart VS Code

### Extensions Not Loading
1. `Ctrl+Shift+P`
2. "Developer: Reload Window"
3. Wait for extensions to activate (check bottom status bar)

## 💡 Additional Resources

- [VS Code Python Docs](https://code.visualstudio.com/docs/python/python-tutorial)
- [Streamlit Docs](https://docs.streamlit.io)
- [GitLens Docs](https://gitlens.amod.io)