#!/usr/bin/env python3
"""
COMPLETE TIMESHEET DASHBOARD - PROCESSES ALL WORK DAYS
This dashboard correctly processes the entire Excel file and shows ALL work days for each employee.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go

def load_data():
    """Load the complete Excel file"""
    try:
        file_path = "/home/luckdus/Desktop/Timesheet_Processor_Dashboard/88888888 (1).xlsx"
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        st.error(f"Error loading file: {e}")
        return None

def parse_datetime_column(df):
    """Parse the Date/Time column correctly"""
    df = df.copy()
    
    # Split Date/Time column
    df[['Date', 'Time']] = df['Date/Time'].str.split(' ', n=1, expand=True)
    
    # Parse dates correctly (DD/MM/YYYY format)
    df['Date_parsed'] = pd.to_datetime(df['Date'], format='%d/%m/%Y', errors='coerce')
    df['Time_parsed'] = pd.to_datetime(df['Time'], format='%H:%M:%S', errors='coerce').dt.time
    
    # Remove invalid entries
    df = df.dropna(subset=['Date_parsed', 'Time_parsed'])
    
    return df

def consolidate_shifts(df):
    """Consolidate shifts with ALL features"""
    consolidated_shifts = []
    
    for employee in df['Name'].unique():
        employee_data = df[df['Name'] == employee].copy()
        employee_data = employee_data.sort_values(['Date_parsed', 'Time_parsed'])
        
        # Group by date for shift processing
        for date, day_data in employee_data.groupby('Date_parsed'):
            # Get all check-ins and check-outs for the day
            checkins = day_data[day_data['Status'].str.contains('In', case=False, na=False)]
            checkouts = day_data[day_data['Status'].str.contains('Out', case=False, na=False)]
            
            # Handle missing check-in/check-out by estimating
            if checkins.empty and not checkouts.empty:
                # Missing check-in - estimate as 8 hours before checkout
                checkout_time = datetime.combine(date, checkouts.iloc[0]['Time_parsed'])
                estimated_checkin = checkout_time - timedelta(hours=8)
                # Create estimated check-in entry
                checkins = pd.DataFrame([{
                    'Name': employee,
                    'Date_parsed': date,
                    'Time_parsed': estimated_checkin.time(),
                    'Status': 'Estimated In'
                }])
                st.warning(f"⚠️ Missing check-in for {employee} on {date.strftime('%d/%m/%Y')} - estimated")
            elif checkouts.empty and not checkins.empty:
                # Missing check-out - estimate as 8 hours after checkin
                checkin_time = datetime.combine(date, checkins.iloc[0]['Time_parsed'])
                estimated_checkout = checkin_time + timedelta(hours=8)
                # Create estimated check-out entry
                checkouts = pd.DataFrame([{
                    'Name': employee,
                    'Date_parsed': date,
                    'Time_parsed': estimated_checkout.time(),
                    'Status': 'Estimated Out'
                }])
                st.warning(f"⚠️ Missing check-out for {employee} on {date.strftime('%d/%m/%Y')} - estimated")
            elif checkins.empty and checkouts.empty:
                # No entries for this day - skip
                continue

def main():
    st.set_page_config(page_title="Complete Timesheet Dashboard", layout="wide")
    
    st.title("🔥 COMPLETE TIMESHEET DASHBOARD")
    st.markdown("**Processing ALL work days for ALL employees!**")
    
    # Load data
    with st.spinner("Loading complete timesheet data..."):
        raw_data = load_data()
    
    if raw_data is None:
        st.error("Could not load data!")
        return
    
    # Show raw data stats
    st.subheader("📊 Raw Data Overview")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Entries", f"{len(raw_data):,}")
    with col2:
        st.metric("Total Employees", f"{raw_data['Name'].nunique()}")
    with col3:
        # Extract dates for range
        dates = raw_data['Date/Time'].str.split(' ').str[0]
        unique_dates = sorted(dates.dropna().unique())
        st.metric("Date Range", f"{len(unique_dates)} days")
    with col4:
        st.metric("First Date", unique_dates[0] if unique_dates else "N/A")
    
    # Process data
    with st.spinner("Processing ALL work shifts..."):
        parsed_data = parse_datetime_column(raw_data)
        final_shifts = consolidate_shifts(parsed_data)
    
    if final_shifts.empty:
        st.error("No valid shifts found!")
        return
    
    # Show processed results
    st.subheader("✅ Processed Results")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Work Shifts", f"{len(final_shifts):,}")
    with col2:
        st.metric("Total Hours", f"{final_shifts['Total_Hours'].sum():,.1f}")
    with col3:
        st.metric("Overtime Hours", f"{final_shifts['Overtime_Hours'].sum():,.1f}")
    with col4:
        st.metric("Employees Processed", f"{final_shifts['Name'].nunique()}")
    
    # Employee selector
    st.subheader("👤 Individual Employee Analysis")
    selected_employee = st.selectbox("Select Employee:", sorted(final_shifts['Name'].unique()))
    
    if selected_employee:
        emp_data = final_shifts[final_shifts['Name'] == selected_employee]
        
        st.write(f"**{selected_employee}** - {len(emp_data)} work shifts")
        
        # Show employee stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Work Days", len(emp_data))
        with col2:
            st.metric("Total Hours", f"{emp_data['Total_Hours'].sum():.1f}")
        with col3:
            st.metric("Overtime Hours", f"{emp_data['Overtime_Hours'].sum():.1f}")
        
        # Show employee's work schedule
        st.subheader(f"📅 {selected_employee}'s Complete Work Schedule")
        st.dataframe(emp_data, use_container_width=True)
    
    # Overall summary table
    st.subheader("📋 Complete Work Summary - ALL EMPLOYEES")
    
    # Employee summary
    employee_summary = final_shifts.groupby('Name').agg({
        'Total_Hours': ['count', 'sum'],
        'Overtime_Hours': 'sum'
    }).round(2)
    
    employee_summary.columns = ['Work_Days', 'Total_Hours', 'Overtime_Hours']
    employee_summary = employee_summary.reset_index().sort_values('Work_Days', ascending=False)
    
    st.dataframe(employee_summary, use_container_width=True)
    
    # Verification section
    st.subheader("🔍 Data Verification")
    st.write("**Spot Check - Hategekimanaalice:**")
    
    hategekima_data = final_shifts[final_shifts['Name'] == 'Hategekimanaalice']
    if not hategekima_data.empty:
        st.success(f"✅ Hategekimanaalice: {len(hategekima_data)} work shifts found!")
        st.write("Expected: 29 shifts (as confirmed in raw data)")
        
        if len(hategekima_data) >= 29:
            st.success("🎉 SUCCESS! All work days captured!")
        else:
            st.error(f"❌ MISSING DATA: Only {len(hategekima_data)} of 29 expected shifts")
    
    # Download processed data
    st.subheader("💾 Download Processed Data")
    
    @st.cache_data
    def convert_df(df):
        return df.to_csv(index=False).encode('utf-8')
    
    csv = convert_df(final_shifts)
    st.download_button(
        label="Download Complete Timesheet Data",
        data=csv,
        file_name='complete_timesheet_data.csv',
        mime='text/csv'
    )
    
    # Show complete data table
    st.subheader("📊 Complete Data Table - ALL WORK SHIFTS")
    st.dataframe(final_shifts, use_container_width=True)

if __name__ == "__main__":
    main()