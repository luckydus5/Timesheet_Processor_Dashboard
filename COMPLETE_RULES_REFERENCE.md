# 📚 Complete Rules Reference - Timesheet Consolidator Dashboard

## Table of Contents
1. [Business Rules](#business-rules)
2. [Error Handling Rules](#error-handling-rules)
3. [Data Processing Rules](#data-processing-rules)
4. [Overtime Calculation Rules](#overtime-calculation-rules)
5. [Validation Rules](#validation-rules)

---

## 1. Business Rules

### 1.1 Shift Classification Rules

#### **Night Shift Detection**
- **Threshold:** Check-in time ≥ **16:10** (4:10 PM)
- **Calculation:** `checkin_hour = hour + (minutes / 60)` where `checkin_hour ≥ 16.1667`
- **Example:** 
  - 16:10 → Night Shift ✅
  - 18:24 → Night Shift ✅
  - 16:05 → Day Shift ❌

#### **Day Shift Detection**
- **Threshold:** Check-in time < **16:10**
- **Standard Hours:** 08:00 AM - 17:00 PM
- **Note:** Employees can check in **before 08:00 AM** (e.g., 07:00), but:
  - All hours are counted in total
  - **NO overtime** for early arrival
  - Overtime **only after 17:00 PM**
- **Example:**
  - 07:00 check-in → Day Shift ✅ (all hours counted, no early OT)
  - 08:00 check-in → Day Shift ✅
  - 15:30 check-in → Day Shift ✅
  - 16:15 check-in → Night Shift ❌

### 1.2 Working Hours Rules

#### **Standard Working Hours**
- **Day Shift:** 8-9 hours (08:00 - 17:00)
- **Night Shift:** 8-13 hours (16:10 - next day 07:00)
- **Maximum Shift:** No hard limit, but >16 hours triggers warning
- **Minimum Shift:** <4 hours triggers data quality alert

#### **Break Time**
- **Not deducted automatically** from total hours
- Must be handled manually or in raw data

### 1.3 Overtime Rules

#### **Day Shift Overtime**
- **Standard Work:** 08:00 AM - 17:00 PM
- **Early Check-In:** Allowed (e.g., 07:00 AM), **but NO overtime for early arrival**
- **OT Starts:** After **17:00 PM** (5:00 PM) **ONLY**
- **Minimum:** Must work ≥30 minutes **after 17:00** to qualify
- **Maximum:** 1.5 hours per shift
- **Formula:** `OT = MIN(1.5, MAX(0, end_time - 17:00)) if >= 0.5 else 0`
- **Example:** Check-in 07:00, check-out 17:30 → Total: 10.5h, OT: 0.5h (only after 17:00)

#### **Night Shift Overtime**
- **Detection:** Check-in ≥ **16:10 PM** (identifies as night shift)
- **Work Counted:** 18:00 PM - 03:00 AM (next day)
- **OT Starts:** After **03:00 AM** (next day) **ONLY**
- **Minimum:** Must work ≥30 minutes **after 03:00 AM** to qualify
- **Maximum:** 3.0 hours per shift
- **Formula:** `OT = MIN(3.0, MAX(0, end_time - 03:00)) if >= 0.5 else 0`
- **Example:** Check-in 18:00, check-out 03:35 → Total: 9.58h, OT: 0.58h (only after 03:00)

#### **Excel Formula OT (1.5x Rate)**
This is a **separate calculation** used in the OT Consolidation tab:

**Logic:**
```
IF Start Time < 16:20:
    IF End Time > 17:00:
        IF (End - 17:00) >= 0.5 hours:
            OT = MIN(1.5, End - 17:00)
        ELSE:
            OT = 0
    ELSE:
        OT = 0

ELSE IF Start Time >= 16:20 AND crosses midnight:
    OT = 3.0 (fixed)

ELSE:
    OT = 0
```

**Key Differences:**
- **Threshold:** 16:20 (vs 16:10 for shift detection)
- **Night Shift OT:** Fixed **3 hours** (vs variable)
- **Purpose:** Matches Excel payroll formula exactly

---

## 2. Error Handling Rules

### 2.1 Missing Check-In

#### **Detection:**
- Record shows Check-Out status without prior Check-In
- Status contains "Out" but no matching "In" before it

#### **Handling:**
1. **Estimate Check-In Time:** 8 hours before check-out
2. **Mark Status:** `"Estimated (Missing Check-In)"`
3. **Show Warning:** Display to user in UI
4. **Create Record:** Normal processing with estimated data

#### **Example:**
```
Input:  23/08/2025 18:24:23 - C/Out (ERROR: No check-in!)

Output: 
  Check In Status: Estimated (Missing Check-In)
  Start Time: 10:24:23 (8 hours before)
  Check Out Status: C/Out
  End Time: 18:24:23
  Total Hours: 8.00
  
Warning: ⚠️ Employee - Found check-out without check-in on 23/08/2025 at 18:24. Estimated check-in time.
```

### 2.2 Missing Check-Out

#### **Detection:**
- Record shows Check-In status without subsequent Check-Out
- Status contains "In" but no matching "Out" after it

#### **Handling:**
1. **Estimate Check-Out Time:** 8 hours after check-in
2. **Mark Status:** `"Estimated"`
3. **Create Record:** Normal processing with estimated data

#### **Example:**
```
Input:  23/08/2025 08:00:00 - C/In (No check-out recorded)

Output:
  Check In Status: C/In
  Start Time: 08:00:00
  Check Out Status: Estimated
  End Time: 16:00:00 (8 hours after)
  Total Hours: 8.00
```

### 2.3 Duplicate Check-In

#### **Detection:**
- Two or more consecutive Check-In records without Check-Out between them

#### **Handling:**
1. **Use First Check-In:** Earliest check-in time is used
2. **Ignore Subsequent:** Later check-ins are skipped
3. **No Warning:** Silent handling (common user error)

#### **Example:**
```
Input:
  23/08/2025 08:00:00 - C/In  ← USED
  23/08/2025 08:01:00 - C/In  ← IGNORED
  24/08/2025 07:00:00 - C/Out

Output: One record with 08:00:00 check-in
```

### 2.4 Duplicate Check-Out

#### **Detection:**
- Two or more consecutive Check-Out records without Check-In between them

#### **Handling:**
1. **Use First Check-Out:** Earliest check-out time is used
2. **Ignore Subsequent:** Later check-outs are skipped
3. **No Warning:** Silent handling

#### **Example:**
```
Input:
  23/08/2025 18:00:00 - C/In
  24/08/2025 07:00:00 - C/Out  ← USED
  24/08/2025 07:01:00 - C/Out  ← IGNORED

Output: One record with 07:00:00 check-out
```

### 2.5 Orphaned Records

#### **Definition:**
- Check-In/Check-Out records that cannot be paired
- Usually due to data corruption or incomplete records

#### **Handling:**
1. **Orphaned Check-Out:** Estimate check-in (see 2.1)
2. **Orphaned Check-In:** Estimate check-out (see 2.2)
3. **Track in Report:** Count in data quality metrics

### 2.6 Data Quality Reporting

#### **Metrics Displayed:**
- ✅ **Total Pairs Created:** Successfully paired records
- ⚠️ **Missing Check-Ins:** Count of estimated check-ins
- ⚠️ **Missing Check-Outs:** Count of estimated check-outs
- 📊 **Data Accuracy:** `(Perfect Pairs / Total Pairs) × 100%`

#### **Warning Threshold:**
- Display warning if `(Missing Check-Ins + Missing Check-Outs) > 0`
- Expandable details show all problematic records

#### **Example Report:**
```
✅ Total Pairs Created: 150
⚠️ Missing Check-Ins: 3 (Estimated)
⚠️ Missing Check-Outs: 5 (Estimated)
📊 Data Accuracy: 94.7%

⚠️ Data Quality Alert: Found 8 records with estimation. 
Please review employee attendance procedures.
```

---

## 3. Data Processing Rules

### 3.1 Date/Time Parsing Rules

#### **Supported Date Formats:**
1. `dd/mm/yyyy HH:MM:SS` (e.g., 23/08/2025 18:24:23)
2. `dd-mmm-yy HH:MM:SS` (e.g., 23-Aug-25 18:24:23)
3. `mm/dd/yyyy HH:MM:SS` (fallback)
4. Pandas auto-detection (fallback)

#### **Parsing Priority:**
1. Try `dd/mm/yyyy HH:MM:SS` first
2. If fails, try `dd-mmm-yy HH:MM:SS`
3. If fails, try `mm/dd/yyyy HH:MM:SS`
4. If all fail, use pandas `to_datetime()` with coercion

#### **Invalid Dates:**
- Set to `NaT` (Not a Time)
- Record skipped from processing
- Counted in validation errors

### 3.2 Status Detection Rules

#### **Valid Check-In Statuses:**
- `"C/In"` - Regular check-in
- `"OverTime In"` - Overtime check-in
- Any status containing `"In"` (case-insensitive)

#### **Valid Check-Out Statuses:**
- `"C/Out"` - Regular check-out
- `"OverTime Out"` - Overtime check-out
- Any status containing `"Out"` (case-insensitive)

#### **Status Validation:**
- Must contain either `"In"` or `"Out"`
- Case-insensitive matching
- Whitespace tolerant
- Records without valid status are skipped

### 3.3 Midnight Crossing Detection

#### **Night Shift Logic:**
- **Condition:** `check_in_time >= 16:10 AND check_out_time < check_in_time`
- **Action:** Assume check-out is **next day**
- **Calculation:** Add 1 day to check-out date

#### **Example:**
```
Check-In:  23/08/2025 18:24:23
Check-Out: 24/08/2025 07:41:56

Detection:
  18:24 (18.4 hours) >= 16:10 → Night Shift ✅
  07:41 < 18:24 → Crosses midnight ✅
  
Result:
  Date: 23/08/2025 (check-in date)
  Total Hours: ~13.3 hours (18:24 → next day 07:41)
```

#### **Day Shift Logic:**
- **Condition:** `check_in_time < 16:10`
- **Action:** Prefer **same-day** check-out
- **Fallback:** If no same-day check-out, use next day

### 3.4 Pairing Algorithm

#### **Process Flow:**
```
1. Sort all records chronologically (Date, Time)
2. Group by employee name
3. For each record:
   a. If Check-In:
      - Determine if night shift (>= 16:10)
      - If night shift: Search NEXT DAY for check-out
      - If day shift: Search SAME DAY first, then next day
      - If no check-out found: ESTIMATE (+8 hours)
      - Create paired record
      - Mark both as "used"
   
   b. If Check-Out (without prior check-in):
      - ESTIMATE check-in (-8 hours)
      - Mark as "Estimated (Missing Check-In)"
      - Show warning
      - Create paired record
      
   c. If Already Used:
      - Skip (prevents double-counting)
```

#### **Priority Rules:**
- **Night Shifts:** Next-day check-outs preferred
- **Day Shifts:** Same-day check-outs preferred
- **Chronological Order:** First available check-out is used
- **No Duplicates:** Each record used only once

---

## 4. Overtime Calculation Rules

### 4.1 Day Shift OT Calculation

#### **Rule:**
- **OT Starts:** 17:00 PM (5:00 PM)
- **Minimum Qualification:** Employee must work **at least 30 minutes AFTER 17:00** to earn overtime
- **Maximum OT:** 1.5 hours per shift

#### **Formula:**
```python
if shift_type == "Day Shift":
    if end_time > time(17, 0):  # After 5 PM
        ot_duration = end_time - time(17, 0)
        ot_hours = ot_duration.total_seconds() / 3600
        
        if ot_hours >= 0.5:  # Minimum 30 minutes AFTER 17:00
            overtime = min(1.5, ot_hours)  # Maximum 1.5 hours
        else:
            overtime = 0  # Less than 30 min = NO overtime
    else:
        overtime = 0  # Ended at or before 17:00 = NO overtime
```

#### **Examples:**
```
End Time: 17:00 → OT: 0 hours → Result: 0 (exactly at 17:00, no OT)
End Time: 17:25 → OT: 0.42 hours → Result: 0 (below 30 min minimum)
End Time: 17:29 → OT: 0.48 hours → Result: 0 (still below 30 min)
End Time: 17:30 → OT: 0.50 hours → Result: 0.5 hours ✅ (exactly 30 min)
End Time: 17:35 → OT: 0.58 hours → Result: 0.58 hours ✅
End Time: 18:00 → OT: 1.0 hours → Result: 1.0 hours ✅
End Time: 18:30 → OT: 1.5 hours → Result: 1.5 hours ✅ (at max)
End Time: 19:00 → OT: 2.0 hours → Result: 1.5 hours (capped at max)
End Time: 16:50 → OT: 0 hours → Result: 0 (finished before 17:00)
```

#### **Key Points:**
- ✅ Must finish work **after 17:00** (5:00 PM)
- ✅ Must work **at least 30 minutes** after 17:00 to qualify
- ✅ OT is calculated from 17:00, not from actual end time
- ❌ Working 17:00-17:29 = **NO overtime** (below minimum)
- ✅ Working 17:00-17:30 = **0.5 hours overtime** (minimum met)
- ✅ Working 17:00-18:30 = **1.5 hours overtime** (maximum reached)

### 4.2 Night Shift OT Calculation

#### **Formula:**
```python
if shift_type == "Night Shift":
    # Handle midnight crossing
    if end_time < start_time:
        end_datetime = datetime.combine(date + timedelta(days=1), end_time)
    else:
        end_datetime = datetime.combine(date, end_time)
    
    ot_threshold = datetime.combine(date + timedelta(days=1), time(3, 0))
    
    if end_datetime > ot_threshold:  # After 3 AM
        ot_duration = end_datetime - ot_threshold
        ot_hours = ot_duration.total_seconds() / 3600
        
        if ot_hours >= 0.5:  # Minimum 30 minutes
            overtime = min(3.0, ot_hours)  # Maximum 3.0 hours
        else:
            overtime = 0
    else:
        overtime = 0
```

#### **Examples:**
```
Start: 18:24, End: 03:25 (next day) → OT: 0.42 hours → Result: 0 (below 0.5h)
Start: 18:24, End: 03:35 (next day) → OT: 0.58 hours → Result: 0.58 hours
Start: 18:24, End: 05:00 (next day) → OT: 2.0 hours → Result: 2.0 hours
Start: 18:24, End: 07:00 (next day) → OT: 4.0 hours → Result: 3.0 hours (capped)
Start: 18:24, End: 02:00 (next day) → OT: 0 hours → Result: 0 (before 3 AM)
```

### 4.3 Excel Formula OT (1.5x Rate)

#### **Used in:** OT Consolidation tab only

#### **Formula:**
```python
def calculate_overtime_15_rate(start_time, end_time):
    # Convert to decimal hours
    start_decimal = start_time.hour + start_time.minute / 60
    end_decimal = end_time.hour + end_time.minute / 60
    
    # Check for midnight crossing
    if end_time < start_time:
        end_decimal += 24
    
    # Day shift logic (start < 16:20)
    if start_decimal < 16.333:  # 16:20
        if end_decimal > 17.0:
            ot = end_decimal - 17.0
            if ot >= 0.5:
                return min(1.5, ot)
        return 0
    
    # Night shift logic (start >= 16:20 and crosses midnight)
    elif start_decimal >= 16.333 and end_time < start_time:
        return 3.0
    
    else:
        return 0
```

#### **Key Differences from Main OT:**
- Threshold: **16:20** (not 16:10)
- Night shift OT: **Fixed 3 hours** (not variable)
- No 3 AM threshold for night shifts
- Purpose: Match Excel payroll formula exactly

---

## 5. Validation Rules

### 5.1 Data Quality Checks

#### **Pre-Processing Validation:**
1. **Required Columns:**
   - `Name` or `EMPLOYEE NAME`
   - `Date` or `DATE`
   - `Time` or inline date-time
   - `Status` or `STATUS`

2. **Non-Empty Check:**
   - DataFrame must have at least 1 row
   - Required columns must have at least some non-null values

3. **Date Validity:**
   - Dates must parse successfully
   - Future dates beyond 1 year trigger warning
   - Dates before 2000 trigger warning

#### **Post-Processing Validation:**
1. **Paired Records:**
   - Each check-in should have matching check-out
   - Orphaned records tracked and reported

2. **Time Logic:**
   - Check-out must be after check-in (accounting for midnight)
   - Total hours should be > 0 and < 24

3. **Overtime Logic:**
   - OT hours must be <= total hours
   - OT hours must be >= 0

### 5.2 Warning Triggers

#### **Critical Warnings (Red):**
- More than 20% of records have estimations
- Any employee with >12 average hours per shift
- Any single shift >16 hours
- More than 10% of records fail to parse

#### **Medium Warnings (Yellow):**
- 5-20% of records have estimations
- Any employee with >10 average hours per shift
- Any single shift >14 hours
- Missing check-ins or check-outs detected

#### **Info Notices (Blue):**
- Less than 5% of records have estimations
- All records within normal parameters
- Data quality >95%

### 5.3 Business Rule Violations

#### **Violations Tracked:**
1. **Invalid OT:** OT calculated when end time is before OT threshold
2. **Negative Hours:** Total hours calculation results in negative value
3. **Excessive Hours:** Single shift >20 hours
4. **Too Short:** Shift <2 hours (may indicate error)

#### **Actions Taken:**
- **Log Warning:** Display in UI
- **Flag Record:** Add to "Review Needed" list
- **Continue Processing:** Don't block the record
- **Track Count:** Show in data quality report

---

## 6. Export Rules

### 6.1 Output Columns

#### **Consolidated Output:**
- `Name` - Employee name
- `Date` - Work date (check-in date)
- `Check In Status` - Original or "Estimated"
- `Start Time` - Check-in time (HH:MM:SS)
- `Check Out Status` - Original or "Estimated"
- `End Time` - Check-out time (HH:MM:SS)
- `Total Hours` - Decimal hours worked
- `Overtime Hours` - Formatted (HH:MM:SS)
- `Overtime Hours (Decimal)` - Decimal OT hours
- `Original Entries` - Count of raw records
- `Entry Details` - Full timestamp details

#### **Columns REMOVED (per user request):**
- ~~`Shift Time`~~ - Removed
- ~~`Monthly_OT_Summary`~~ - Removed

### 6.2 Excel Export Structure

#### **Sheet 1: Overal**
- All detailed records
- One row per work day per employee
- Type of Work dropdown enabled
- Formatted with borders and headers

#### **Sheet 2: Consolidated**
- Monthly summary by employee
- Pivot format: Employee × Month
- Total column at end
- Conditional formatting for high OT

#### **Sheet 3: Summary (Optional)**
- Top performers by OT
- Department/supervisor summaries
- Monthly trends
- Data quality statistics

---

## 7. Configuration Rules

### 7.1 System Settings

#### **Estimation Window:**
- Default: **8 hours**
- Configurable: No (hardcoded)
- Used for both missing check-in and check-out

#### **Night Shift Threshold:**
- Default: **16:10** (16.1667 hours)
- Configurable: No (hardcoded)
- Critical for shift classification

#### **OT Thresholds:**
- Day shift OT start: **17:00** (5 PM)
- Night shift OT start: **03:00 AM** (next day)
- Configurable: No (business rules)

#### **OT Limits:**
- Day shift max: **1.5 hours**
- Night shift max: **3.0 hours**
- Minimum: **0.5 hours** (30 minutes)
- Configurable: No (business rules)

### 7.2 UI Settings

#### **Show Estimation Warnings:**
- Default: **OFF**
- User Configurable: ✅ Yes (sidebar checkbox)
- Effect: Shows/hides inline warnings for estimated records

#### **Date Format Display:**
- Output: `dd-mmm-yyyy` (e.g., 23-Aug-2025)
- Input: Multiple formats accepted
- Configurable: No

#### **Time Format:**
- Display: `HH:MM:SS` (24-hour)
- Internal: datetime objects
- Configurable: No

---

## 8. Summary of Key Rules

### Priority Rules (Most Important):
1. ⭐ **Night Shift = 16:10+** (16.1667 hours)
2. ⭐ **Missing Check-In = Estimate -8 hours**
3. ⭐ **Missing Check-Out = Estimate +8 hours**
4. ⭐ **Night Shifts → Prioritize Next Day Check-Out**
5. ⭐ **Day Shift OT after 17:00, Night Shift OT after 03:00**
6. ⭐ **Minimum OT = 0.5 hours (30 minutes)**
7. ⭐ **Max Day OT = 1.5h, Max Night OT = 3.0h**

### Data Quality Rules:
1. ✅ **Track all estimations** and show in report
2. ✅ **Never lose data** - estimate rather than skip
3. ✅ **Transparent reporting** - mark all estimated values
4. ✅ **User warnings** - alert on data quality issues
5. ✅ **Accuracy metric** - calculate % of perfect records

### Processing Rules:
1. 🔄 **Chronological order** - sort by date/time first
2. 🔄 **One-time use** - each record paired only once
3. 🔄 **First match wins** - earliest valid pair used
4. 🔄 **Midnight aware** - handle cross-day shifts
5. 🔄 **Group by employee** - process each separately

---

## Document Version
- **Version:** 1.0
- **Date:** November 5, 2025
- **Author:** System Documentation
- **Status:** Current and Complete

---

## Change Log
- **v1.0** (Nov 5, 2025): Initial comprehensive rules documentation
  - Business rules
  - Error handling rules
  - Data processing rules
  - Overtime calculation rules
  - Validation rules
  - Export rules
  - Configuration rules

---

**For Implementation Details:** See `timesheet_dashboard.py`
**For Error Handling Examples:** See `ERROR_HANDLING_GUIDE.md`
**For OT Consolidation:** See `OT_CONSOLIDATION_FEATURE.md`
