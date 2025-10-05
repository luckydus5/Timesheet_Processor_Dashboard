#!/bin/bash

# ☁️ Premium Timesheet Manager - OneDrive Style Dashboard
# Professional Cloud-Style Interface for Timesheet Processing

echo "☁️ Premium Timesheet Manager"
echo "=================================="
echo "🎨 OneDrive-Style Professional Interface"
echo "📊 Preserves Original Excel Structure"
echo "🧮 Adds Calculated Fields"
echo "✨ Premium Visual Experience"
echo ""

# Check if we're in the right directory
if [ ! -f "premium_timesheet_dashboard.py" ]; then
    echo "❌ Error: premium_timesheet_dashboard.py not found"
    echo "Please run this script from the Data Cleaner directory"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🔄 Activating virtual environment..."
    source .venv/bin/activate
fi

# Install/upgrade dependencies
echo "📦 Installing premium dependencies..."
pip install streamlit plotly pandas numpy openpyxl xlrd python-dateutil --quiet

echo "✅ Premium system ready!"
echo ""
echo "🚀 Launching Premium Timesheet Manager..."
echo "🎨 OneDrive-Style Interface Loading..."
echo ""
echo "📍 Access URLs:"
echo "   • Local:    http://localhost:8502"
echo "   • Network:  Will be shown below"
echo ""
echo "✨ Premium Features:"
echo "   • OneDrive-style file management"
echo "   • Original data preservation"
echo "   • Enhanced calculated columns"
echo "   • Professional cloud interface"
echo "   • Multi-format export options"
echo ""
echo "🛑 Press Ctrl+C to stop the premium dashboard"
echo "=================================="

# Launch Premium Streamlit dashboard on different port
python -m streamlit run premium_timesheet_dashboard.py --server.port 8502 --server.headless false