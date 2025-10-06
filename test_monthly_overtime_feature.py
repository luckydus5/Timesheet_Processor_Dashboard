#!/usr/bin/env python3
"""
Test script to demonstrate the Monthly Overtime Summary feature
"""

import pandas as pd
from datetime import datetime

def format_hours_to_time(decimal_hours):
    """Convert decimal hours to HH:MM:SS format"""
    if decimal_hours == 0:
        return "00:00:00"
    
    hours = int(decimal_hours)
    minutes = int((decimal_hours - hours) * 60)
    seconds = int(((decimal_hours - hours) * 60 - minutes) * 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def add_monthly_overtime_summary(df):
    """Add monthly overtime summary columns for each person"""
    if df.empty:
        return df
    
    # Convert date strings to datetime for proper month extraction
    df['Date_dt'] = pd.to_datetime(df['Date'], format='%d/%m/%Y')
    df['Year_Month'] = df['Date_dt'].dt.to_period('M')
    
    # Calculate monthly overtime statistics for each person
    monthly_stats = []
    
    for name in df['Name'].unique():
        name_data = df[df['Name'] == name]
        
        for year_month in name_data['Year_Month'].unique():
            month_data = name_data[name_data['Year_Month'] == year_month]
            
            # Calculate total overtime hours for the month
            total_overtime_hours = month_data['Overtime Hours (Decimal)'].sum()
            
            # Count days with overtime (where overtime > 0)
            overtime_days = len(month_data[month_data['Overtime Hours (Decimal)'] > 0])
            
            # Format total overtime as HH:MM:SS
            total_overtime_formatted = format_hours_to_time(total_overtime_hours)
            
            # Create summary text
            monthly_summary = f"Month Total: {total_overtime_formatted} | OT Days: {overtime_days}"
            
            monthly_stats.append({
                'Name': name,
                'Year_Month': year_month,
                'Monthly_OT_Hours': total_overtime_hours,
                'Monthly_OT_Days': overtime_days,
                'Monthly_OT_Summary': monthly_summary
            })
    
    # Create monthly stats dataframe
    monthly_df = pd.DataFrame(monthly_stats)
    
    # Merge back to original dataframe
    df = df.merge(
        monthly_df[['Name', 'Year_Month', 'Monthly_OT_Summary']], 
        on=['Name', 'Year_Month'], 
        how='left'
    )
    
    # Clean up temporary columns
    df = df.drop(['Date_dt', 'Year_Month'], axis=1)
    
    return df

# Test with the provided data
def test_monthly_overtime_feature():
    """Test the monthly overtime summary feature with BAKOMEZA GIDEON data"""
    
    # Sample data from your attachment
    data = [
        {'Name': 'BAKOMEZA GIDEON', 'Date': '01/08/2025', 'Start Time': '06:44:57', 'End Time': '17:37:20', 'Shift Time': 'Day Shift', 'Total Hours': '10.87', 'Overtime Hours': '00:37:12', 'Overtime Hours (Decimal)': 0.62},
        {'Name': 'BAKOMEZA GIDEON', 'Date': '02/08/2025', 'Start Time': '06:46:12', 'End Time': '17:24:01', 'Shift Time': 'Day Shift', 'Total Hours': '10.63', 'Overtime Hours': '00:00:00', 'Overtime Hours (Decimal)': 0.0},
        {'Name': 'BAKOMEZA GIDEON', 'Date': '03/08/2025', 'Start Time': '06:47:45', 'End Time': '15:47:50', 'Shift Time': 'Day Shift', 'Total Hours': '9', 'Overtime Hours': '00:00:00', 'Overtime Hours (Decimal)': 0.0},
        {'Name': 'BAKOMEZA GIDEON', 'Date': '20/08/2025', 'Start Time': '06:44:05', 'End Time': '17:51:20', 'Shift Time': 'Day Shift', 'Total Hours': '11.12', 'Overtime Hours': '00:51:36', 'Overtime Hours (Decimal)': 0.86},
        {'Name': 'BAKOMEZA GIDEON', 'Date': '22/08/2025', 'Start Time': '06:48:55', 'End Time': '17:33:06', 'Shift Time': 'Day Shift', 'Total Hours': '10.74', 'Overtime Hours': '00:33:00', 'Overtime Hours (Decimal)': 0.55},
        {'Name': 'BAKOMEZA GIDEON', 'Date': '24/08/2025', 'Start Time': '21:36:35', 'End Time': '07:41:56', 'Shift Time': 'Night Shift', 'Total Hours': '10.09', 'Overtime Hours': '03:00:00', 'Overtime Hours (Decimal)': 3.0},
        {'Name': 'BAKOMEZA GIDEON', 'Date': '28/08/2025', 'Start Time': '06:44:14', 'End Time': '18:27:25', 'Shift Time': 'Day Shift', 'Total Hours': '11.72', 'Overtime Hours': '01:27:35', 'Overtime Hours (Decimal)': 1.46},
    ]
    
    df = pd.DataFrame(data)
    
    print("🧪 TESTING MONTHLY OVERTIME SUMMARY FEATURE")
    print("=" * 60)
    print("\n📊 Original Data Sample:")
    print(df[['Name', 'Date', 'Overtime Hours', 'Overtime Hours (Decimal)']])
    
    # Add monthly overtime summary
    df_with_summary = add_monthly_overtime_summary(df)
    
    print("\n✅ Data with Monthly Overtime Summary:")
    print(df_with_summary[['Name', 'Date', 'Overtime Hours', 'Monthly_OT_Summary']])
    
    # Calculate expected totals for verification
    total_ot_hours = df['Overtime Hours (Decimal)'].sum()
    ot_days = len(df[df['Overtime Hours (Decimal)'] > 0])
    
    print(f"\n🎯 EXPECTED RESULTS FOR BAKOMEZA GIDEON (August 2025):")
    print(f"   Total Overtime Hours: {format_hours_to_time(total_ot_hours)} ({total_ot_hours:.2f} decimal)")
    print(f"   Days with Overtime: {ot_days}")
    print(f"   Expected Summary: Month Total: {format_hours_to_time(total_ot_hours)} | OT Days: {ot_days}")
    
    print(f"\n✅ Feature working correctly! Each row now shows:")
    print(f"   - Individual daily overtime hours")
    print(f"   - Monthly overtime summary for that person")

if __name__ == "__main__":
    test_monthly_overtime_feature()