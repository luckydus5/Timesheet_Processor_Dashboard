/bin/bash

# 🎨 Beautiful Dashboard Launcher
echo "✨ Starting Beautiful Timesheet Dashboard..."
echo "🎨 Ultra-modern design with stunning visuals"
echo "📊 Professional analytics and charts"
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

# Install/upgrade required packages
echo "📚 Installing beautiful dashboard dependencies..."
pip install --upgrade streamlit>=1.28.0 pandas>=2.0.0 plotly>=5.15.0 openpyxl>=3.1.0 numpy

# Clear any existing streamlit cache
echo "🧹 Clearing cache for fresh start..."
streamlit cache clear 2>/dev/null || true

# Launch the beautiful dashboard
echo ""
echo "🚀 Launching Beautiful Dashboard..."
echo "🌐 Opening on: http://localhost:8503"
echo "✨ Get ready for an amazing experience!"
echo ""

# Run with specific port for beautiful dashboard
python -m streamlit run beautiful_dashboard.py --server.port 8503 --server.headless true

echo ""
echo "👋 Beautiful Dashboard closed. Thank you!"