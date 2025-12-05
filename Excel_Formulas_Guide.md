# 📊 Excel Formulas for Attendance Statistics Calculation

## 📋 Data Structure Assumption

Your attendance data has these columns:
- **Column A:** Department
- **Column B:** Name
- **Column C:** No.
- **Column D:** Date/Time
- **Column E:** Status (C/In, C/Out, OverTime In, OverTime Out)
- **Column F:** Location ID
- **Column G:** ID Number
- **Column H:** Workcode
- **Column I:** VerifyCode
- **Column J:** Comment

**Data starts from Row 4** (Row 1: Title, Row 2: Empty, Row 3: Headers)

---

## 🎯 Formula 1: Total Days Attended

**What it calculates:** Number of unique dates an employee has attendance records

### Formula (for specific employee):
```excel
=SUMPRODUCT((B:B="Employee Name")/COUNTIFS(B:B,"Employee Name",D:D,D:D))
```

### Example:
```excel
=SUMPRODUCT((B:B="Shillu John")/COUNTIFS(B:B,"Shillu John",D:D,D:D))
```

### How to use in a summary table:
If you have a list of employees in column M starting from M2:
```excel
=SUMPRODUCT((B:B=M2)/COUNTIFS(B:B,M2,D:D,D:D))
```

### Alternative Formula (Simpler but requires helper column):
1. Create helper column in K: `=B4&"|"&TEXT(D4,"DD-MMM-YYYY")`
2. Count unique: `=SUMPRODUCT((B:B="Employee Name")/-COUNTIF(K:K,K:K))`

---

## ⏰ Formula 2: Total Overtime Hours

**What it calculates:** Sum of overtime hours worked by an employee

### Step 1: Create Helper Column for Overtime Hours (Column K)

Put this formula in K4 and drag down:
```excel
=IF(AND(B4=B5, TEXT(D4,"DD-MMM-YYYY")=TEXT(D5,"DD-MMM-YYYY"), 
    OR(E4="OverTime In",E4="Overtime In"), 
    OR(E5="OverTime Out",E5="Overtime Out")),
    (D5-D4)*24, 0)
```

### Step 2: Sum Overtime Hours for Employee
```excel
=SUMIFS(K:K, B:B, "Employee Name")
```

### Combined Formula (Without Helper Column - Advanced):
```excel
=SUMPRODUCT((B4:B10000="Employee Name")*
    (B4:B10000=B5:B10001)*
    ((E4:E10000="OverTime In")+(E4:E10000="Overtime In"))*
    ((E5:E10001="OverTime Out")+(E5:E10001="Overtime Out"))*
    ((D5:D10001-D4:D10000)*24))
```

---

## 🌅 Formula 3: Weekend Days Worked

**What it calculates:** Number of unique weekend dates (Saturday/Sunday) worked

### Formula:
```excel
=SUMPRODUCT((B:B="Employee Name")*
    ((WEEKDAY(D:D)=1)+(WEEKDAY(D:D)=7))/
    COUNTIFS(B:B,"Employee Name",D:D,D:D))
```

**Note:** WEEKDAY returns 1 for Sunday, 7 for Saturday

### Alternative (if your weeks start Monday):
```excel
=SUMPRODUCT((B:B="Employee Name")*
    ((WEEKDAY(D:D,2)=6)+(WEEKDAY(D:D,2)=7))/
    COUNTIFS(B:B,"Employee Name",D:D,D:D))
```

**Note:** WEEKDAY(date,2) returns 6 for Saturday, 7 for Sunday

---

## 📅 Formula 4: Weekday Days Worked

**What it calculates:** Total Days Attended - Weekend Days

### Formula:
```excel
=SUMPRODUCT((B:B="Employee Name")/COUNTIFS(B:B,"Employee Name",D:D,D:D)) - 
 SUMPRODUCT((B:B="Employee Name")*((WEEKDAY(D:D)=1)+(WEEKDAY(D:D)=7))/COUNTIFS(B:B,"Employee Name",D:D,D:D))
```

### Simpler (if you already calculated Total Days and Weekend Days):
```excel
=[Total Days Attended] - [Weekend Days Worked]
```

---

## 📊 Formula 5: Total Records

**What it calculates:** Total number of check-in/check-out entries

### Formula:
```excel
=COUNTIF(B:B, "Employee Name")
```

### For summary table:
```excel
=COUNTIF(B:B, M2)
```

---

## 🔢 Formula 6: Overtime Days Count

**What it calculates:** Number of days employee worked overtime

### With Helper Column (Column L - Is Overtime Day):
Put this in L4 and drag down:
```excel
=IF(OR(E4="OverTime In", E4="Overtime In", E4="OverTime Out", E4="Overtime Out"), 
    B4&"|"&TEXT(D4,"DD-MMM-YYYY"), "")
```

Then count unique overtime days:
```excel
=SUMPRODUCT((B:B="Employee Name")/-COUNTIF(L:L,L:L&"")*(L:L<>""))
```

### Without Helper Column:
```excel
=SUMPRODUCT((B:B="Employee Name")*
    ((E:E="OverTime In")+(E:E="Overtime In")+(E:E="OverTime Out")+(E:E="Overtime Out"))/
    COUNTIFS(B:B,"Employee Name",D:D,D:D,E:E,E:E))
```

---

## 📋 Complete Summary Table Setup

### Create a summary sheet with these columns:

| Column | Header | Formula (starting Row 2) |
|--------|--------|--------------------------|
| M | Employee Name | (Manual list or `=UNIQUE(Sheet1!B:B)`) |
| N | Total Days Attended | `=SUMPRODUCT((Sheet1!B:B=M2)/COUNTIFS(Sheet1!B:B,M2,Sheet1!D:D,Sheet1!D:D))` |
| O | Total Records | `=COUNTIF(Sheet1!B:B,M2)` |
| P | Weekend Days | `=SUMPRODUCT((Sheet1!B:B=M2)*((WEEKDAY(Sheet1!D:D)=1)+(WEEKDAY(Sheet1!D:D)=7))/COUNTIFS(Sheet1!B:B,M2,Sheet1!D:D,Sheet1!D:D))` |
| Q | Weekday Days | `=N2-P2` |
| R | Total OT Hours | `=SUMIFS(Sheet1!K:K,Sheet1!B:B,M2)` (need helper column) |
| S | OT Days | `=SUMPRODUCT((Sheet1!B:B=M2)*((Sheet1!E:E="OverTime In")+(Sheet1!E:E="Overtime In"))/COUNTIFS(Sheet1!B:B,M2,Sheet1!D:D,Sheet1!D:D))` |

---

## 🏆 Top 10 Rankings

### Top 10 by Overtime Hours:
1. Sort your summary table by column R (Total OT Hours) in descending order
2. Take the first 10 rows

**Formula for dynamic Top 10:**
```excel
=LARGE($R$2:$R$1000, ROW()-1)
```

Then use INDEX-MATCH to get corresponding names:
```excel
=INDEX($M$2:$M$1000, MATCH(LARGE($R$2:$R$1000,ROW()-1), $R$2:$R$1000, 0))
```

### Top 10 by Weekend Days:
Same approach but use column P (Weekend Days)

### Top 10 by Daily Attendance:
Same approach but use column N (Total Days Attended)

---

## 💡 Pro Tips

### 1. Named Ranges
Create named ranges for easier formulas:
- `AttendanceData` = Sheet1!A:J
- `EmployeeNames` = Sheet1!B:B
- `Dates` = Sheet1!D:D
- `Status` = Sheet1!E:E

Then use:
```excel
=SUMPRODUCT((EmployeeNames="John")/COUNTIFS(EmployeeNames,"John",Dates,Dates))
```

### 2. Array Formulas (Excel 365)
If you have Excel 365, use dynamic arrays:
```excel
=UNIQUE(FILTER(B:B, B:B<>""))
```

### 3. Pivot Tables Alternative
Create a Pivot Table:
1. Insert > PivotTable
2. Rows: Name
3. Values: Date (Count of Unique Items)
4. This gives you Total Days Attended quickly!

---

## 🔧 Helper Columns Setup

### Column K: Overtime Hours Calculation
```excel
=IF(AND(B4=B5, TEXT(D4,"DD-MMM-YYYY")=TEXT(D5,"DD-MMM-YYYY"), 
    OR(E4="OverTime In",E4="Overtime In"), 
    OR(E5="OverTime Out",E5="Overtime Out")),
    (D5-D4)*24, 0)
```

### Column L: Date Only (for counting unique dates)
```excel
=TEXT(D4,"DD-MMM-YYYY")
```

### Column M: Is Weekend
```excel
=IF(OR(WEEKDAY(D4)=1, WEEKDAY(D4)=7), "Yes", "No")
```

### Column N: Employee-Date Combination (for unique counting)
```excel
=B4&"|"&TEXT(D4,"DD-MMM-YYYY")
```

---

## 📊 Example Calculation for "Shillu John"

Assuming data in rows 4-1000:

### Total Days Attended:
```excel
=SUMPRODUCT((B4:B1000="Shillu John")/COUNTIFS(B4:B1000,"Shillu John",D4:D1000,D4:D1000))
```
**Result:** 228 days

### Total Records:
```excel
=COUNTIF(B4:B1000,"Shillu John")
```
**Result:** 518 records

### Weekend Days:
```excel
=SUMPRODUCT((B4:B1000="Shillu John")*
    ((WEEKDAY(D4:D1000)=1)+(WEEKDAY(D4:D1000)=7))/
    COUNTIFS(B4:B1000,"Shillu John",D4:D1000,D4:D1000))
```
**Result:** 66 days

### Weekday Days:
```excel
=228 - 66
```
**Result:** 162 days

---

## ⚠️ Important Notes

1. **Adjust ranges:** Change `B:B`, `D:D` to specific ranges like `B4:B10000` for better performance

2. **Date format:** Ensure Date/Time column (D) is formatted as Date/Time in Excel

3. **Status values:** Check exact spelling of status values in your data:
   - "OverTime In" vs "Overtime In"
   - "C/In" vs "C/Out"

4. **Array formulas:** Press `Ctrl+Shift+Enter` for array formulas in older Excel versions

5. **Performance:** For large datasets (>10,000 rows), use helper columns instead of complex nested formulas

---

## 🎯 Quick Reference Card

| Metric | Formula Template |
|--------|------------------|
| **Days Attended** | `=SUMPRODUCT((B:B="Name")/COUNTIFS(B:B,"Name",D:D,D:D))` |
| **Total Records** | `=COUNTIF(B:B,"Name")` |
| **Weekend Days** | `=SUMPRODUCT((B:B="Name")*((WEEKDAY(D:D)=1)+(WEEKDAY(D:D)=7))/COUNTIFS(B:B,"Name",D:D,D:D))` |
| **Weekday Days** | `=[Days Attended] - [Weekend Days]` |
| **OT Hours** | `=SUMIFS(K:K,B:B,"Name")` (with helper column K) |
| **Records Count** | `=COUNTIF(B:B,"Name")` |

---

**Created:** December 5, 2025  
**Author:** Olivier
