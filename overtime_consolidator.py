"""
Overtime Consolidator Module
This module implements the Excel formula logic for calculating overtime at 1.5x rate
and consolidates it into a monthly summary by employee.
"""

import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta


def calculate_overtime_15_rate(start_time, end_time):
    """
    Calculate overtime hours at 1.5x rate based on the Excel formula logic:
    
    =IF(OR(ISBLANK(E4),ISBLANK(F4),ISNA(E4),ISNA(F4)),"",
    IF(E4<TIME(16,20,0),
       IF((F4+IF(F4<E4,1,0))>TIME(17,0,0),
          IF((F4+IF(F4<E4,1,0)-TIME(17,0,0))*24>=0.5,
             MIN(1.5,(F4+IF(F4<E4,1,0)-TIME(17,0,0))*24),
          0),
       0),
    IF(AND(E4>=TIME(16,20,0),F4<E4),
       3,
    0)))
    
    Args:
        start_time: Start time (datetime.time or string)
        end_time: End time (datetime.time or string)
    
    Returns:
        float: Overtime hours at 1.5x rate, or NaN if invalid
    """
    # Handle missing values
    if pd.isna(start_time) or pd.isna(end_time):
        return np.nan
    
    # Convert to time objects if they're strings
    if isinstance(start_time, str):
        try:
            start_time = pd.to_datetime(start_time).time()
        except:
            return np.nan
    
    if isinstance(end_time, str):
        try:
            end_time = pd.to_datetime(end_time).time()
        except:
            return np.nan
    
    # Convert time to datetime for calculation
    base_date = datetime(2000, 1, 1)
    start_dt = datetime.combine(base_date, start_time)
    end_dt = datetime.combine(base_date, end_time)
    
    # Handle midnight crossover (end time before start time)
    if end_time < start_time:
        end_dt += timedelta(days=1)
    
    # Define threshold times
    threshold_16_20 = time(16, 20, 0)  # 16:20
    threshold_17_00 = time(17, 0, 0)   # 17:00
    
    # CASE 1: Start time < 16:20
    if start_time < threshold_16_20:
        # Check if end time (adjusted for midnight) > 17:00
        end_dt_adjusted = end_dt
        threshold_17_00_dt = datetime.combine(base_date, threshold_17_00)
        
        if end_dt_adjusted > threshold_17_00_dt:
            # Calculate hours after 17:00
            ot_hours = (end_dt_adjusted - threshold_17_00_dt).total_seconds() / 3600
            
            # Only count if >= 0.5 hours
            if ot_hours >= 0.5:
                # Return minimum of 1.5 hours or actual OT hours
                return min(1.5, ot_hours)
            else:
                return 0.0
        else:
            return 0.0
    
    # CASE 2: Start time >= 16:20 AND end time crosses midnight
    elif start_time >= threshold_16_20 and end_time < start_time:
        return 3.0
    
    # CASE 3: All other cases
    else:
        return 0.0


def read_overal_sheet(file_path, sheet_name='Overal', header_row=2):
    """
    Read the Overal sheet from Excel file.
    
    Args:
        file_path: Path to Excel file
        sheet_name: Name of the sheet (default: 'Overal')
        header_row: Row number for headers (default: 2 for 0-indexed row 3)
    
    Returns:
        DataFrame with overtime data
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=header_row)
    
    # Ensure Date column is datetime
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    return df


def read_consolidated_sheet(file_path, sheet_name='Consolidated'):
    """
    Read the Consolidated sheet from Excel file.
    
    Args:
        file_path: Path to Excel file
        sheet_name: Name of the sheet (default: 'Consolidated')
    
    Returns:
        DataFrame with consolidated overtime data
    """
    df = pd.read_excel(file_path, sheet_name=sheet_name, header=0)
    return df


def apply_ot_formula(df_overal):
    """
    Apply the OT calculation formula to the Overal dataframe.
    
    Args:
        df_overal: DataFrame from Overal sheet
    
    Returns:
        DataFrame with calculated OT at 1.5x rate
    """
    df = df_overal.copy()
    
    # Calculate OT using the formula
    df['Calculated_Hrs_15_Rate'] = df.apply(
        lambda row: calculate_overtime_15_rate(row.get('Start time'), row.get('End time')),
        axis=1
    )
    
    return df


def consolidate_overtime_by_employee_month(df_overal):
    """
    Consolidate overtime hours by employee and month from the Overal sheet.
    
    Args:
        df_overal: DataFrame from Overal sheet with calculated OT
    
    Returns:
        DataFrame with consolidated OT by employee and month
    """
    df = df_overal.copy()
    
    # Ensure we have required columns
    if 'Date' not in df.columns or 'EMPLOYEE NAME' not in df.columns:
        raise ValueError("Required columns 'Date' and 'EMPLOYEE NAME' not found")
    
    # Use calculated OT if available, otherwise use existing column
    ot_column = 'Calculated_Hrs_15_Rate' if 'Calculated_Hrs_15_Rate' in df.columns else 'Hrs at 1.5 rate'
    
    # Extract year-month
    df['Year_Month'] = df['Date'].dt.to_period('M')
    
    # Group by employee and month
    consolidated = df.groupby(['EMPLOYEE NAME', 'Year_Month'])[ot_column].sum().reset_index()
    
    # Pivot to have months as columns
    pivot = consolidated.pivot(index='EMPLOYEE NAME', columns='Year_Month', values=ot_column)
    pivot = pivot.fillna(0)
    
    # Add total column
    pivot['Total'] = pivot.sum(axis=1)
    
    # Reset index to make employee name a column
    pivot = pivot.reset_index()
    
    return pivot


def update_consolidated_sheet(file_path, output_path=None):
    """
    Read Overal sheet, apply OT formula, and update Consolidated sheet.
    
    Args:
        file_path: Path to input Excel file
        output_path: Path to output Excel file (if None, creates a new file)
    
    Returns:
        Tuple of (df_overal_with_calc, df_consolidated_new)
    """
    # Read sheets
    df_overal = read_overal_sheet(file_path)
    df_consolidated_old = read_consolidated_sheet(file_path)
    
    # Apply OT formula
    df_overal = apply_ot_formula(df_overal)
    
    # Consolidate by employee and month
    df_consolidated_new = consolidate_overtime_by_employee_month(df_overal)
    
    # If output path specified, write to Excel
    if output_path:
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_overal.to_excel(writer, sheet_name='Overal_Updated', index=False)
            df_consolidated_new.to_excel(writer, sheet_name='Consolidated_New', index=False)
            df_consolidated_old.to_excel(writer, sheet_name='Consolidated_Old', index=False)
    
    return df_overal, df_consolidated_new


def compare_ot_calculations(df_overal):
    """
    Compare the existing 'Hrs at 1.5 rate' with calculated values.
    
    Args:
        df_overal: DataFrame with both existing and calculated OT
    
    Returns:
        DataFrame with comparison results
    """
    if 'Calculated_Hrs_15_Rate' not in df_overal.columns:
        df_overal = apply_ot_formula(df_overal)
    
    comparison = df_overal[[
        'SN', 'EMPLOYEE NAME', 'Date', 'Start time', 'End time',
        'Hrs at 1.5 rate', 'Calculated_Hrs_15_Rate'
    ]].copy()
    
    # Calculate difference
    comparison['Difference'] = (
        comparison['Calculated_Hrs_15_Rate'] - comparison['Hrs at 1.5 rate']
    )
    
    # Flag mismatches
    comparison['Match'] = np.isclose(
        comparison['Hrs at 1.5 rate'].fillna(0),
        comparison['Calculated_Hrs_15_Rate'].fillna(0),
        atol=0.01
    )
    
    return comparison


if __name__ == "__main__":
    # Test the module
    file_path = "Consolidated_OT management2.xlsx"
    
    print("="*60)
    print("OVERTIME CONSOLIDATOR TEST")
    print("="*60)
    
    # Read and process
    df_overal, df_consolidated = update_consolidated_sheet(
        file_path,
        output_path="Consolidated_OT_Updated.xlsx"
    )
    
    print("\n--- Overal Sheet with Calculated OT ---")
    print(df_overal[['EMPLOYEE NAME', 'Date', 'Start time', 'End time', 
                     'Hrs at 1.5 rate', 'Calculated_Hrs_15_Rate']].head(10))
    
    print("\n--- Consolidated Sheet (New) ---")
    print(df_consolidated.head(10))
    
    # Compare calculations
    comparison = compare_ot_calculations(df_overal)
    mismatches = comparison[~comparison['Match']]
    
    print(f"\n--- Comparison Results ---")
    print(f"Total records: {len(comparison)}")
    print(f"Matches: {comparison['Match'].sum()}")
    print(f"Mismatches: {len(mismatches)}")
    
    if len(mismatches) > 0:
        print("\nMismatched records:")
        print(mismatches)
    
    print("\n✅ Processing complete! Output saved to 'Consolidated_OT_Updated.xlsx'")
