"""
Test script to demonstrate shift detection in both systems
"""
import pandas as pd
from datetime import time
from overtime_consolidator import calculate_overtime_15_rate

print("="*80)
print("SHIFT DETECTION COMPARISON - Main Dashboard vs OT Consolidation")
print("="*80)
print()

# Test cases
test_cases = [
    ('06:00', '18:30', 'Early day shift, late end'),
    ('06:45', '17:10', 'Day shift, short OT (<30min)'),
    ('14:00', '19:00', 'Afternoon start, 2h past 17:00'),
    ('16:19', '02:00', 'Just before 16:20 threshold'),
    ('16:20', '07:50', 'Exactly at 16:20, crosses midnight'),
    ('16:23', '07:50', 'After 16:20, crosses midnight'),
    ('16:30', '22:00', 'After 16:20, NO midnight cross'),
    ('18:00', '22:00', 'Evening start, same day'),
    ('20:00', '06:00', 'Late night, crosses midnight'),
]

print(f"{'Description':<35} | {'Start':<8} | {'End':<8} | {'Main Dash':<12} | {'OT System':<12} | {'OT Hours'}")
print("-" * 105)

for start_str, end_str, desc in test_cases:
    # Parse times
    start_time = pd.to_datetime(start_str, format='%H:%M').time()
    end_time = pd.to_datetime(end_str, format='%H:%M').time()
    
    # Main Dashboard logic (threshold 18:00)
    start_hour = start_time.hour + start_time.minute / 60
    main_dash_shift = "Day Shift" if start_hour < 18.0 else "Night Shift"
    
    # OT Consolidation logic (threshold 16:20)
    if start_time < time(16, 20):
        ot_system_shift = "Day Logic"
    elif start_time >= time(16, 20) and end_time < start_time:
        ot_system_shift = "Night Logic"
    else:
        ot_system_shift = "No OT"
    
    # Calculate OT using formula
    ot_hours = calculate_overtime_15_rate(start_time, end_time)
    
    print(f"{desc:<35} | {start_str:<8} | {end_str:<8} | {main_dash_shift:<12} | {ot_system_shift:<12} | {ot_hours:.1f}h")

print()
print("="*80)
print("KEY DIFFERENCES:")
print("="*80)
print()
print("MAIN DASHBOARD:")
print("  - Threshold: 18:00 (6:00 PM)")
print("  - Day Shift: Start < 18:00")
print("  - Night Shift: Start >= 18:00")
print("  - Purpose: General attendance tracking")
print()
print("OT CONSOLIDATION (Excel Formula):")
print("  - Threshold: 16:20 (4:20 PM)")
print("  - Day Logic: Start < 16:20 → Max 1.5h OT after 17:00")
print("  - Night Logic: Start >= 16:20 AND crosses midnight → Fixed 3h OT")
print("  - No OT: Start >= 16:20 but NO midnight cross")
print("  - Purpose: Payroll calculation matching Excel")
print()
print("="*80)
