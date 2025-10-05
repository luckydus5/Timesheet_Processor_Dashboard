# 🧹 Timesheet Consolidator Dashboard

## Professional Web Interface for Timesheet Data Processing

A powerful, user-friendly web dashboard that consolidates duplicate timesheet entries and applies business rules automatically. Perfect for HR departments, payroll processing, and workforce management.

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Streamlit-red?style=for-the-badge&logo=streamlit)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

## 🎯 Key Features

### 📂 **File Processing**
- **Multiple Formats**: Excel (.xlsx, .xls) and CSV files
- **Auto-Detection**: Automatically handles different column structures
- **Smart Parsing**: Splits combined Date/Time columns automatically
- **Error Handling**: Clear feedback for missing columns or invalid data

### 🧹 **Data Consolidation**
- **Duplicate Removal**: Merges multiple entries per employee per date
- **FIRST Check-in**: Uses earliest check-in as start time
- **LAST Check-out**: Uses latest check-out as end time
- **Real-time Progress**: Live progress tracking during processing

### 🎯 **Business Rules Engine**
- **Day Shift**: 8:00 AM - 17:00 PM (overtime after 5:00 PM)
- **Night Shift**: 18:00 PM - 3:00 AM (overtime after 3:00 AM)
- **Overtime Limits**: Automatic enforcement of min/max rules
- **Cross-midnight**: Handles shifts spanning midnight

### 📊 **Interactive Analytics**
- **Overview Dashboard**: Shift distribution, overtime analysis
- **Employee Analytics**: Individual performance metrics
- **Date Trends**: Daily patterns and insights
- **Overtime Analysis**: Detailed overtime breakdowns

### 💾 **Export Options**
- **CSV Export**: Clean data for further processing
- **Excel Export**: Professionally formatted with multiple sheets
- **Summary Reports**: Automatic generation of key metrics
- **Timestamped Files**: Organized file naming

## 🚀 Quick Start

### 1. **Installation**
```bash
# Clone or download the files to your computer
cd "/home/luckdus/Desktop/Data Cleaner"

# Install dependencies (automatic)
./launch_dashboard.sh
```

### 2. **Launch Dashboard**
```bash
# Option 1: Use the launcher script (recommended)
./launch_dashboard.sh

# Option 2: Manual launch
pip install -r requirements.txt
streamlit run timesheet_dashboard.py
```

### 3. **Access Dashboard**
- **Local**: http://localhost:8501
- **Network**: URL will be displayed in terminal

## 📋 Usage Guide

### **Step 1: Upload File**
1. Click "Browse files" in the sidebar
2. Select your timesheet file (Excel or CSV)
3. Dashboard automatically analyzes the file structure

### **Step 2: Review Analysis**
- View file overview and sample data
- Check duplicate entry statistics
- Review entry distribution charts

### **Step 3: Process Data**
1. Click "🧹 Start Consolidation Process"
2. Watch real-time progress
3. Review consolidation summary

### **Step 4: Explore Analytics**
- **Overview**: Shift distribution and overtime summary
- **By Employee**: Individual performance metrics
- **By Date**: Daily trends and patterns
- **Overtime**: Detailed overtime analysis

### **Step 5: Export Results**
- Download CSV for further processing
- Download Excel with summary sheets
- Files automatically timestamped

## 📊 Dashboard Sections

### **📂 File Upload & Analysis**
- **File Upload**: Drag-and-drop or browse for files
- **Data Overview**: Records, employees, date ranges
- **Sample Preview**: First 10 records display
- **Duplicate Analysis**: Statistics and visualizations

### **🧹 Consolidation Engine**
- **Progress Tracking**: Real-time processing updates
- **Business Rules**: Automatic application
- **Results Summary**: Before/after comparison
- **Success Feedback**: Clear status messages

### **📈 Analytics Tabs**
- **🎯 Overview**: High-level metrics and charts
- **👥 By Employee**: Individual performance analysis
- **📅 By Date**: Time-based trends
- **💼 Overtime**: Detailed overtime breakdowns

### **💾 Export Center**
- **CSV Download**: Raw consolidated data
- **Excel Download**: Multi-sheet workbook
- **Summary Reports**: Key metrics compilation
- **Flexible Naming**: Timestamped files

## 🎯 Business Rules

### **Day Shift Rules**
- **Official Hours**: 8:00 AM - 17:00 PM
- **Early Check-in**: Allowed, no overtime
- **Overtime Start**: After 17:00 PM (5:00 PM)
- **Overtime Limits**: 30 minutes minimum, 1.5 hours maximum

### **Night Shift Rules**
- **Official Hours**: 18:00 PM - 3:00 AM
- **Early Check-in**: Allowed, no overtime
- **Overtime Start**: After 3:00 AM (next day)
- **Overtime Limits**: 30 minutes minimum, 3 hours maximum

### **Consolidation Logic**
- **Start Time**: FIRST check-in (C/In or OverTime In)
- **End Time**: LAST check-out (C/Out or OverTime Out)
- **Multiple Entries**: Automatically merged per employee per date
- **Cross-midnight**: Properly handled for night shifts

## 📁 Required File Format

### **Column Requirements**
Your timesheet file must contain these columns:

| Column | Description | Example |
|--------|-------------|---------|
| `Name` | Employee name | "John Smith" |
| `Date` | Date of work | "05/10/2025" |
| `Time` | Time of entry | "08:30:15" |
| `Status` | Entry type | "C/In", "C/Out", "OverTime In", "OverTime Out" |

### **Alternative Formats**
- **Combined Date/Time**: Single column will be automatically split
- **Additional Columns**: Extra columns are preserved but not used
- **Different Names**: Column mapping can be added if needed

### **Supported Status Types**
- **C/In**: Regular check-in
- **C/Out**: Regular check-out
- **OverTime In**: Overtime check-in
- **OverTime Out**: Overtime check-out

## 🔧 Technical Details

### **Dependencies**
- **streamlit**: Web dashboard framework
- **pandas**: Data processing and analysis
- **plotly**: Interactive visualizations
- **openpyxl**: Excel file handling
- **numpy**: Numerical computations

### **Performance**
- **Processing Speed**: ~1000 records per second
- **Memory Usage**: Optimized for large datasets
- **Real-time Updates**: Live progress tracking
- **Error Resilience**: Graceful handling of data issues

### **Security**
- **Local Processing**: All data stays on your computer
- **No Cloud Upload**: Files never leave your system
- **Privacy First**: No data collection or tracking

## 🆘 Troubleshooting

### **Common Issues**

**File Upload Errors**
- ✅ Ensure file is Excel (.xlsx/.xls) or CSV
- ✅ Check required columns are present
- ✅ Verify data format consistency

**Processing Errors**
- ✅ Check date/time format consistency
- ✅ Ensure employee names don't have special characters
- ✅ Verify status values match expected types

**Performance Issues**
- ✅ For large files (>10,000 records), be patient
- ✅ Close other browser tabs to free memory
- ✅ Restart dashboard if it becomes unresponsive

### **Support**
If you encounter issues:
1. Check the terminal output for error messages
2. Verify your file format matches requirements
3. Try with a smaller sample file first
4. Restart the dashboard: Ctrl+C then relaunch

## 📈 Advanced Features

### **Custom Analytics**
The dashboard provides several analytical views:
- **Shift Distribution**: Pie charts and percentages
- **Employee Rankings**: Top performers by hours
- **Daily Trends**: Time series analysis
- **Overtime Patterns**: Distribution and statistics

### **Export Customization**
- **CSV**: Clean, minimal format for further processing
- **Excel**: Multi-sheet workbook with:
  - Consolidated_Data: Main results
  - Summary: Key metrics
  - Formatting: Professional styling

### **Real-time Processing**
- **Progress Bars**: Visual processing feedback
- **Status Updates**: Step-by-step information
- **Error Handling**: Clear error messages
- **Memory Management**: Efficient for large datasets

## 🏢 Use Cases

### **HR Departments**
- Process employee timesheet data
- Generate payroll-ready reports
- Analyze attendance patterns
- Identify overtime trends

### **Payroll Processing**
- Clean duplicate entries automatically
- Apply business rules consistently
- Export to payroll systems
- Validate overtime calculations

### **Workforce Management**
- Monitor employee hours
- Track shift patterns
- Analyze productivity metrics
- Generate compliance reports

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**🧹 Timesheet Consolidator Dashboard** - Making timesheet processing simple, accurate, and efficient.