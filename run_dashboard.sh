#!/bin/bash

# 🚀 TIMESHEET PROCESSOR DASHBOARD LAUNCHER
# =========================================
# Simple script to launch your timesheet dashboard locally

echo "🧹 Starting Timesheet Processor Dashboard..."
echo "📊 Enhanced with cross-midnight shift detection"
echo ""

# Navigate to project directory
cd /home/luckdus/Desktop/Timesheet_Processor_Dashboard

# Set up PATH for streamlit
export PATH="$HOME/.local/bin:$PATH"

# Check if streamlit is available
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing dependencies..."
    python3 -m pip install --user streamlit pandas plotly openpyxl --break-system-packages
    export PATH="$HOME/.local/bin:$PATH"
fi

# Clear any previous streamlit cache
echo "🧹 Clearing cache..."
streamlit cache clear 2>/dev/null || true

# Launch the dashboard
echo ""
echo "🚀 Launching Timesheet Processor Dashboard..."
echo "🌐 Opening on: http://localhost:8505"
echo "💡 Press Ctrl+C to stop the dashboard"
echo ""

# Run the dashboard
streamlit run timesheet_processor_dashboard.py --server.port 8505