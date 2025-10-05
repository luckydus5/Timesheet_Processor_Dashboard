#!/usr/bin/env python3
"""
🏆 Ultimate Demo Data Creator - Premium Edition
Creates realistic timesheet data to showcase the premium system
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_premium_demo_data():
    """Create premium demo data with realistic scenarios"""
    
    # Premium employee list with realistic names
    employees = [
        "Alexandra Johnson", "Benjamin Martinez", "Catherine Williams", "Daniel Thompson",
        "Elena Rodriguez", "Frederick Davis", "Gabriella Wilson", "Harrison Brown",
        "Isabella Garcia", "Jonathan Miller", "Katherine Anderson", "Leonardo Silva",
        "Maximilian Taylor", "Natalia Petrov", "Oliver Chen", "Patricia Moore",
        "Quinton Jackson", "Rebecca Lee", "Sebastian Kumar", "Victoria Chang"
    ]
    
    # Generate 30 days of premium test data
    data = []
    start_date = datetime(2025, 9, 1)
    
    for day in range(30):  # 30 days of comprehensive data
        current_date = start_date + timedelta(days=day)
        date_str = current_date.strftime('%d/%m/%Y')
        
        # Skip some weekends randomly
        if current_date.weekday() >= 5 and random.random() > 0.3:
            continue
            
        for employee in employees:
            # Skip some employees some days (realistic absences)
            if random.random() > 0.85:
                continue
                
            # Determine shift type (80% day shift, 20% night shift)
            is_night_shift = random.random() > 0.8
            
            if is_night_shift:
                # Night shift: 18:00 to 03:00 (+1 day)
                base_start = 18 + random.randint(-2, 1)  # 16:00-19:00 start
                start_hour = max(16, min(22, base_start))
                start_minute = random.randint(0, 59)
                
                # Work 8-9 hours
                work_duration = 8 + random.random() * 1
                end_time = (start_hour + work_duration) % 24
                end_hour = int(end_time)
                end_minute = int((end_time % 1) * 60)
                
                # Handle next day for night shift
                if end_hour < 12:  # Early morning next day
                    end_date = current_date + timedelta(days=1)
                else:
                    end_date = current_date
                    
            else:
                # Day shift: 08:00 to 17:00
                base_start = 8 + random.randint(-2, 2)  # 06:00-10:00 start
                start_hour = max(6, min(10, base_start))
                start_minute = random.randint(0, 59)
                
                # Work 8-9 hours
                work_duration = 8 + random.random() * 1
                end_time = start_hour + work_duration
                end_hour = int(end_time)
                end_minute = int((end_time % 1) * 60)
                end_date = current_date
            
            # Create realistic check-in times
            check_in_time = current_date.replace(hour=start_hour, minute=start_minute, second=random.randint(0, 59))
            check_out_time = end_date.replace(hour=end_hour, minute=end_minute, second=random.randint(0, 59))
            
            # Create multiple entries per employee per day (realistic scenario)
            entries = []
            
            # Primary check-in
            entries.append((check_in_time, "C/In"))
            
            # Sometimes multiple check-ins (employee forgets to check in, double-taps, etc.)
            if random.random() > 0.7:  # 30% chance
                extra_checkin = check_in_time + timedelta(minutes=random.randint(1, 15))
                entries.append((extra_checkin, "C/In"))
            
            # Primary check-out
            entries.append((check_out_time, "C/Out"))
            
            # Overtime scenarios
            overtime_chance = 0.4 if not is_night_shift else 0.3
            if random.random() < overtime_chance:
                # Overtime starts after regular check-out
                ot_start = check_out_time + timedelta(minutes=random.randint(5, 20))
                ot_duration = random.randint(30, 120)  # 30 minutes to 2 hours
                ot_end = ot_start + timedelta(minutes=ot_duration)
                
                entries.append((ot_start, "OverTime In"))
                entries.append((ot_end, "OverTime Out"))
                
                # Sometimes multiple overtime entries
                if random.random() > 0.8:
                    extra_ot_out = ot_end + timedelta(minutes=random.randint(1, 10))
                    entries.append((extra_ot_out, "OverTime Out"))
            
            # Add lunch break scenarios (check out for lunch, check back in)
            if random.random() > 0.6 and not is_night_shift:  # 40% chance for day shift
                lunch_start = check_in_time + timedelta(hours=4, minutes=random.randint(0, 60))
                lunch_end = lunch_start + timedelta(minutes=random.randint(30, 60))
                
                # Only add if lunch is before main check-out
                if lunch_end < check_out_time:
                    entries.append((lunch_start, "C/Out"))
                    entries.append((lunch_end, "C/In"))
            
            # Convert to records
            for time_entry, status in entries:
                data.append({
                    'Department': random.choice(['Operations', 'Administration', 'Security', 'Maintenance', 'Customer Service']),
                    'Name': employee,
                    'Employee_ID': f"EMP{hash(employee) % 10000:04d}",
                    'Date/Time': time_entry.strftime('%d/%m/%Y %H:%M:%S'),
                    'Status': status,
                    'Location': random.choice(['Main Office', 'Warehouse', 'Branch A', 'Branch B', 'Remote']),
                    'Badge_Number': f"B{random.randint(1000, 9999)}",
                    'Supervisor': random.choice(['Manager A', 'Manager B', 'Manager C', 'Manager D']),
                    'Cost_Center': f"CC{random.randint(100, 999)}",
                    'Project_Code': random.choice(['PROJ001', 'PROJ002', 'PROJ003', 'MAINT', 'ADMIN'])
                })
    
    return pd.DataFrame(data)

def save_premium_demo_data():
    """Save premium demo data in multiple formats"""
    df = create_premium_demo_data()
    
    # Sort by date/time to make it realistic
    df['DateTime_Sort'] = pd.to_datetime(df['Date/Time'], format='%d/%m/%Y %H:%M:%S')
    df = df.sort_values(['Name', 'DateTime_Sort']).drop('DateTime_Sort', axis=1)
    
    # Reset index to ensure continuous numbering
    df = df.reset_index(drop=True)
    
    # Save as Excel (primary format)
    excel_filename = "premium_demo_timesheet.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"✅ Premium Excel demo created: {excel_filename}")
    
    # Save as CSV (backup format)
    csv_filename = "premium_demo_timesheet.csv"
    df.to_csv(csv_filename, index=False)
    print(f"✅ Premium CSV demo created: {csv_filename}")
    
    # Create a smaller sample for quick testing
    sample_df = df.head(100)
    sample_filename = "premium_demo_sample.xlsx"
    sample_df.to_excel(sample_filename, index=False)
    print(f"✅ Premium sample created: {sample_filename}")
    
    # Analysis and preview
    print(f"\n📊 Premium Demo Data Analysis:")
    print(f"   Total Records: {len(df):,}")
    print(f"   Unique Employees: {df['Name'].nunique()}")
    print(f"   Date Range: {len(df['Date/Time'].str[:10].unique())} unique dates")
    print(f"   Departments: {', '.join(df['Department'].unique())}")
    
    # Analyze entry patterns
    df['Date_Only'] = df['Date/Time'].str[:10]
    entry_patterns = df.groupby(['Name', 'Date_Only']).size()
    
    print(f"\n🔍 Entry Pattern Analysis:")
    print(f"   Employee-date combinations: {len(entry_patterns)}")
    print(f"   Multiple entries per day: {len(entry_patterns[entry_patterns > 1])} ({len(entry_patterns[entry_patterns > 1])/len(entry_patterns)*100:.1f}%)")
    print(f"   Max entries per employee per day: {entry_patterns.max()}")
    print(f"   Average entries per employee per day: {entry_patterns.mean():.1f}")
    
    # Status distribution
    status_dist = df['Status'].value_counts()
    print(f"\n📋 Status Distribution:")
    for status, count in status_dist.items():
        print(f"   {status}: {count:,} ({count/len(df)*100:.1f}%)")
    
    # Sample preview
    print(f"\n📋 Sample Records (First 10):")
    preview_cols = ['Name', 'Date/Time', 'Status', 'Department']
    print(df[preview_cols].head(10).to_string(index=False))
    
    return excel_filename, csv_filename, sample_filename

if __name__ == "__main__":
    print("🏆 Creating Premium Demo Data for Ultimate Timesheet Processor")
    print("=" * 70)
    
    excel_file, csv_file, sample_file = save_premium_demo_data()
    
    print(f"\n🎯 Premium Demo Files Ready:")
    print(f"   📊 Full Dataset: {excel_file} (comprehensive demo)")
    print(f"   📄 CSV Version: {csv_file} (alternative format)")
    print(f"   🧪 Quick Sample: {sample_file} (fast testing)")
    
    print(f"\n🚀 Next Steps:")
    print(f"   1. Launch Ultimate System: ./launch_ultimate.sh")
    print(f"   2. Open: http://localhost:8502")
    print(f"   3. Upload: {excel_file}")
    print(f"   4. Click: 'ENHANCE WITH PREMIUM CALCULATIONS'")
    print(f"   5. Explore: Premium analytics and export enhanced Excel")
    
    print(f"\n✨ This demo showcases:")
    print(f"   🔒 Original structure preservation (NO sorting)")
    print(f"   ➕ Enhanced calculations added")
    print(f"   🎨 Premium visual interface")
    print(f"   📊 Professional Excel formatting")
    print(f"   📈 Advanced analytics")
    
    print(f"\n🏆 Premium demo data ready for ultimate processing!")