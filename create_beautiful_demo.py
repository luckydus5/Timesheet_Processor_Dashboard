"""
🎨 Beautiful Demo Data Creator
============================
Creates stunning demo data for the Beautiful Timesheet Dashboard
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def create_beautiful_demo_data():
    """Create comprehensive demo data for beautiful dashboard testing"""
    
    # Beautiful employee data with diverse backgrounds
    employees = [
        {'id': 'EMP001', 'name': 'Alexandra Chen', 'dept': 'Creative Design', 'role': 'Senior Designer'},
        {'id': 'EMP002', 'name': 'Marcus Johnson', 'dept': 'Operations', 'role': 'Team Lead'},
        {'id': 'EMP003', 'name': 'Sofia Rodriguez', 'dept': 'Analytics', 'role': 'Data Scientist'},
        {'id': 'EMP004', 'name': 'Kai Nakamura', 'dept': 'Engineering', 'role': 'Frontend Developer'},
        {'id': 'EMP005', 'name': 'Emma Thompson', 'dept': 'Marketing', 'role': 'Content Strategist'},
        {'id': 'EMP006', 'name': 'David Kim', 'dept': 'Security', 'role': 'Cybersecurity Analyst'},
        {'id': 'EMP007', 'name': 'Isabella Silva', 'dept': 'HR', 'role': 'People Operations'},
        {'id': 'EMP008', 'name': 'Oliver Schmidt', 'dept': 'Finance', 'role': 'Financial Analyst'},
        {'id': 'EMP009', 'name': 'Zara Ahmed', 'dept': 'Product', 'role': 'Product Manager'},
        {'id': 'EMP010', 'name': 'Lucas Andersson', 'dept': 'Support', 'role': 'Customer Success'},
        {'id': 'EMP011', 'name': 'Maya Patel', 'dept': 'Research', 'role': 'UX Researcher'},
        {'id': 'EMP012', 'name': 'Carlos Mendoza', 'dept': 'Operations', 'role': 'Operations Manager'},
        {'id': 'EMP013', 'name': 'Aisha Williams', 'dept': 'Legal', 'role': 'Legal Counsel'},
        {'id': 'EMP014', 'name': 'Noah Zhang', 'dept': 'Engineering', 'role': 'Backend Developer'},
        {'id': 'EMP015', 'name': 'Elena Rossi', 'dept': 'Sales', 'role': 'Sales Director'},
        {'id': 'EMP016', 'name': 'James O\'Connor', 'dept': 'IT', 'role': 'Systems Administrator'},
        {'id': 'EMP017', 'name': 'Priya Sharma', 'dept': 'Quality', 'role': 'QA Engineer'},
        {'id': 'EMP018', 'name': 'Antonio Garcia', 'dept': 'Maintenance', 'role': 'Facility Manager'},
        {'id': 'EMP019', 'name': 'Sarah Mitchell', 'dept': 'Training', 'role': 'Learning Specialist'},
        {'id': 'EMP020', 'name': 'Hassan Ali', 'dept': 'Procurement', 'role': 'Procurement Specialist'},
    ]
    
    # Generate timesheet data for the last 30 days
    start_date = datetime.now() - timedelta(days=30)
    records = []
    
    for day_offset in range(30):
        current_date = start_date + timedelta(days=day_offset)
        
        # Skip weekends for most employees (some work weekends)
        if current_date.weekday() >= 5 and random.random() > 0.3:
            continue
        
        for emp in employees:
            # 85% chance employee works each day
            if random.random() > 0.85:
                continue
            
            emp_id = emp['id']
            dept = emp['dept']
            
            # Determine shift type based on department
            if dept in ['Security', 'Maintenance', 'IT']:
                # More likely to work night shifts
                shift_type = random.choice(['day', 'night', 'night'])
            else:
                # Mostly day shifts
                shift_type = random.choice(['day', 'day', 'day', 'night'])
            
            if shift_type == 'day':
                # Day shift variations
                start_time = random.choice([
                    '08:00', '08:15', '08:30', '07:45', '09:00'
                ])
                
                # Multiple check-ins/check-outs (realistic patterns)
                entries = []
                
                # Initial check-in
                entries.append({
                    'Employee_ID': emp_id,
                    'Date': current_date.strftime('%Y-%m-%d'),
                    'Time': start_time,
                    'Entry_Type': 'Check-in',
                    'Department': dept,
                    'Employee_Name': emp['name']
                })
                
                # Possible lunch break (60% chance)
                if random.random() > 0.4:
                    lunch_out = random.choice(['12:00', '12:30', '13:00'])
                    lunch_in = random.choice(['13:00', '13:30', '14:00'])
                    
                    entries.append({
                        'Employee_ID': emp_id,
                        'Date': current_date.strftime('%Y-%m-%d'),
                        'Time': lunch_out,
                        'Entry_Type': 'Check-out',
                        'Department': dept,
                        'Employee_Name': emp['name']
                    })
                    
                    entries.append({
                        'Employee_ID': emp_id,
                        'Date': current_date.strftime('%Y-%m-%d'),
                        'Time': lunch_in,
                        'Entry_Type': 'Check-in',
                        'Department': dept,
                        'Employee_Name': emp['name']
                    })
                
                # End of day check-out with possible overtime
                base_end = random.choice(['17:00', '17:15', '17:30'])
                
                # 30% chance of overtime
                if random.random() > 0.7:
                    overtime_end = random.choice(['18:00', '18:30', '19:00', '17:45'])
                    end_time = overtime_end
                else:
                    end_time = base_end
                
                entries.append({
                    'Employee_ID': emp_id,
                    'Date': current_date.strftime('%Y-%m-%d'),
                    'Time': end_time,
                    'Entry_Type': 'Check-out',
                    'Department': dept,
                    'Employee_Name': emp['name']
                })
                
            else:  # Night shift
                start_time = random.choice(['18:00', '18:30', '19:00', '20:00'])
                
                entries = []
                
                # Night shift check-in
                entries.append({
                    'Employee_ID': emp_id,
                    'Date': current_date.strftime('%Y-%m-%d'),
                    'Time': start_time,
                    'Entry_Type': 'Check-in',
                    'Department': dept,
                    'Employee_Name': emp['name']
                })
                
                # Possible dinner break
                if random.random() > 0.5:
                    break_out = random.choice(['22:00', '23:00', '00:00'])
                    break_in = random.choice(['23:00', '00:00', '01:00'])
                    
                    entries.append({
                        'Employee_ID': emp_id,
                        'Date': current_date.strftime('%Y-%m-%d'),
                        'Time': break_out,
                        'Entry_Type': 'Check-out',
                        'Department': dept,
                        'Employee_Name': emp['name']
                    })
                    
                    entries.append({
                        'Employee_ID': emp_id,
                        'Date': current_date.strftime('%Y-%m-%d'),
                        'Time': break_in,
                        'Entry_Type': 'Check-in',
                        'Department': dept,
                        'Employee_Name': emp['name']
                    })
                
                # End of night shift
                base_end = random.choice(['03:00', '03:30', '02:30'])
                
                # 25% chance of night overtime
                if random.random() > 0.75:
                    overtime_end = random.choice(['04:00', '05:00', '06:00'])
                    end_time = overtime_end
                else:
                    end_time = base_end
                
                # Check-out next day
                next_date = current_date + timedelta(days=1)
                entries.append({
                    'Employee_ID': emp_id,
                    'Date': next_date.strftime('%Y-%m-%d'),
                    'Time': end_time,
                    'Entry_Type': 'Check-out',
                    'Department': dept,
                    'Employee_Name': emp['name']
                })
            
            records.extend(entries)
    
    # Create DataFrame
    df = pd.DataFrame(records)
    
    # Add some realistic variations
    df['Location'] = np.random.choice(['Main Office', 'Branch A', 'Branch B', 'Remote'], size=len(df))
    df['Badge_ID'] = df['Employee_ID'].str.replace('EMP', 'BADGE')
    
    # Shuffle to make more realistic
    df = df.sample(frac=1).reset_index(drop=True)
    
    print(f"✨ Created beautiful demo dataset:")
    print(f"📊 Total Records: {len(df):,}")
    print(f"👥 Employees: {df['Employee_ID'].nunique()}")
    print(f"🏢 Departments: {df['Department'].nunique()}")
    print(f"📅 Date Range: {df['Date'].min()} to {df['Date'].max()}")
    print(f"🎯 Duplicate Rate: {((df.groupby(['Employee_ID', 'Date']).size() > 2).mean() * 100):.1f}%")
    
    return df

if __name__ == "__main__":
    print("🎨 Creating Beautiful Demo Data...")
    print("=" * 50)
    
    # Create demo data
    demo_df = create_beautiful_demo_data()
    
    # Save in multiple formats
    print("\n💾 Saving demo files...")
    
    # Excel file with multiple sheets
    with pd.ExcelWriter('beautiful_demo_timesheet.xlsx', engine='openpyxl') as writer:
        demo_df.to_excel(writer, sheet_name='Timesheet_Data', index=False)
        
        # Create a summary sheet
        summary = demo_df.groupby('Employee_ID').agg({
            'Date': 'nunique',
            'Employee_Name': 'first',
            'Department': 'first'
        }).rename(columns={'Date': 'Days_Worked'})
        summary.to_excel(writer, sheet_name='Employee_Summary')
    
    # CSV file
    demo_df.to_csv('beautiful_demo_timesheet.csv', index=False)
    
    # Sample file (first 100 records)
    demo_df.head(100).to_excel('beautiful_demo_sample.xlsx', index=False)
    
    print("✅ Files created successfully:")
    print("   📊 beautiful_demo_timesheet.xlsx (Complete dataset)")
    print("   📄 beautiful_demo_timesheet.csv (CSV format)")
    print("   🎯 beautiful_demo_sample.xlsx (Sample data)")
    print("")
    print("🚀 Ready to test the Beautiful Dashboard!")
    print("🌐 Upload any of these files to see the magic!")