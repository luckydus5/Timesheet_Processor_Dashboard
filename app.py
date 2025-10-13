#!/usr/bin/env python3
"""
Main entry point for Timesheet Processor Dashboard
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

# Import and run the dashboard
from timesheet_dashboard import main

if __name__ == "__main__":
    main()