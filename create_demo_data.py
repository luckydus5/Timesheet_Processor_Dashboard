#!/usr/bin/env python3
"""
🧪 Dashboard Demo Script
Quick test to verify dashboard functionality
"""

import pandas as pd
from datetime import datetime, timedelta
import random

def create_sample_data():
    """Create sample timesheet data for testing"""
    
    # Sample employees
    employees = [
        "John Smith", "Mary Johnson", "David Brown", "Sarah Wilson", 
        "Michael Davis", "Lisa Anderson", "Robert Taylor", "Jennifer White"
    ]
    
    # Generate test data
    data = []
    start_date = datetime(2025, 10, 1)
    
    for day in range(10):  # 10 days of data
        current_date = start_date + timedelta(days=day)
        date_str = current_date.strftime('%d/%m/%Y')
        
        for employee in employees:
            # Create multiple entries per employee per day (realistic duplicate scenario)
            entries_count = random.randint(2, 4)
            
            # Generate realistic check-in/out times
            check_in_time = datetime.combine(current_date, datetime.min.time()) + timedelta(
                hours=random.randint(6, 8), 
                minutes=random.randint(0, 59)
            )
            
            check_out_time = check_in_time + timedelta(
                hours=random.randint(8, 10),
                minutes=random.randint(0, 59)
            )
            
            # Add some overtime
            if random.random() > 0.7:  # 30% chance of overtime
                overtime_out = check_out_time + timedelta(
                    hours=random.randint(1, 2),
                    minutes=random.randint(0, 59)
                )
            else:
                overtime_out = None
            
            # Create entries (simulating multiple check-ins/outs)
            times_and_statuses = [
                (check_in_time, "C/In"),
                (check_out_time, "C/Out")
            ]
            
            if overtime_out:
                times_and_statuses.append((overtime_out, "OverTime Out"))
            
            # Add some duplicate entries to simulate real problems
            if entries_count > 2:
                # Add extra check-in
                extra_checkin = check_in_time + timedelta(minutes=random.randint(5, 30))
                times_and_statuses.append((extra_checkin, "C/In"))
            
            if entries_count > 3:
                # Add overtime in
                if overtime_out:
                    ot_in = check_out_time + timedelta(minutes=random.randint(5, 15))
                    times_and_statuses.append((ot_in, "OverTime In"))
            
            # Create records
            for time_dt, status in times_and_statuses:
                data.append({
                    'Name': employee,
                    'Date': date_str,
                    'Time': time_dt.strftime('%H:%M:%S'),
                    'Status': status,
                    'Department': 'Operations' if random.random() > 0.5 else 'Administration'
                })
    
    return pd.DataFrame(data)

def save_sample_data():
    """Save sample data files"""
    df = create_sample_data()
    
    # Save as CSV
    csv_filename = "sample_timesheet_data.csv"
    df.to_csv(csv_filename, index=False)
    print(f"✅ Sample CSV created: {csv_filename}")
    
    # Save as Excel
    excel_filename = "sample_timesheet_data.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"✅ Sample Excel created: {excel_filename}")
    
    # Show sample
    print(f"\n📊 Sample Data Preview:")
    print(f"   Records: {len(df)}")
    print(f"   Employees: {df['Name'].nunique()}")
    print(f"   Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    print(f"\n📋 First 10 records:")
    print(df[['Name', 'Date', 'Time', 'Status']].head(10).to_string(index=False))
    
    # Analyze duplicates
    duplicates = df.groupby(['Name', 'Date']).size().reset_index(name='Entries')
    multi_entries = duplicates[duplicates['Entries'] > 1]
    
    print(f"\n🔍 Duplicate Analysis:")
    print(f"   Employee-date combinations: {len(duplicates)}")
    print(f"   With multiple entries: {len(multi_entries)} ({len(multi_entries)/len(duplicates)*100:.1f}%)")
    
    return csv_filename, excel_filename

if __name__ == "__main__":
    print("🧪 Creating sample timesheet data for dashboard testing...")
    print("=" * 60)
    
    csv_file, excel_file = save_sample_data()
    
    print(f"\n🎯 Test Instructions:")
    print(f"1. Open the dashboard: http://localhost:8501")
    print(f"2. Upload either '{csv_file}' or '{excel_file}'")
    print(f"3. Click 'Start Consolidation Process'")
    print(f"4. Explore the analytics tabs")
    print(f"5. Download the processed results")
    
    print(f"\n✅ Demo data ready!")