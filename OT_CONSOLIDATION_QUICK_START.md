# 🚀 Quick Start Guide - OT Consolidation Feature

## What This Feature Does

The **OT Consolidation (1.5x)** feature automatically:
1. Reads your "Consolidated OT management" Excel file
2. Calculates overtime hours at 1.5x rate using the Excel formula logic
3. Groups overtime by employee and month
4. Provides verification that calculations match your Excel formulas
5. Exports results in multiple formats

## Step-by-Step Usage

### 1. Open the Dashboard
```bash
# Activate virtual environment
.\dashboard\Scripts\Activate.ps1

# Run dashboard
streamlit run timesheet_dashboard.py
```

### 2. Navigate to OT Consolidation Tab
- Click on the **"💰 OT Consolidation (1.5x)"** tab
- This is the 5th tab in the navigation

### 3. Upload Your Excel File
- Click "Browse files" button
- Select your "Consolidated OT management2.xlsx" file
- File must contain:
  - **"Overal" sheet** with time records
  - **"Consolidated" sheet** for monthly summary

### 4. View Results

#### 📊 Summary Tab
- See total employees, records, OT hours
- View top 10 OT earners (bar chart)
- Check OT distribution histogram

#### 🔍 Detailed Records Tab
- View all calculations in a table
- Filter by employee name
- Filter by date range
- See both Excel and calculated values

#### 📈 Consolidated View Tab
- Employee × Month matrix
- Monthly totals per employee
- Overall totals
- Download consolidated CSV

#### ⚖️ Formula Verification Tab
- Match rate percentage
- Detailed comparison table
- Highlights any mismatches
- Should show 100% match

### 5. Export Your Data

Three export options available:

**Option 1: Detailed Records (CSV)**
- All records with calculations
- Start/end times included
- Compare Excel vs Python calculations

**Option 2: Consolidated (CSV)**
- Employee × Month summary
- Monthly totals
- Grand total per employee

**Option 3: Full Report (Excel)**
- Multiple sheets:
  - Overal_Updated
  - Consolidated_New
  - Verification
- Complete audit trail

## Expected File Structure

Your Excel file should have this structure:

### Sheet: "Overal"
```
Row 3 (Headers):
A: SN | B: EMPLOYEE NAME | C: JOB TITLE | D: Date | 
E: Start time | F: End time | G: No. Hours | H: Hrs at 1.5 rate | 
I: Type of Work | J: Direct Supervisor | K: Department

Row 4+ (Data):
1 | John Doe | Operator | 2025-10-10 | 16:23:00 | 07:50:00 | 15.45 | 3.0 | ...
```

### Sheet: "Consolidated"
```
Row 1 (Headers):
A: SN | B: Name | C: Oct 2025 | D: Nov 2025 | E: Dec 2025 | F: Total

Row 2+ (Data):
1 | John Doe | 3.0 | 1.5 | 0.0 | 4.5
```

## Formula Logic Explained

### The Excel Formula:
```excel
=IF(OR(ISBLANK(E4),ISBLANK(F4),ISNA(E4),ISNA(F4)),"",
IF(E4<TIME(16,20,0),
   IF((F4+IF(F4<E4,1,0))>TIME(17,0,0),
      IF((F4+IF(F4<E4,1,0)-TIME(17,0,0))*24>=0.5,
         MIN(1.5,(F4+IF(F4<E4,1,0)-TIME(17,0,0))*24),
      0),
   0),
IF(AND(E4>=TIME(16,20,0),F4<E4),
   3,
0)))
```

### What It Means:

**Scenario 1: Day Shift (Start < 16:20)**
- Checks if employee works past 17:00
- Calculates hours after 17:00
- Only counts if >= 30 minutes (0.5 hours)
- Maximum 1.5 hours OT at 1.5x rate

**Example:**
- Start: 06:45, End: 18:30
- Hours after 17:00: 1.5 hours
- OT at 1.5x: 1.5 hours ✓

**Scenario 2: Night Shift (Start >= 16:20, crosses midnight)**
- Fixed 3 hours OT at 1.5x rate
- No calculation needed

**Example:**
- Start: 16:23, End: 07:50 (next day)
- OT at 1.5x: 3.0 hours ✓

**Scenario 3: Regular Shift (no OT)**
- Start: 06:30, End: 16:00
- Ends before 17:00
- OT at 1.5x: 0.0 hours

## Troubleshooting

### Issue: File upload fails
**Solution:** Ensure your file:
- Is in Excel format (.xlsx or .xls)
- Has "Overal" and "Consolidated" sheets
- Has proper column structure

### Issue: Calculation mismatches
**Solution:** Check:
- Time format is correct (HH:MM:SS)
- Dates are valid
- No extra spaces in employee names
- Headers start at row 3 in Overal sheet

### Issue: Missing employees in consolidated view
**Solution:** Verify:
- Employee names match exactly between sheets
- Names don't have extra spaces
- Check for spelling variations

## Tips for Best Results

1. **Clean Data**: Remove empty rows from Overal sheet
2. **Consistent Names**: Ensure employee names are spelled exactly the same
3. **Valid Dates**: Make sure Date column has proper date format
4. **Time Format**: Use HH:MM:SS format for Start/End times
5. **Regular Backups**: Keep original Excel file as backup before using this tool

## Support

For issues or questions:
1. Check the "📖 View Expected File Structure" section in the dashboard
2. Review the Formula Verification tab for calculation details
3. Export the Full Report (Excel) to see all intermediate calculations

---

**Ready to Use!** 🎉

Navigate to the dashboard, upload your file, and let the system do the work!
