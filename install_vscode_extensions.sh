#!/bin/bash

# Install recommended VS Code extensions for Timesheet Dashboard project

echo "🚀 Installing VS Code Extensions for Python/Streamlit Development..."
echo "======================================================================"
echo ""

# Array of extension IDs
extensions=(
    "ms-python.python"
    "ms-python.vscode-pylance"
    "ms-python.black-formatter"
    "ms-python.isort"
    "ms-toolsai.jupyter"
    "pkief.material-icon-theme"
    "oderwat.indent-rainbow"
    "streetsidesoftware.code-spell-checker"
    "eamodio.gitlens"
    "donjayamanne.githistory"
    "mhutchie.git-graph"
    "github.vscode-pull-request-github"
    "visualstudioexptteam.vscodeintellicode"
    "visualstudioexptteam.intellicode-api-usage-examples"
    "usernamehw.errorlens"
    "wayou.vscode-todo-highlight"
    "gruntfuggly.todo-tree"
    "alefragnani.bookmarks"
    "christian-kohler.path-intellisense"
    "ms-vscode.live-server"
)

# Install each extension
for extension in "${extensions[@]}"
do
    echo "📦 Installing: $extension"
    code --install-extension "$extension" --force
done

echo ""
echo "✅ Installation complete!"
echo ""
echo "📋 Installed Extensions:"
echo "  • Python + Pylance (IntelliSense, linting)"
echo "  • Black Formatter (code formatting)"
echo "  • isort (import sorting)"
echo "  • Jupyter (notebook support)"
echo "  • Material Icon Theme (beautiful file icons)"
echo "  • Indent Rainbow (colorful indentation)"
echo "  • Code Spell Checker (typo detection)"
echo "  • GitLens + Git History (advanced git features)"
echo "  • Git Graph (visual git history)"
echo "  • GitHub Integration (PRs, issues)"
echo "  • IntelliCode (AI-assisted coding)"
echo "  • Error Lens (inline error display)"
echo "  • TODO Highlight + Tree (task management)"
echo "  • Bookmarks (code navigation)"
echo "  • Path IntelliSense (autocomplete paths)"
echo "  • Live Server (web preview)"
echo ""
echo "🔄 Please reload VS Code for changes to take effect"
echo "   Press: Ctrl+Shift+P → 'Developer: Reload Window'"
