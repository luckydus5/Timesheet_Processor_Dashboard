#!/usr/bin/env python3
"""
EXACT FORMULAS FOR TIMESHEET PROCESSING
Based on your specific business rules
"""

def determine_shift_type(start_time):
    """
    FORMULA: Shift Type Determination
    
    INPUT: start_time (datetime.time object)
    
    LOGIC:
    - If start_time >= 06:00 AND start_time < 18:00 → "Day Shift"
    - If start_time >= 18:00 OR start_time < 06:00 → "Night Shift"
    
    FORMULA:
    shift_type = "Day Shift" if 6 <= start_time.hour < 18 else "Night Shift"
    """
    if 6 <= start_time.hour < 18:
        return "Day Shift"
    else:
        return "Night Shift"

def calculate_total_hours(start_time, end_time, shift_type, work_date):
    """
    FORMULA: Total Work Hours
    
    INPUT: start_time, end_time (datetime.time), shift_type (string), work_date (date)
    
    LOGIC:
    - Create full datetime objects
    - Handle cross-midnight for night shifts
    - Calculate total duration in hours
    
    FORMULA:
    total_hours = (end_datetime - start_datetime).total_seconds() / 3600
    """
    from datetime import datetime, timedelta
    
    start_dt = datetime.combine(work_date, start_time)
    end_dt = datetime.combine(work_date, end_time)
    
    # Handle cross-midnight for night shifts
    if shift_type == "Night Shift" and end_time < start_time:
        end_dt += timedelta(days=1)
    
    total_duration = end_dt - start_dt
    total_hours = total_duration.total_seconds() / 3600
    return round(total_hours, 2)

def calculate_overtime_hours(start_time, end_time, shift_type, work_date):
    """
    FORMULA: Overtime Hours Calculation
    
    INPUT: start_time, end_time (datetime.time), shift_type (string)
    
    DAY SHIFT FORMULA:
    - IF end_time > 17:00:00 THEN
    -   overtime_raw = (end_time_decimal - 17.0)
    -   IF overtime_raw < 0.5 THEN overtime = 0
    -   ELIF overtime_raw > 1.5 THEN overtime = 1.5
    -   ELSE overtime = overtime_raw
    - ELSE overtime = 0
    
    NIGHT SHIFT FORMULA:
    - IF end_time_decimal <= 12.0 AND end_time_decimal > 3.0 THEN
    -   overtime_raw = (end_time_decimal - 3.0)
    -   IF overtime_raw < 0.5 THEN overtime = 0
    -   ELIF overtime_raw > 3.0 THEN overtime = 3.0
    -   ELSE overtime = overtime_raw
    - ELSE overtime = 0
    """
    overtime = 0
    
    if shift_type == "Day Shift":
        # Convert end time to decimal hours
        end_decimal = end_time.hour + end_time.minute/60 + end_time.second/3600
        
        if end_decimal > 17.0:  # After 5:00 PM
            overtime_raw = end_decimal - 17.0
            
            # Apply day shift rules
            if overtime_raw < 0.5:      # Less than 30 minutes = no overtime
                overtime = 0
            elif overtime_raw > 1.5:    # More than 1.5 hours = cap at 1.5
                overtime = 1.5
            else:                       # Between 30 min and 1.5 hours = exact amount
                overtime = overtime_raw
                
    elif shift_type == "Night Shift":
        end_decimal = end_time.hour + end_time.minute/60 + end_time.second/3600
        
        # Only check for overtime if end time is early morning (cross-midnight)
        if end_decimal <= 12.0 and end_decimal > 3.0:  # Between 3:00 AM and 12:00 PM
            overtime_raw = end_decimal - 3.0
            
            # Apply night shift rules
            if overtime_raw < 0.5:      # Less than 30 minutes = no overtime
                overtime = 0
            elif overtime_raw > 3.0:    # More than 3 hours = cap at 3.0
                overtime = 3.0
            else:                       # Between 30 min and 3 hours = exact amount
                overtime = overtime_raw
    
    return round(overtime, 2)

def calculate_regular_hours(total_hours, overtime_hours):
    """
    FORMULA: Regular Hours
    
    INPUT: total_hours (float), overtime_hours (float)
    
    FORMULA:
    regular_hours = total_hours - overtime_hours
    regular_hours = MAX(0, regular_hours)  # Never negative
    """
    regular = total_hours - overtime_hours
    return round(max(regular, 0), 2)

def count_overtime_days(overtime_hours_list):
    """
    FORMULA: Count Overtime Days
    
    INPUT: overtime_hours_list (list of decimal hours)
    
    LOGIC:
    - Count days where overtime_hours > 0
    - This automatically follows the 30-minute minimum rule
    - Because calculate_overtime_hours() already returns 0 for < 30 minutes
    
    FORMULA:
    overtime_days = COUNT(overtime_hours WHERE overtime_hours > 0)
    """
    return len([hours for hours in overtime_hours_list if hours > 0])

def calculate_monthly_summary(person_data):
    """
    FORMULA: Monthly Overtime Summary
    
    INPUT: person_data (DataFrame for one person for one month)
    
    FORMULAS:
    total_monthly_overtime = SUM(overtime_hours_decimal)
    overtime_days_count = COUNT(days WHERE overtime_hours_decimal > 0)
    monthly_summary = f"Month Total: {HH:MM:SS_format(total_monthly_overtime)} | OT Days: {overtime_days_count}"
    """
    total_overtime = person_data['Overtime Hours (Decimal)'].sum()
    overtime_days = len(person_data[person_data['Overtime Hours (Decimal)'] > 0])
    
    # Convert to HH:MM:SS format
    hours = int(total_overtime)
    minutes = int((total_overtime - hours) * 60)
    seconds = int(((total_overtime - hours) * 60 - minutes) * 60)
    time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    return f"Month Total: {time_formatted} | OT Days: {overtime_days}"

# EXAMPLE PROCESSING WORKFLOW
def process_timesheet_data(raw_data):
    """
    COMPLETE WORKFLOW EXAMPLE
    
    INPUT: raw_data with columns [Name, Date, Time, Status]
    OUTPUT: processed_data with all calculated columns
    """
    
    # Step 1: Group by Name and Date to get daily records
    # Step 2: For each day, find first check-in and last check-out
    # Step 3: Apply formulas:
    
    processed_records = []
    
    for (name, date), day_data in raw_data.groupby(['Name', 'Date']):
        # Get times
        checkin_times = day_data[day_data['Status'] == 'Check In']['Time']
        checkout_times = day_data[day_data['Status'] == 'Check Out']['Time']
        
        if not checkin_times.empty and not checkout_times.empty:
            start_time = min(checkin_times)
            end_time = max(checkout_times)
            
            # Apply formulas
            shift_type = determine_shift_type(start_time)
            total_hours = calculate_total_hours(start_time, end_time, shift_type, date)
            overtime_hours = calculate_overtime_hours(start_time, end_time, shift_type, date)
            regular_hours = calculate_regular_hours(total_hours, overtime_hours)
            
            processed_records.append({
                'Name': name,
                'Date': date,
                'Start Time': start_time,
                'End Time': end_time,
                'Shift Time': shift_type,
                'Total Hours': total_hours,
                'Regular Hours': regular_hours,
                'Overtime Hours': overtime_hours
            })
    
    return processed_records

print("✅ EXACT FORMULAS DEFINED")
print("📋 Business Rules Implementation:")
print("   - Day Shift: 08:00-17:00, OT after 17:00, Min 30min, Max 1.5h")
print("   - Night Shift: 18:00-03:00, OT after 03:00, Min 30min, Max 3h")
print("   - Overtime Days: Count only days with OT > 0 (≥30 minutes)")