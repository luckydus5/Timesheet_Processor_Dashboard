#!/bin/bash

# 🧹 Timesheet Processor Dashboard Launcher
echo "🧹 Starting Timesheet Processor Dashboard..."
echo "📊 All-in-one timesheet processing, analysis, and cleaning"
echo ""

# Activate virtual environment
if [ -d ".venv" ]; then
    echo "🔄 Activating virtual environment..."
    source .venv/bin/activate
else
    echo "📦 Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
fi

# Install required packages
echo "📚 Installing dependencies..."
pip install --upgrade streamlit>=1.28.0 pandas>=2.0.0 plotly>=5.15.0 openpyxl>=3.1.0

# Clear cache
echo "🧹 Clearing cache..."
streamlit cache clear 2>/dev/null || true

# Launch dashboard
echo ""
echo "🚀 Launching Timesheet Processor Dashboard..."
echo "🌐 Opening on: http://localhost:8504"
echo "🧹 Ready to process your timesheet data!"
echo ""

python -m streamlit run timesheet_processor_dashboard.py --server.port 8504 --server.headless true