#!/usr/bin/env python3
"""
Detailed analysis of Datas.xlsx for night shift and pairing issues
"""

import pandas as pd
from datetime import datetime, time

# Load the file
df = pd.read_excel("Datas.xlsx")

print("=" * 100)
print("DETAILED ANALYSIS OF DATAS.XLSX")
print("=" * 100)

# Parse date and time from Date/Time column
df[['Date', 'Time']] = df['Date/Time'].astype(str).str.split(' ', n=1, expand=True)
df['Date_parsed'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
df['Time_parsed'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time

print(f"\n📊 Total records: {len(df)}")
print(f"📊 Total check-ins: {len(df[df['Status'] == 'C/In'])}")
print(f"📊 Total check-outs: {len(df[df['Status'] == 'C/Out'])}")
print(f"📊 Difference: {len(df[df['Status'] == 'C/In']) - len(df[df['Status'] == 'C/Out'])} (should be close to 0)")

# Check for morning checkouts
print("\n" + "=" * 100)
print("MORNING CHECKOUTS (before 12:00 PM) - Potential night shift endings:")
print("=" * 100)

morning_checkouts = df[
    (df['Status'] == 'C/Out') & 
    (df['Time_parsed'].notna()) &
    (df['Time_parsed'].apply(lambda x: x.hour < 12))
]

if len(morning_checkouts) > 0:
    print(f"\n⚠️  Found {len(morning_checkouts)} morning checkouts")
    print("\nSample records:")
    for idx, row in morning_checkouts.head(10).iterrows():
        print(f"  {row['Name']:30s} | {row['Date']:12s} | {row['Time']:10s} | {row['Status']}")
else:
    print("✅ No morning checkouts found")

# Check for night shift check-ins
print("\n" + "=" * 100)
print("NIGHT SHIFT CHECK-INS (after 16:10):")
print("=" * 100)

night_checkins = df[
    (df['Status'] == 'C/In') & 
    (df['Time_parsed'].notna()) &
    (df['Time_parsed'].apply(lambda x: (x.hour + x.minute/60) >= 16.1667))
]

if len(night_checkins) > 0:
    print(f"\n🌙 Found {len(night_checkins)} night shift check-ins")
    print("\nSample records:")
    for idx, row in night_checkins.head(10).iterrows():
        print(f"  {row['Name']:30s} | {row['Date']:12s} | {row['Time']:10s} | {row['Status']}")
else:
    print("✅ No night shift check-ins found")

# Analyze pairing by employee
print("\n" + "=" * 100)
print("EMPLOYEE-LEVEL PAIRING ANALYSIS:")
print("=" * 100)

for employee in df['Name'].unique()[:5]:  # Check first 5 employees
    emp_data = df[df['Name'] == employee].sort_values('Date_parsed')
    
    print(f"\n📋 {employee}")
    print(f"   Total records: {len(emp_data)}")
    print(f"   Check-ins: {len(emp_data[emp_data['Status'] == 'C/In'])}")
    print(f"   Check-outs: {len(emp_data[emp_data['Status'] == 'C/Out'])}")
    
    # Show all records
    print("\n   All records:")
    for idx, row in emp_data.iterrows():
        date_str = row['Date_parsed'].strftime('%d/%m/%Y') if pd.notna(row['Date_parsed']) else 'N/A'
        time_obj = row['Time_parsed']
        time_str = f"{time_obj.hour:02d}:{time_obj.minute:02d}:{time_obj.second:02d}" if time_obj else 'N/A'
        print(f"     {date_str} {time_str:10s} | {row['Status']:6s}")
    
    # Check for potential issues
    issues = []
    
    # Check for dates with multiple check-ins or check-outs
    daily_groups = emp_data.groupby('Date_parsed')
    for date, group in daily_groups:
        checkins = len(group[group['Status'] == 'C/In'])
        checkouts = len(group[group['Status'] == 'C/Out'])
        
        if checkins > 1:
            issues.append(f"Multiple check-ins ({checkins}) on {date.strftime('%d/%m/%Y')}")
        if checkouts > 1:
            issues.append(f"Multiple check-outs ({checkouts}) on {date.strftime('%d/%m/%Y')}")
    
    # Check for unpaired check-ins/outs
    total_ins = len(emp_data[emp_data['Status'] == 'C/In'])
    total_outs = len(emp_data[emp_data['Status'] == 'C/Out'])
    if total_ins != total_outs:
        issues.append(f"Unmatched count: {total_ins} check-ins vs {total_outs} check-outs")
    
    if issues:
        print("\n   ⚠️  Potential issues:")
        for issue in issues:
            print(f"     - {issue}")
    else:
        print("\n   ✅ No issues detected")

print("\n" + "=" * 100)
print("SUMMARY:")
print("=" * 100)
print(f"✅ Total records: {len(df)}")
print(f"✅ Employees: {df['Name'].nunique()}")
print(f"✅ Date range: {df['Date_parsed'].min().strftime('%d/%m/%Y')} to {df['Date_parsed'].max().strftime('%d/%m/%Y')}")
print(f"✅ Check-ins: {len(df[df['Status'] == 'C/In'])}")
print(f"✅ Check-outs: {len(df[df['Status'] == 'C/Out'])}")
print(f"✅ Morning checkouts: {len(morning_checkouts)}")
print(f"✅ Night shift check-ins: {len(night_checkins)}")

print("\n💡 NEXT STEP: Upload this file to the Streamlit dashboard to process it!")
print("=" * 100)
