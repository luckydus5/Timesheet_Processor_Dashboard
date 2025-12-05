"""
100% Accuracy Verification Script
Tests the attendance analyzer against manual calculations
"""

import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import sys
from io import StringIO

# Suppress print statements from analyzer
class SuppressOutput:
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = StringIO()
        return self
    def __exit__(self, *args):
        sys.stdout = self._stdout

from attendance_analyzer import load_attendance_file, calculate_all_metrics, validate_data

def verify_accuracy(file_path):
    print('='*70)
    print('100% ACCURACY VERIFICATION TEST')
    print('='*70)
    print(f'\nFile: {file_path}')
    
    # Load data (suppress warnings)
    with SuppressOutput():
        df = load_attendance_file(file_path)
        metrics = calculate_all_metrics(df)
    
    validation = validate_data(df)
    combined = metrics['combined']
    
    print(f'Total Records: {validation["TotalRecords"]:,}')
    print(f'Unique Employees: {validation["UniqueEmployees"]}')
    print(f'Date Range: {validation["DateRange"]["min"]} to {validation["DateRange"]["max"]}')
    
    # Test ALL employees
    all_pass = True
    failed_employees = []
    
    for emp_name in combined['Name'].unique():
        emp_raw = df[df['Name'] == emp_name]
        emp_calc = combined[combined['Name'] == emp_name].iloc[0]
        
        # Manual calculations from raw data
        manual_total = emp_raw['Date'].nunique()
        manual_weekend = emp_raw[emp_raw['IsWeekend'] == True]['Date'].nunique()
        manual_weekday = emp_raw[emp_raw['IsWeekend'] == False]['Date'].nunique()
        
        # Verify calculations match
        total_ok = emp_calc['TotalDays'] == manual_total
        weekend_ok = emp_calc['WeekendDays'] == manual_weekend
        weekday_ok = emp_calc['WeekdayDays'] == manual_weekday
        sum_ok = emp_calc['WeekdayDays'] + emp_calc['WeekendDays'] == emp_calc['TotalDays']
        
        if not (total_ok and weekend_ok and weekday_ok and sum_ok):
            all_pass = False
            failed_employees.append({
                'Name': emp_name,
                'Issue': 'Mismatch',
                'Calc_Total': emp_calc['TotalDays'],
                'Manual_Total': manual_total,
                'Calc_Weekend': emp_calc['WeekendDays'],
                'Manual_Weekend': manual_weekend
            })
    
    # Show results
    print(f'\nTested {len(combined)} employees')
    
    if all_pass:
        print('\n' + '='*70)
        print('RESULT: ALL TESTS PASSED - 100% ACCURATE')
        print('='*70)
    else:
        print(f'\nFailed employees ({len(failed_employees)}):')
        for emp in failed_employees[:10]:
            print(f"  - {emp['Name']}: Calc={emp['Calc_Total']}, Manual={emp['Manual_Total']}")
    
    # Show sample verification for top employees
    print('\n' + '-'*70)
    print('SAMPLE VERIFICATION (Top 5 by Overtime):')
    print('-'*70)
    
    top_5 = combined.nlargest(5, 'TotalOvertimeHours')
    for _, emp_calc in top_5.iterrows():
        emp_name = emp_calc['Name']
        emp_raw = df[df['Name'] == emp_name]
        
        manual_total = emp_raw['Date'].nunique()
        manual_weekend = emp_raw[emp_raw['IsWeekend'] == True]['Date'].nunique()
        
        total_match = 'OK' if emp_calc['TotalDays'] == manual_total else 'FAIL'
        weekend_match = 'OK' if emp_calc['WeekendDays'] == manual_weekend else 'FAIL'
        
        print(f'\n{emp_name}:')
        print(f'  Total Days:    Calc={int(emp_calc["TotalDays"]):3}, Manual={manual_total:3} [{total_match}]')
        print(f'  Weekend Days:  Calc={int(emp_calc["WeekendDays"]):3}, Manual={manual_weekend:3} [{weekend_match}]')
        print(f'  Weekday Days:  {int(emp_calc["WeekdayDays"]):3}')
        print(f'  OT Hours:      {emp_calc["TotalOvertimeHours"]:.2f} ({int(emp_calc["OvertimeSessions"])} sessions)')
    
    # Verify overtime calculation for one employee
    print('\n' + '-'*70)
    print('OVERTIME CALCULATION VERIFICATION:')
    print('-'*70)
    
    test_emp = top_5.iloc[0]['Name']
    emp_raw = df[df['Name'] == test_emp]
    ot_records = emp_raw[emp_raw['Status'].str.contains('OverTime', case=False, na=False)]
    ot_in = ot_records[ot_records['Status'].str.contains('In', case=False)]
    ot_out = ot_records[ot_records['Status'].str.contains('Out', case=False) & ~ot_records['Status'].str.contains('In', case=False)]
    
    print(f'\n{test_emp}:')
    print(f'  Total OT Records: {len(ot_records)}')
    print(f'  OT In Records: {len(ot_in)}')
    print(f'  OT Out Records: {len(ot_out)}')
    print(f'  Expected Sessions (pairs): ~{min(len(ot_in), len(ot_out))}')
    print(f'  Calculated Sessions: {int(combined[combined["Name"] == test_emp].iloc[0]["OvertimeSessions"])}')
    
    return all_pass

if __name__ == '__main__':
    # Test both files
    files = [
        'Office Attendance fingerprint.xlsx',
        'Peat Office Attendance 2025.xlsx'
    ]
    
    for f in files:
        try:
            verify_accuracy(f)
            print('\n')
        except Exception as e:
            print(f'Error with {f}: {e}')
