# 🌙 Night Shift Rules - Complete Guide

## Overview
Night shift employees have specific rules for work counting and overtime calculation. This guide explains how the system handles night shift detection, work hours, and overtime.

---

## 🎯 Key Rules Summary

### 1. **Night Shift Detection**
- **Detection Threshold:** Check-in ≥ **16:10 PM** (4:10 PM)
- **Purpose:** Identifies the shift as "Night Shift"
- **Note:** Employees CAN check in from 16:10 PM onwards

### 2. **Work Hour Counting**
- **Counted Period:** 18:00 PM - 03:00 AM (next day)
- **Standard Shift:** 9 hours (18:00 PM to 03:00 AM)
- **All hours between 18:00 PM and 03:00 AM are counted**

### 3. **Overtime Rules**
- **OT Starts:** After **03:00 AM** (next day) **ONLY**
- **Minimum:** Must work ≥30 minutes **after 03:00 AM** to qualify
- **Maximum:** 3.0 hours per shift
- **NO overtime before 03:00 AM**

---

## 📊 Visual Timeline

### Full Night Shift Timeline
```
     Detection Zone          Work Counted Zone              Overtime Zone
     (Check-in starts)       (18:00 PM - 03:00 AM)         (After 03:00 AM)
┌─────────────────┐    ┌──────────────────────────────┐    ┌─────────────┐
│                 │    │                              │    │             │
16:10 PM      18:00 PM                           03:00 AM              06:00 AM
   ↑            ↑                                    ↑                    ↑
   │            │                                    │                    │
   │            └── Standard work counting starts    │                    │
   │                (9 hours to 03:00 AM)            │                    │
   │                                                  │                    │
   └── Night shift detection                         └─── OT starts ───→ Max 3h
       (can check in from here)                           (After 03:00 only)
```

### Overtime Qualification Zone
```
03:00 AM                 03:30 AM                    06:00 AM
   │                        │                           │
   ├────────────────────────┼───────────────────────────┤
   │   NO OVERTIME ZONE     │    OVERTIME ZONE          │
   │   (0-29 minutes)       │    (30 min - 3.0 hours)   │
   │   ❌ Below minimum     │    ✅ Qualifies for OT    │
   └────────────────────────┴───────────────────────────┘
```

---

## ✅ Examples: When Overtime is EARNED

### Example 1: Minimum Overtime (30 minutes)
```
Check-In:  18:00 PM
Check-Out: 03:30 AM (next day)

Work Duration: 9.5 hours
Regular Hours: 9.0 hours (18:00 PM - 03:00 AM)
OT Calculation: 03:30 - 03:00 = 0.5 hours (30 minutes)
OT Earned: 0.5 hours ✅
```

### Example 2: 1 Hour Overtime
```
Check-In:  18:00 PM
Check-Out: 04:00 AM (next day)

Work Duration: 10.0 hours
Regular Hours: 9.0 hours
OT Calculation: 04:00 - 03:00 = 1.0 hour
OT Earned: 1.0 hours ✅
```

### Example 3: Maximum Overtime (3 hours)
```
Check-In:  18:00 PM
Check-Out: 06:00 AM (next day)

Work Duration: 12.0 hours
Regular Hours: 9.0 hours
OT Calculation: 06:00 - 03:00 = 3.0 hours
OT Earned: 3.0 hours ✅ (Maximum reached)
```

### Example 4: Beyond Maximum (Capped)
```
Check-In:  18:00 PM
Check-Out: 07:00 AM (next day)

Work Duration: 13.0 hours
Regular Hours: 9.0 hours
OT Calculation: 07:00 - 03:00 = 4.0 hours
OT Earned: 3.0 hours ✅ (Capped at maximum)
```

### Example 5: Early Check-In (16:30) with OT
```
Check-In:  16:30 PM (Early arrival, detected as night shift)
Check-Out: 03:45 AM (next day)

Shift Type: Night Shift (check-in ≥ 16:10)
Work Duration: 11.25 hours
Work Counted: From 18:00 PM to 03:45 AM = 9.75 hours
OT Calculation: 03:45 - 03:00 = 0.75 hours
OT Earned: 0.75 hours ✅

Note: Check-in at 16:30 identifies as night shift, but work 
      counting starts at 18:00 PM. Hours before 18:00 may be 
      counted in total but don't affect OT calculation.
```

---

## ❌ Examples: When Overtime is NOT EARNED

### Example 6: Finish Exactly at 03:00 AM
```
Check-In:  18:00 PM
Check-Out: 03:00 AM (next day)

Work Duration: 9.0 hours
OT Calculation: 03:00 - 03:00 = 0 hours
OT Earned: 0 hours ❌ (Must work AFTER 03:00)
```

### Example 7: Below 30-Minute Minimum (25 minutes)
```
Check-In:  18:00 PM
Check-Out: 03:25 AM (next day)

Work Duration: 9.42 hours
OT Calculation: 03:25 - 03:00 = 0.42 hours (25 minutes)
OT Earned: 0 hours ❌ (Below 30-minute minimum)
```

### Example 8: Below 30-Minute Minimum (29 minutes)
```
Check-In:  18:00 PM
Check-Out: 03:29 AM (next day)

Work Duration: 9.48 hours
OT Calculation: 03:29 - 03:00 = 0.48 hours (29 minutes)
OT Earned: 0 hours ❌ (Below 30-minute minimum)
```

### Example 9: Finish Before 03:00 AM (No OT)
```
Check-In:  18:00 PM
Check-Out: 02:00 AM (next day)

Work Duration: 8.0 hours
OT Calculation: Not applicable (finished before 03:00)
OT Earned: 0 hours ❌ (No overtime before 03:00 AM)
```

---

## 📈 Overtime Earning Chart

```
End Time    │ Minutes After 03:00 │ OT Earned │ Status
────────────┼─────────────────────┼───────────┼──────────────────
02:00 AM    │ -60 (before)        │ 0.0 h     │ ❌ No OT
03:00 AM    │ 0                   │ 0.0 h     │ ❌ No OT
03:15 AM    │ 15                  │ 0.0 h     │ ❌ Below min
03:29 AM    │ 29                  │ 0.0 h     │ ❌ Below min
03:30 AM    │ 30                  │ 0.5 h     │ ✅ Minimum met
03:45 AM    │ 45                  │ 0.75 h    │ ✅ OT earned
04:00 AM    │ 60                  │ 1.0 h     │ ✅ OT earned
04:30 AM    │ 90                  │ 1.5 h     │ ✅ OT earned
05:00 AM    │ 120                 │ 2.0 h     │ ✅ OT earned
05:30 AM    │ 150                 │ 2.5 h     │ ✅ OT earned
06:00 AM    │ 180                 │ 3.0 h     │ ✅ Max reached
06:30 AM    │ 210                 │ 3.0 h     │ ✅ Capped at max
07:00 AM    │ 240                 │ 3.0 h     │ ✅ Capped at max
```

---

## 🎯 Quick Reference

### The 30-Minute Rule
```
┌──────────────────────────────────────────────┐
│  To earn ANY overtime on night shift:        │
│                                               │
│  ✅ Must finish work AFTER 03:00 AM          │
│  ✅ Must work AT LEAST 30 minutes after      │
│                                               │
│  03:00 to 03:29 = NO OVERTIME ❌             │
│  03:00 to 03:30 = 0.5h OVERTIME ✅           │
└──────────────────────────────────────────────┘
```

### Night Shift Detection vs Work Counting
```
┌─────────────────────────────────────────────┐
│  Detection (16:10 PM):                      │
│  - Identifies shift as "Night Shift"        │
│  - Employees can check in from 16:10        │
│                                              │
│  Work Counting (18:00 PM):                  │
│  - Standard work counted from 18:00         │
│  - 9 hours: 18:00 PM → 03:00 AM            │
│                                              │
│  Overtime (After 03:00 AM):                 │
│  - ONLY counted after 03:00 AM              │
│  - Maximum 3 hours                          │
└─────────────────────────────────────────────┘
```

---

## 💡 Important Notes

### Why Check-in at 16:10 but Count from 18:00?
- **16:10 PM:** Threshold to **identify** the shift as "Night Shift"
- **18:00 PM:** Standard **work start time** for night shift
- Employees may arrive early (16:10-17:59) for preparation, handover, etc.
- This prevents day shift employees (who finish at 17:00) from being counted as night shift

### Why the 30-Minute Minimum?
- Prevents overtime for very short periods after 03:00 AM
- Ensures meaningful overtime work
- Standard industry practice
- Reduces administrative overhead

### Why the 3-Hour Maximum?
- Controls overnight costs
- Prevents excessive night hours
- Encourages proper shift handover
- Aligns with business policies

---

## 📊 Payroll Examples

### Scenario 1: Normal Night Shift + Small OT
```
Employee: John Doe
Check-In: 18:00 PM
Check-Out: 03:45 AM

Regular Hours: 9.0 hours (18:00 PM - 03:00 AM)
Overtime: 0.75 hours (03:00 - 03:45)
Total Hours: 9.75 hours

Payroll:
- Regular Pay: 9 hours × $20/hr = $180
- OT Pay (1.5x): 0.75 hours × $30/hr = $22.50
- Total: $202.50
```

### Scenario 2: Normal Night Shift + Maximum OT
```
Employee: Jane Smith
Check-In: 18:00 PM
Check-Out: 06:00 AM

Regular Hours: 9.0 hours
Overtime: 3.0 hours (03:00 - 06:00, capped)
Total Hours: 12.0 hours

Payroll:
- Regular Pay: 9 hours × $20/hr = $180
- OT Pay (1.5x): 3.0 hours × $30/hr = $90
- Total: $270
```

### Scenario 3: Below Minimum (No OT)
```
Employee: Bob Wilson
Check-In: 18:00 PM
Check-Out: 03:25 AM

Regular Hours: 9.0 hours
Overtime: 0 hours (25 min is below 30 min minimum)
Total Hours: 9.42 hours

Payroll:
- Regular Pay: 9.42 hours × $20/hr = $188.40
- OT Pay: $0 (below minimum)
- Total: $188.40
```

---

## 🔍 How System Detects This

### Detection Code Logic
```python
# From timesheet_dashboard.py

# 1. Detect night shift (check-in >= 16:10)
checkin_hour = checkin_time.hour + checkin_time.minute / 60
is_night_shift = checkin_hour >= 16.1667  # 16:10

# 2. For night shift, check overtime after 03:00 AM
if shift_type == "Night Shift":
    if end_time <= 12:00:  # Early morning (crossed midnight)
        if end_time > 03:00:  # After 3 AM
            overtime = end_time - 03:00
            
            # Apply rules
            if overtime < 0.5:  # Less than 30 minutes
                overtime = 0
            elif overtime > 3.0:  # More than 3 hours
                overtime = 3.0
```

---

## ✅ Summary

### Night Shift Rules (Quick Checklist)
- [ ] Check-in must be **≥ 16:10 PM** (for detection)
- [ ] Standard work counted: **18:00 PM - 03:00 AM** (9 hours)
- [ ] Employee must finish **after 03:00 AM** for OT
- [ ] Employee must work **≥30 minutes after 03:00 AM** for OT
- [ ] Maximum OT is **3.0 hours** per shift
- [ ] OT is calculated from **03:00 AM**, not from start time

### When OT is Earned:
✅ End time ≥ 03:30 and ≤ 06:00 → Full OT calculation
✅ End time > 06:00 → OT capped at 3.0 hours

### When OT is NOT Earned:
❌ End time ≤ 03:00 → No overtime
❌ End time between 03:01 and 03:29 → Below minimum, no overtime

---

**Document Version:** 1.0  
**Last Updated:** November 5, 2025  
**Author:** Timesheet Consolidator System
