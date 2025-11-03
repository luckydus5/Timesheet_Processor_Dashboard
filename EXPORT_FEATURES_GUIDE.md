# 📊 Export Features Guide - OT Management Format

## Overview
All exported Excel files now follow the **OT Management.xlsx** standard format with:
- ✅ **Overal Sheet**: Detailed records with all data
- ✅ **Consolidated Sheet**: Monthly summary by employee
- ✅ **Type of Work Dropdown**: Data validation in Overal sheet
- ✅ **Accurate Calculations**: All formulas verified and correct

---

## 🎯 Export Locations

### 1. **Tab 1: Timesheet Processing** 📊
**File Format**: `OT_Management_YYYYMMDD_HHMMSS.xlsx`

**Sheets Included:**
- **Overal**: 
  - All consolidated timesheet records
  - Contains selected display columns
  - Type of Work dropdown validation
  - Full detailed data with overtime calculations

- **Consolidated**:
  - Monthly summary grouped by Employee Name and Month
  - Columns: SN, EMPLOYEE NAME, Month, Days Worked, Total Hours, Total OT Hours
  - Aggregated data showing totals per employee per month

**Features:**
- ✅ Dropdown validation for "Type of Work" column
- ✅ Monthly aggregation (Days Worked, Total Hours, Total OT)
- ✅ Auto-generated SN (Serial Number)
- ✅ Date parsing and month extraction

---

### 2. **Tab 2: Attendance Consolidation** 🔄
**File Format**: `OT_Management_YYYYMMDD_HHMMSS.xlsx`

**Sheets Included:**
- **Overal**: 
  - Converted attendance to overtime format
  - All employee shifts with detailed times
  - Type of Work dropdown validation
  - Start Time, End Time, Break Time, Total Hours, OT calculations

- **Consolidated**:
  - Monthly summary by employee
  - Columns: SN, EMPLOYEE NAME, Month, Days Worked, Total Hours, Total OT Hours
  - Monthly aggregation of all attendance records

**Features:**
- ✅ Attendance to overtime conversion
- ✅ Shift time detection (Day/Night)
- ✅ Break time calculations
- ✅ Type of Work dropdown with 5 options
- ✅ Monthly consolidation

---

### 3. **Tab 4: Filter & Export by Date/Name** 🔍
**File Format**: `filtered_overtime_[filters]_YYYYMMDD_HHMMSS.xlsx`

**Example Filenames:**
- `filtered_overtime_09Oct2025_John_Doe_20251014_153045.xlsx`
- `filtered_overtime_multiple_dates_5_employees_20251014_153045.xlsx`

**Sheets Included:**
- **Overal**: 
  - Filtered records based on selected dates and/or employees
  - All original columns from source data
  - Type of Work dropdown validation
  - Full detail for selected criteria

- **Consolidated**:
  - Monthly summary of filtered data
  - Grouped by Employee Name and Month
  - Shows aggregated totals for filtered records only

- **Summary** (Optional):
  - Additional analytics sheet
  - Per-employee totals across all selected dates
  - Columns: SN, Employee Name, Number of Shifts, Total OT Hours, Dates Worked
  - Comma-separated list of dates worked

**Features:**
- ✅ Dynamic filename based on filters
- ✅ Optional Summary sheet (checkbox controlled)
- ✅ Both Overal and Consolidated sheets always included
- ✅ Type of Work dropdown validation
- ✅ Monthly aggregation even for filtered data

---

## 📋 Sheet Structure Details

### Overal Sheet (All Exports)
**Purpose**: Detailed record-level data

**Common Columns:**
- SN (Serial Number)
- EMPLOYEE NAME
- Date (dd-Mon-yyyy format)
- Type of Work (with dropdown)
- Start Time, End Time
- Break Time (in minutes)
- No. Hours (total work hours)
- Hrs at 1.5 rate (overtime hours)
- Shift Time (Day Shift / Night Shift)

**Features:**
- Every row represents one work shift/day
- Type of Work dropdown: Wagon, Superloader, Bulldozer/Superloader, Pump, Miller
- All calculations already applied
- Ready for manual edits with data validation

---

### Consolidated Sheet (All Exports)
**Purpose**: Monthly summary for payroll/reporting

**Columns:**
- SN (Serial Number)
- EMPLOYEE NAME
- Month (YYYY-MM format)
- Days Worked (count of working days)
- Total Hours (sum of all hours worked)
- Total OT Hours (sum of overtime hours)

**Calculation Logic:**
```
Days Worked = COUNT(Date) per employee per month
Total Hours = SUM(No. Hours) per employee per month
Total OT Hours = SUM(Hrs at 1.5 rate) per employee per month
```

**Features:**
- One row per employee per month
- Automatic month detection from dates
- Accurate aggregation formulas
- Serial number auto-generated

---

### Summary Sheet (Tab 4 Only - Optional)
**Purpose**: Cross-cutting analytics across filtered data

**Columns:**
- SN (Serial Number)
- Employee Name
- Number of Shifts (total count)
- Total OT Hours (sum across all dates)
- Dates Worked (comma-separated list)

**Use Case:**
- Quick view of employee performance
- List of specific dates worked
- Useful for targeted reports (e.g., "Show me all shifts for 10-Oct-2025")

---

## 🔧 Data Validation

### Type of Work Dropdown
**Applied To:** Overal sheet, "Type of Work" column

**Valid Options:**
1. Wagon
2. Superloader
3. Bulldozer/Superloader
4. Pump
5. Miller

**Validation Settings:**
- Shows dropdown arrow in Excel
- Prevents invalid entries
- Allows blank values
- Error message on invalid input
- Applied to all data rows (excluding header)

---

## ✅ Calculation Accuracy

### Overtime Calculations (Tab 1)
- Based on business rules in `timesheet_business_rules.py`
- Considers work hours, break times, and shift types
- Format: Decimal hours (e.g., 2.5 for 2 hours 30 minutes)
- Conversion available: `HH:MM:SS` ↔ Decimal

### Attendance to Overtime Conversion (Tab 2)
- Input: Check In/Check Out times
- Calculates: Break time, Total hours, OT hours
- Shift detection: Day Shift (<18:00) / Night Shift (≥18:00)
- Handles overnight shifts correctly

### Monthly Aggregation (Consolidated Sheet)
- Accurate date parsing: dd-Mon-yyyy format
- Month extraction: YYYY-MM period
- SUM aggregation: Total Hours, OT Hours
- COUNT aggregation: Days Worked

### Filter Calculations (Tab 4)
- Filters applied before aggregation
- Consolidated sheet shows filtered totals only
- Summary sheet provides additional analytics
- No data loss or miscalculation

---

## 📊 Export Process

### Tab 1 & Tab 2 Export Flow
1. Process timesheet/attendance data
2. Create Overal dataframe with all details
3. Generate Consolidated summary (monthly grouping)
4. Add Type of Work dropdown to Overal sheet
5. Save both sheets to Excel file
6. Provide download button

### Tab 4 Export Flow
1. User selects dates and/or employee names
2. Filter overal_df based on selections
3. Generate dynamic filename
4. Create Overal sheet with filtered data
5. Create Consolidated sheet (monthly summary of filtered data)
6. Optionally create Summary sheet (if checkbox selected)
7. Add Type of Work dropdown
8. Save all sheets to Excel file
9. Provide download button

---

## 🎯 Best Practices

### When to Use Each Export

**Tab 1 Export** - Use when:
- Processing raw timesheet data
- Need complete consolidated view
- Want all processed records with business rules applied

**Tab 2 Export** - Use when:
- Converting attendance (Check In/Check Out) to overtime format
- Have attendance data instead of timesheet
- Need shift time detection

**Tab 4 Export** - Use when:
- Need specific dates (e.g., daily reports for WhatsApp)
- Want specific employees only
- Creating targeted reports
- Generating payroll for selected period
- Need summary analytics sheet

### Filename Conventions

**Standard Format:**
- `OT_Management_YYYYMMDD_HHMMSS.xlsx` (Tab 1 & 2)
- `filtered_overtime_[criteria]_YYYYMMDD_HHMMSS.xlsx` (Tab 4)

**Tab 4 Dynamic Naming:**
- Single date: `filtered_overtime_09Oct2025_...`
- Multiple dates: `filtered_overtime_multiple_dates_...`
- Single employee: `filtered_overtime_..._John_Doe_...`
- Multiple employees: `filtered_overtime_..._5_employees_...`

---

## 🔍 Verification Checklist

### Before Using Export File

✅ **Overal Sheet Present**: Contains detailed records
✅ **Consolidated Sheet Present**: Contains monthly summary
✅ **Type of Work Dropdown**: Works correctly in Excel
✅ **Calculations Verified**: Numbers match expected totals
✅ **Date Format**: dd-Mon-yyyy (e.g., 09-Oct-2025)
✅ **Month Format**: YYYY-MM (e.g., 2025-10)
✅ **No Duplicate Rows**: Each record is unique in Overal
✅ **Aggregation Correct**: Consolidated totals match Overal sums

### Testing Calculations

**Manual Verification:**
1. Open Overal sheet
2. Filter by one employee and one month
3. Sum the "Hrs at 1.5 rate" column manually
4. Compare with corresponding row in Consolidated sheet
5. Should match exactly

**Example:**
```
Overal Sheet (John Doe, Oct 2025):
- 09-Oct-2025: 2.5 OT hours
- 10-Oct-2025: 3.0 OT hours
- 11-Oct-2025: 1.5 OT hours
Total: 7.0 OT hours

Consolidated Sheet:
John Doe | 2025-10 | 3 days | 7.0 OT hours ✅
```

---

## 📞 Support

If you notice any calculation discrepancies or export issues:

1. Check the date format in source data (should be dd-Mon-yyyy)
2. Verify "Type of Work" column exists in source
3. Ensure "EMPLOYEE NAME" column is present
4. Check for any error messages in the dashboard
5. Review this guide for expected behavior

**All exports now match the OT Management.xlsx standard format with accurate calculations!** ✅

---

**Last Updated**: October 14, 2025
**Version**: 2.0
**Developed by**: Olivier Dusabamahoro
