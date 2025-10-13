#!/bin/bash

# 🧹 Timesheet Consolidator Dashboard Launcher
# Professional Web Interface for Timesheet Data Processing

echo "🧹 Starting Timesheet Consolidator Dashboard..."
echo "================================================"

# Check if we're in the right directory
if [ ! -f "timesheet_dashboard.py" ]; then
    echo "❌ Error: timesheet_dashboard.py not found"
    echo "Please run this script from the Data Cleaner directory"
    exit 1
fi

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3 first"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ Error: pip3 is not installed"
    echo "Please install pip3 first"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🔄 Activating virtual environment..."
    source .venv/bin/activate
fi

# Install/upgrade dependencies
echo "📦 Installing/updating dependencies..."
pip install -r requirements.txt --quiet

echo "✅ Dependencies installed successfully"
echo ""
echo "🚀 Launching dashboard..."
echo "📍 Local URL: http://localhost:8501"
echo "📍 Network URL: Will be shown below"
echo ""
echo "💡 Tips:"
echo "   - Upload your Excel/CSV timesheet files"
echo "   - Click 'Start Consolidation Process' to process data"
echo "   - Use the tabs to explore analytics"
echo "   - Download results as CSV or Excel"
echo ""
echo "🛑 Press Ctrl+C to stop the dashboard"
echo "================================================"

# Launch Streamlit dashboard
python -m streamlit run src/timesheet_dashboard.py --server.port 8501 --server.headless false
