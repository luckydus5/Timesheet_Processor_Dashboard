#!/bin/bash

# 🏆 ULTIMATE TIMESHEET PROCESSOR - Premium Launcher
# Professional Excel Enhancement System

echo "🏆 Starting Ultimate Timesheet Processor - Premium Edition"
echo "=============================================================="
echo "🎯 Features: Original Structure Preserved • Premium Design • Professional Excel Output"
echo ""

# Check if we're in the right directory
if [ ! -f "ultimate_timesheet_dashboard.py" ]; then
    echo "❌ Error: ultimate_timesheet_dashboard.py not found"
    echo "Please run this script from the Data Cleaner directory"
    exit 1
fi

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    echo "🔄 Activating premium environment..."
    source .venv/bin/activate
fi

# Install/upgrade dependencies
echo "📦 Installing premium dependencies..."
pip install -r requirements.txt --quiet

echo "✅ Premium environment ready"
echo ""
echo "🚀 Launching Ultimate Timesheet Processor..."
echo "📍 Premium Interface: http://localhost:8502"
echo "📍 Network Access: Will be shown below"
echo ""
echo "✨ PREMIUM FEATURES:"
echo "   🔒 Original Excel structure preserved (NO SORTING!)"
echo "   ➕ Enhanced calculations added to existing data"
echo "   🎨 Professional Excel formatting with highlighted enhancements"
echo "   📊 Advanced analytics and visualizations"
echo "   💎 Premium visual design"
echo "   ⚡ Real-time processing with progress tracking"
echo ""
echo "💡 USAGE:"
echo "   1. Upload your Excel/CSV timesheet file"
echo "   2. Click 'ENHANCE WITH PREMIUM CALCULATIONS'"
echo "   3. Explore analytics in premium dashboard"
echo "   4. Download enhanced Excel with professional formatting"
echo ""
echo "🛑 Press Ctrl+C to stop the premium system"
echo "=============================================================="

# Launch Premium Streamlit dashboard on different port
python -m streamlit run ultimate_timesheet_dashboard.py --server.port 8502 --server.headless false