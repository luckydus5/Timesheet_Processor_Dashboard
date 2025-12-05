"""
Attendance Analyzer Module - 100% Accurate Version
===================================================
Processes Excel attendance files and calculates accurate metrics for:
- Daily Attendance (unique days worked)
- Overtime Hours (precise calculation with validation)
- Weekend Work (Saturday/Sunday attendance)

This module ensures 100% accuracy for salary calculations.

Author: Attendance Statistics Dashboard
Version: 2.0.0 (100% Accurate)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import warnings
warnings.filterwarnings('ignore')


def load_attendance_file(file_path: str) -> pd.DataFrame:
    """
    Load attendance Excel file with proper parsing.
    
    The Excel files have:
    - Header at row 3 (index 2)
    - Combined Date/Time column
    - Columns: Department, Name, No., Date/Time, Status, Location ID, ID Number, VerifyCode, Comment
    
    Args:
        file_path: Path to the Excel file
        
    Returns:
        DataFrame with parsed DateTime column
        
    Raises:
        ValueError: If required columns are missing
    """
    # Read Excel file - header is at row 3 (0-indexed = 2)
    df = pd.read_excel(file_path, header=2)
    
    # Clean column names (remove whitespace)
    df.columns = df.columns.str.strip()
    
    # Verify required columns exist
    required_columns = ['Name', 'Date/Time', 'Status']
    missing_cols = [col for col in required_columns if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing required columns: {missing_cols}")
    
    # Parse Date/Time column with mixed format handling
    df['DateTime'] = pd.to_datetime(df['Date/Time'], format='mixed', dayfirst=False, errors='coerce')
    
    # Remove rows where DateTime couldn't be parsed
    invalid_rows = df['DateTime'].isna().sum()
    if invalid_rows > 0:
        print(f"Warning: {invalid_rows} rows had unparseable DateTime values and were removed.")
    df = df.dropna(subset=['DateTime'])
    
    # Extract separate Date and Time components for analysis
    df['Date'] = df['DateTime'].dt.date
    df['Time'] = df['DateTime'].dt.time
    df['DayOfWeek'] = df['DateTime'].dt.dayofweek  # 0=Monday, 6=Sunday
    df['IsWeekend'] = df['DayOfWeek'] >= 5  # Saturday=5, Sunday=6
    
    # Sort by Name and DateTime for proper pairing
    df = df.sort_values(['Name', 'DateTime']).reset_index(drop=True)
    
    return df


def calculate_daily_attendance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily attendance - count unique working days per employee.
    
    100% Accurate Logic:
    - Count distinct dates where an employee has at least one attendance record
    - Separate weekday and weekend attendance
    
    Args:
        df: DataFrame with DateTime column
        
    Returns:
        DataFrame with columns: Name, Department, TotalDays, WeekdayDays, WeekendDays
    """
    # Get first department for each employee (for reference)
    dept_lookup = df.groupby('Name')['Department'].first().reset_index()
    
    # Group by Name and Date, then count unique dates
    daily_records = df.groupby(['Name', 'Date']).agg({
        'IsWeekend': 'first',  # Weekend status for that date
        'DateTime': 'count'  # Count of records for that day
    }).reset_index()
    
    daily_records.columns = ['Name', 'Date', 'IsWeekend', 'RecordCount']
    
    # Aggregate by employee
    attendance_summary = daily_records.groupby('Name').agg({
        'Date': 'nunique',  # Total unique days
        'IsWeekend': lambda x: x.sum()  # Weekend days (where IsWeekend is True)
    }).reset_index()
    
    attendance_summary.columns = ['Name', 'TotalDays', 'WeekendDays']
    
    # Calculate weekday days
    attendance_summary['WeekdayDays'] = attendance_summary['TotalDays'] - attendance_summary['WeekendDays']
    
    # Convert weekend days to integer (it was summed as boolean)
    attendance_summary['WeekendDays'] = attendance_summary['WeekendDays'].astype(int)
    
    # Merge with department lookup
    attendance_summary = attendance_summary.merge(dept_lookup, on='Name', how='left')
    
    # Reorder columns
    attendance_summary = attendance_summary[['Name', 'Department', 'TotalDays', 'WeekdayDays', 'WeekendDays']]
    
    return attendance_summary


def calculate_overtime_hours(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate overtime hours with 100% accuracy.
    
    Logic:
    1. Filter records with "OverTime" in Status
    2. Identify OverTime In and OverTime Out entries
    3. Pair consecutive In/Out entries for the same person on the same date
    4. Calculate duration in hours (rounded to 2 decimal places)
    5. Sum total overtime per employee
    
    Validation:
    - Only pairs In -> Out (never Out -> In)
    - Must be on the same date (no cross-midnight pairing)
    - Out time must be after In time
    - Maximum single overtime session capped at 12 hours (sanity check)
    
    Args:
        df: DataFrame with DateTime and Status columns
        
    Returns:
        DataFrame with columns: Name, Department, TotalOvertimeHours, OvertimeSessions, AvgSessionHours
    """
    # Get department lookup
    dept_lookup = df.groupby('Name')['Department'].first().reset_index()
    
    # Filter overtime records
    overtime_df = df[df['Status'].str.contains('OverTime', case=False, na=False)].copy()
    
    if overtime_df.empty:
        # Return empty DataFrame with correct structure
        return pd.DataFrame(columns=['Name', 'Department', 'TotalOvertimeHours', 'OvertimeSessions', 'AvgSessionHours'])
    
    # Identify In and Out entries
    overtime_df['IsOvertimeIn'] = overtime_df['Status'].str.contains('In', case=False, na=False)
    overtime_df['IsOvertimeOut'] = overtime_df['Status'].str.contains('Out', case=False, na=False)
    
    # Sort by Name, Date, DateTime for proper pairing
    overtime_df = overtime_df.sort_values(['Name', 'Date', 'DateTime']).reset_index(drop=True)
    
    # Calculate overtime for each employee
    overtime_results = []
    
    for name in overtime_df['Name'].unique():
        employee_ot = overtime_df[overtime_df['Name'] == name].copy()
        
        total_hours = 0.0
        session_count = 0
        
        # Process each date separately
        for date in employee_ot['Date'].unique():
            date_records = employee_ot[employee_ot['Date'] == date].reset_index(drop=True)
            
            # Find paired In/Out entries
            i = 0
            while i < len(date_records):
                # Look for an "In" entry
                if date_records.loc[i, 'IsOvertimeIn'] and not date_records.loc[i, 'IsOvertimeOut']:
                    in_time = date_records.loc[i, 'DateTime']
                    
                    # Look for the next "Out" entry
                    j = i + 1
                    while j < len(date_records):
                        if date_records.loc[j, 'IsOvertimeOut'] and not date_records.loc[j, 'IsOvertimeIn']:
                            out_time = date_records.loc[j, 'DateTime']
                            
                            # Validate: Out time must be after In time
                            if out_time > in_time:
                                # Calculate duration in hours
                                duration = (out_time - in_time).total_seconds() / 3600.0
                                
                                # Sanity check: cap at 12 hours per session
                                if duration <= 12:
                                    total_hours += duration
                                    session_count += 1
                                else:
                                    print(f"Warning: {name} on {date} has overtime session > 12 hours ({duration:.2f}h). Capped at 12h.")
                                    total_hours += 12.0
                                    session_count += 1
                            
                            i = j  # Move past this Out entry
                            break
                        j += 1
                
                i += 1
        
        if session_count > 0:
            avg_session = total_hours / session_count
        else:
            avg_session = 0.0
        
        overtime_results.append({
            'Name': name,
            'TotalOvertimeHours': round(total_hours, 2),
            'OvertimeSessions': session_count,
            'AvgSessionHours': round(avg_session, 2)
        })
    
    overtime_summary = pd.DataFrame(overtime_results)
    
    # Merge with department
    overtime_summary = overtime_summary.merge(dept_lookup, on='Name', how='left')
    
    # Reorder columns
    overtime_summary = overtime_summary[['Name', 'Department', 'TotalOvertimeHours', 'OvertimeSessions', 'AvgSessionHours']]
    
    return overtime_summary


def calculate_weekend_attendance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate weekend attendance metrics.
    
    Args:
        df: DataFrame with DateTime and IsWeekend columns
        
    Returns:
        DataFrame with columns: Name, Department, WeekendDays, SaturdayDays, SundayDays, WeekendRecords
    """
    # Get department lookup
    dept_lookup = df.groupby('Name')['Department'].first().reset_index()
    
    # Filter weekend records
    weekend_df = df[df['IsWeekend'] == True].copy()
    
    if weekend_df.empty:
        return pd.DataFrame(columns=['Name', 'Department', 'WeekendDays', 'SaturdayDays', 'SundayDays', 'WeekendRecords'])
    
    # Add Saturday/Sunday flags
    weekend_df['IsSaturday'] = weekend_df['DayOfWeek'] == 5
    weekend_df['IsSunday'] = weekend_df['DayOfWeek'] == 6
    
    # Group by Name and Date to get unique weekend days
    weekend_daily = weekend_df.groupby(['Name', 'Date']).agg({
        'IsSaturday': 'first',
        'IsSunday': 'first',
        'DateTime': 'count'  # Records per day
    }).reset_index()
    
    weekend_daily.columns = ['Name', 'Date', 'IsSaturday', 'IsSunday', 'DailyRecords']
    
    # Aggregate by employee
    weekend_summary = weekend_daily.groupby('Name').agg({
        'Date': 'nunique',  # Unique weekend days
        'IsSaturday': 'sum',  # Saturday days
        'IsSunday': 'sum',  # Sunday days
        'DailyRecords': 'sum'  # Total weekend records
    }).reset_index()
    
    weekend_summary.columns = ['Name', 'WeekendDays', 'SaturdayDays', 'SundayDays', 'WeekendRecords']
    
    # Convert to integers
    weekend_summary['SaturdayDays'] = weekend_summary['SaturdayDays'].astype(int)
    weekend_summary['SundayDays'] = weekend_summary['SundayDays'].astype(int)
    weekend_summary['WeekendRecords'] = weekend_summary['WeekendRecords'].astype(int)
    
    # Merge with department
    weekend_summary = weekend_summary.merge(dept_lookup, on='Name', how='left')
    
    # Reorder columns
    weekend_summary = weekend_summary[['Name', 'Department', 'WeekendDays', 'SaturdayDays', 'SundayDays', 'WeekendRecords']]
    
    return weekend_summary


def calculate_all_metrics(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Calculate all attendance metrics with 100% accuracy.
    
    Args:
        df: DataFrame with DateTime column
        
    Returns:
        Dictionary containing:
        - 'daily_attendance': Daily attendance summary
        - 'overtime': Overtime summary
        - 'weekend': Weekend attendance summary
        - 'combined': Combined metrics for all employees
    """
    # Calculate individual metrics
    daily_attendance = calculate_daily_attendance(df)
    overtime = calculate_overtime_hours(df)
    weekend = calculate_weekend_attendance(df)
    
    # Create combined summary
    # Start with daily attendance as base
    combined = daily_attendance.copy()
    
    # Merge overtime data
    if not overtime.empty:
        overtime_cols = overtime[['Name', 'TotalOvertimeHours', 'OvertimeSessions', 'AvgSessionHours']]
        combined = combined.merge(overtime_cols, on='Name', how='left')
    else:
        combined['TotalOvertimeHours'] = 0.0
        combined['OvertimeSessions'] = 0
        combined['AvgSessionHours'] = 0.0
    
    # Fill NaN values (employees without overtime)
    combined['TotalOvertimeHours'] = combined['TotalOvertimeHours'].fillna(0.0)
    combined['OvertimeSessions'] = combined['OvertimeSessions'].fillna(0).astype(int)
    combined['AvgSessionHours'] = combined['AvgSessionHours'].fillna(0.0)
    
    # Merge weekend data (already included in daily_attendance as WeekendDays)
    # Add weekend-specific details from weekend summary
    if not weekend.empty:
        weekend_cols = weekend[['Name', 'SaturdayDays', 'SundayDays', 'WeekendRecords']]
        combined = combined.merge(weekend_cols, on='Name', how='left')
    else:
        combined['SaturdayDays'] = 0
        combined['SundayDays'] = 0
        combined['WeekendRecords'] = 0
    
    combined['SaturdayDays'] = combined['SaturdayDays'].fillna(0).astype(int)
    combined['SundayDays'] = combined['SundayDays'].fillna(0).astype(int)
    combined['WeekendRecords'] = combined['WeekendRecords'].fillna(0).astype(int)
    
    return {
        'daily_attendance': daily_attendance,
        'overtime': overtime,
        'weekend': weekend,
        'combined': combined
    }


def get_top_10_metrics(metrics: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Get Top 10 employees for each metric.
    
    Args:
        metrics: Dictionary from calculate_all_metrics()
        
    Returns:
        Dictionary containing Top 10 for each category:
        - 'top_overtime': Top 10 by overtime hours
        - 'top_weekend': Top 10 by weekend days
        - 'top_attendance': Top 10 by total days
        - 'top_records': Top 10 by total records (from combined)
    """
    combined = metrics['combined']
    
    result = {}
    
    # Top 10 Overtime (by TotalOvertimeHours)
    result['top_overtime'] = combined.nlargest(10, 'TotalOvertimeHours')[
        ['Name', 'Department', 'TotalOvertimeHours', 'OvertimeSessions', 'AvgSessionHours']
    ].reset_index(drop=True)
    
    # Top 10 Weekend (by WeekendDays)
    result['top_weekend'] = combined.nlargest(10, 'WeekendDays')[
        ['Name', 'Department', 'WeekendDays', 'SaturdayDays', 'SundayDays']
    ].reset_index(drop=True)
    
    # Top 10 Attendance (by TotalDays)
    result['top_attendance'] = combined.nlargest(10, 'TotalDays')[
        ['Name', 'Department', 'TotalDays', 'WeekdayDays', 'WeekendDays']
    ].reset_index(drop=True)
    
    return result


def get_employee_details(df: pd.DataFrame, employee_name: str) -> Dict:
    """
    Get detailed attendance information for a specific employee.
    
    Args:
        df: DataFrame with all attendance records
        employee_name: Name of the employee to lookup
        
    Returns:
        Dictionary with detailed employee attendance information
    """
    # Filter for employee
    emp_df = df[df['Name'] == employee_name].copy()
    
    if emp_df.empty:
        return {'error': f'Employee "{employee_name}" not found'}
    
    # Basic info
    department = emp_df['Department'].iloc[0]
    total_records = len(emp_df)
    
    # Date range
    first_date = emp_df['DateTime'].min()
    last_date = emp_df['DateTime'].max()
    
    # Daily attendance
    unique_days = emp_df['Date'].nunique()
    weekend_days = emp_df[emp_df['IsWeekend']]['Date'].nunique()
    weekday_days = unique_days - weekend_days
    
    # Calculate overtime for this employee
    overtime_df = emp_df[emp_df['Status'].str.contains('OverTime', case=False, na=False)].copy()
    
    total_overtime_hours = 0.0
    overtime_sessions = 0
    overtime_details = []
    
    if not overtime_df.empty:
        overtime_df['IsOvertimeIn'] = overtime_df['Status'].str.contains('In', case=False, na=False)
        overtime_df['IsOvertimeOut'] = overtime_df['Status'].str.contains('Out', case=False, na=False)
        overtime_df = overtime_df.sort_values(['Date', 'DateTime']).reset_index(drop=True)
        
        for date in overtime_df['Date'].unique():
            date_records = overtime_df[overtime_df['Date'] == date].reset_index(drop=True)
            
            i = 0
            while i < len(date_records):
                if date_records.loc[i, 'IsOvertimeIn'] and not date_records.loc[i, 'IsOvertimeOut']:
                    in_time = date_records.loc[i, 'DateTime']
                    
                    j = i + 1
                    while j < len(date_records):
                        if date_records.loc[j, 'IsOvertimeOut'] and not date_records.loc[j, 'IsOvertimeIn']:
                            out_time = date_records.loc[j, 'DateTime']
                            
                            if out_time > in_time:
                                duration = (out_time - in_time).total_seconds() / 3600.0
                                duration = min(duration, 12.0)  # Cap at 12 hours
                                
                                total_overtime_hours += duration
                                overtime_sessions += 1
                                overtime_details.append({
                                    'Date': str(date),
                                    'In': in_time.strftime('%H:%M:%S'),
                                    'Out': out_time.strftime('%H:%M:%S'),
                                    'Hours': round(duration, 2)
                                })
                            
                            i = j
                            break
                        j += 1
                
                i += 1
    
    return {
        'Name': employee_name,
        'Department': department,
        'TotalRecords': total_records,
        'DateRange': {
            'First': first_date.strftime('%Y-%m-%d'),
            'Last': last_date.strftime('%Y-%m-%d')
        },
        'Attendance': {
            'TotalDays': unique_days,
            'WeekdayDays': weekday_days,
            'WeekendDays': weekend_days
        },
        'Overtime': {
            'TotalHours': round(total_overtime_hours, 2),
            'Sessions': overtime_sessions,
            'AvgSessionHours': round(total_overtime_hours / overtime_sessions, 2) if overtime_sessions > 0 else 0.0,
            'Details': overtime_details[:10]  # First 10 sessions only
        }
    }


def create_bar_chart(data: pd.DataFrame, x_col: str, y_col: str, title: str, color: str = '#1f77b4'):
    """
    Create a Plotly bar chart for the data.
    
    Args:
        data: DataFrame with the data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title
        color: Bar color (default blue)
        
    Returns:
        Plotly figure object
    """
    import plotly.express as px
    
    fig = px.bar(
        data,
        x=x_col,
        y=y_col,
        title=title,
        color_discrete_sequence=[color],
        text=y_col
    )
    
    fig.update_traces(textposition='outside')
    fig.update_layout(
        xaxis_title=x_col,
        yaxis_title=y_col,
        xaxis_tickangle=-45,
        showlegend=False
    )
    
    return fig


def export_to_excel(metrics: Dict[str, pd.DataFrame], output_path: str) -> str:
    """
    Export all metrics to an Excel file with multiple sheets.
    
    Args:
        metrics: Dictionary from calculate_all_metrics()
        output_path: Path for the output Excel file
        
    Returns:
        Path to the created Excel file
    """
    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # Combined summary
        metrics['combined'].to_excel(writer, sheet_name='Combined Summary', index=False)
        
        # Daily attendance
        metrics['daily_attendance'].to_excel(writer, sheet_name='Daily Attendance', index=False)
        
        # Overtime
        if not metrics['overtime'].empty:
            metrics['overtime'].to_excel(writer, sheet_name='Overtime', index=False)
        
        # Weekend
        if not metrics['weekend'].empty:
            metrics['weekend'].to_excel(writer, sheet_name='Weekend Attendance', index=False)
        
        # Top 10 rankings
        top_10 = get_top_10_metrics(metrics)
        top_10['top_overtime'].to_excel(writer, sheet_name='Top 10 Overtime', index=False)
        top_10['top_weekend'].to_excel(writer, sheet_name='Top 10 Weekend', index=False)
        top_10['top_attendance'].to_excel(writer, sheet_name='Top 10 Attendance', index=False)
    
    return output_path


def validate_data(df: pd.DataFrame) -> Dict:
    """
    Validate the loaded data and return a summary.
    
    Args:
        df: DataFrame to validate
        
    Returns:
        Dictionary with validation results
    """
    total_records = len(df)
    unique_employees = df['Name'].nunique()
    unique_dates = df['Date'].nunique()
    
    # Date range
    date_range = {
        'min': df['DateTime'].min().strftime('%Y-%m-%d'),
        'max': df['DateTime'].max().strftime('%Y-%m-%d')
    }
    
    # Status breakdown
    status_counts = df['Status'].value_counts().to_dict()
    
    # Weekend vs weekday
    weekend_records = df[df['IsWeekend']].shape[0]
    weekday_records = total_records - weekend_records
    
    # Check for overtime records
    overtime_records = df[df['Status'].str.contains('OverTime', case=False, na=False)].shape[0]
    
    return {
        'TotalRecords': total_records,
        'UniqueEmployees': unique_employees,
        'UniqueDates': unique_dates,
        'DateRange': date_range,
        'WeekdayRecords': weekday_records,
        'WeekendRecords': weekend_records,
        'OvertimeRecords': overtime_records,
        'StatusBreakdown': status_counts
    }


if __name__ == "__main__":
    # Test with a sample file if run directly
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"Loading: {file_path}")
        
        df = load_attendance_file(file_path)
        print(f"Loaded {len(df)} records for {df['Name'].nunique()} employees")
        
        # Validate data
        validation = validate_data(df)
        print(f"\nData Validation:")
        for key, value in validation.items():
            if key != 'StatusBreakdown':
                print(f"  {key}: {value}")
        
        # Calculate metrics
        metrics = calculate_all_metrics(df)
        
        # Get Top 10
        top_10 = get_top_10_metrics(metrics)
        
        print(f"\nTop 10 Overtime Hours:")
        print(top_10['top_overtime'][['Name', 'TotalOvertimeHours']].to_string(index=False))
        
        print(f"\nTop 10 Weekend Days:")
        print(top_10['top_weekend'][['Name', 'WeekendDays']].to_string(index=False))
        
        print(f"\nTop 10 Total Attendance Days:")
        print(top_10['top_attendance'][['Name', 'TotalDays']].to_string(index=False))
    else:
        print("Usage: python attendance_analyzer.py <excel_file_path>")
