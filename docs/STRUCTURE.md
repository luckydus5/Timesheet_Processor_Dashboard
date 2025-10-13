# Project Structure

```
Timesheet_Processor_Dashboard/
│
├── src/                          # Source code
│   ├── core/                     # Core business logic
│   │   └── timesheet_business_rules.py
│   ├── ui/                       # UI components
│   ├── utils/                    # Utility functions
│   └── timesheet_dashboard.py   # Main dashboard
│
├── data/                         # Data files
│   ├── samples/                  # Sample data
│   └── output/                   # Processed output
│
├── docs/                         # Documentation
│
├── assets/                       # Static assets
│   ├── images/                   # Images
│   └── screenshots/              # Screenshots
│
├── .vscode/                      # VS Code configuration
│   ├── settings.json            # Editor settings
│   ├── launch.json              # Debug configurations
│   ├── tasks.json               # Build tasks
│   └── extensions.json          # Recommended extensions
│
├── venv/                         # Virtual environment
│
├── app.py                        # Main entry point
├── requirements.txt              # Python dependencies
├── launch_dashboard.sh           # Launch script
├── README.md                     # Project documentation
└── .gitignore                    # Git ignore rules
```

## Development Workflow

1. **Activate virtual environment**: `source venv/bin/activate`
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run dashboard**: `python -m streamlit run src/timesheet_dashboard.py`
4. **Debug**: Use VS Code debug configuration (F5)