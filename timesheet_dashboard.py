#!/usr/bin/env python3
"""
🧹 TIMESHEET CONSOLIDATOR DASHBOARD
Professional Web Interface for Timesheet Data Processing

Features:
- File upload (Excel/CSV)
- Automatic duplicate entry consolidation
- Business rules application
- Interactive data visualization
- Export functionality
- Real-time processing feedback

Author: AI Assistant
Created: October 2025
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io
import base64
import os
from typing import Tuple, Optional, Dict, Any

# Page Configuration
st.set_page_config(
    page_title="🧹 Timesheet Consolidator Dashboard",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
    }
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #c3e6cb;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #f5c6cb;
    }
    .info-box {
        background-color: #d1ecf1;
        color: #0c5460;
        padding: 1rem;
        border-radius: 5px;
        border: 1px solid #bee5eb;
    }
</style>
""", unsafe_allow_html=True)

class TimesheetProcessor:
    """Core business logic for timesheet processing"""
    
    def __init__(self):
        self.BASE_FOLDER = "/home/luckdus/Desktop/Data Cleaner"
    
    def parse_date_time(self, date_str, time_str):
        """Parse separate date and time strings"""
        if pd.isna(date_str) or pd.isna(time_str) or date_str == '' or time_str == '':
            return None, None
        try:
            date_obj = pd.to_datetime(date_str, dayfirst=True).date()
            time_obj = pd.to_datetime(time_str, format='%H:%M:%S').time()
            return date_obj, time_obj
        except:
            return None, None

    def find_first_checkin_last_checkout(self, employee_day_records):
        """Find FIRST check-in and LAST check-out for an employee on a specific date"""
        if employee_day_records.empty:
            return None, None
        
        sorted_records = employee_day_records.sort_values('Time_parsed')
        checkins = sorted_records[sorted_records['Status'].isin(['C/In', 'OverTime In'])]
        checkouts = sorted_records[sorted_records['Status'].isin(['C/Out', 'OverTime Out'])]
        
        start_time = checkins.iloc[0]['Time_parsed'] if not checkins.empty else None
        end_time = checkouts.iloc[-1]['Time_parsed'] if not checkouts.empty else None
        
        return start_time, end_time

    def determine_shift_type(self, start_time):
        """Determine shift type based on FIRST check-in time"""
        if start_time is None:
            return ""
        
        start_decimal = start_time.hour + start_time.minute/60 + start_time.second/3600
        return "Day Shift" if start_decimal < 18.0 else "Night Shift"

    def calculate_total_work_hours(self, start_time, end_time, shift_type):
        """Calculate total work hours between start and end time"""
        if start_time is None or end_time is None:
            return 0
        
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        
        if shift_type == "Night Shift" and end_time < start_time:
            end_dt += timedelta(days=1)
        
        total_duration = end_dt - start_dt
        total_hours = total_duration.total_seconds() / 3600
        return round(total_hours, 2)

    def calculate_overtime_hours(self, start_time, end_time, shift_type):
        """Calculate overtime hours based on company business rules"""
        if start_time is None or end_time is None or shift_type == "":
            return 0
        
        overtime = 0
        
        if shift_type == "Day Shift":
            end_decimal = end_time.hour + end_time.minute/60 + end_time.second/3600
            if end_decimal > 17.0:  # After 5:00 PM
                overtime = end_decimal - 17.0
                if overtime < 0.5:
                    overtime = 0
                elif overtime > 1.5:
                    overtime = 1.5
                    
        elif shift_type == "Night Shift":
            end_decimal = end_time.hour + end_time.minute/60 + end_time.second/3600
            if end_decimal <= 12.0:  # Early morning hours
                if end_decimal > 3.0:  # After 3:00 AM
                    overtime = end_decimal - 3.0
                    if overtime < 0.5:
                        overtime = 0
                    elif overtime > 3.0:
                        overtime = 3.0
        
        return round(overtime, 2)

    def calculate_regular_hours(self, total_hours, overtime_hours):
        """Calculate regular hours (total - overtime)"""
        if total_hours == 0:
            return 0
        regular = total_hours - overtime_hours
        return round(max(regular, 0), 2)

    def load_timesheet_file(self, uploaded_file) -> Optional[pd.DataFrame]:
        """Load timesheet data from uploaded file"""
        try:
            if uploaded_file.name.lower().endswith('.xlsx') or uploaded_file.name.lower().endswith('.xls'):
                df = pd.read_excel(uploaded_file)
            elif uploaded_file.name.lower().endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                st.error("❌ File must be Excel (.xlsx/.xls) or CSV (.csv)")
                return None
            
            # Handle different file formats
            if 'Date/Time' in df.columns:
                st.info("🔄 Detected combined Date/Time column - splitting...")
                df['DateTime_parsed'] = pd.to_datetime(df['Date/Time'], errors='coerce')
                df['Date'] = df['DateTime_parsed'].dt.strftime('%d/%m/%Y')
                df['Time'] = df['DateTime_parsed'].dt.strftime('%H:%M:%S')
            
            # Check for required columns
            required_cols = ['Name', 'Date', 'Time', 'Status']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"❌ Missing required columns: {missing_cols}")
                st.info(f"💡 Available columns: {list(df.columns)}")
                return None
            
            return df
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return None

    def consolidate_timesheet_data(self, df) -> pd.DataFrame:
        """Master function to consolidate timesheet data and apply business rules"""
        
        # Make a copy and clean unnecessary columns
        df_work = df.copy()
        unnecessary_cols = [col for col in df_work.columns if 'Unnamed' in col]
        for col in unnecessary_cols:
            df_work = df_work.drop(col, axis=1)
        
        # Parse Date and Time
        df_work[['Date_parsed', 'Time_parsed']] = df_work.apply(
            lambda row: pd.Series(self.parse_date_time(row['Date'], row['Time'])), axis=1
        )
        
        # Remove rows where parsing failed
        initial_count = len(df_work)
        df_work = df_work[df_work['Date_parsed'].notna()]
        df_work = df_work[df_work['Time_parsed'].notna()]
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Consolidate entries by employee and date
        consolidated_rows = []
        employee_dates = df_work.groupby(['Name', 'Date_parsed'])
        total_groups = len(employee_dates)
        processed_groups = 0
        
        for (name, date), group_data in employee_dates:
            start_time, end_time = self.find_first_checkin_last_checkout(group_data)
            
            if start_time and end_time:
                shift_type = self.determine_shift_type(start_time)
                total_hours = self.calculate_total_work_hours(start_time, end_time, shift_type)
                overtime_hours = self.calculate_overtime_hours(start_time, end_time, shift_type)
                regular_hours = self.calculate_regular_hours(total_hours, overtime_hours)
                
                consolidated_row = {
                    'Name': name,
                    'Date': date.strftime('%d/%m/%Y'),
                    'Start Time': start_time.strftime('%H:%M:%S'),
                    'End Time': end_time.strftime('%H:%M:%S'),
                    'Shift Time': shift_type,
                    'Total Hours': total_hours,
                    'Regular Hours': regular_hours,
                    'Overtime Hours': overtime_hours,
                    'Original Entries': len(group_data),
                    'Entry Details': ', '.join([f"{row['Time']}({row['Status']})" for _, row in group_data.iterrows()])
                }
                
                consolidated_rows.append(consolidated_row)
            
            processed_groups += 1
            progress = processed_groups / total_groups
            progress_bar.progress(progress)
            status_text.text(f"Processing: {processed_groups}/{total_groups} employee-date combinations...")
        
        progress_bar.empty()
        status_text.empty()
        
        consolidated_df = pd.DataFrame(consolidated_rows)
        consolidated_df = consolidated_df.sort_values(['Name', 'Date'])
        
        return consolidated_df

def create_dashboard():
    """Main dashboard function"""
    
    # Header
    st.markdown('<h1 class="main-header">🧹 Timesheet Consolidator Dashboard</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div class="info-box">
    <h3>🎯 Professional Timesheet Data Processing System</h3>
    <p><strong>Features:</strong> File Upload • Duplicate Consolidation • Business Rules • Data Visualization • Export</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize processor
    processor = TimesheetProcessor()
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Dashboard Controls")
        
        # File Upload Section
        st.subheader("📂 File Upload")
        uploaded_file = st.file_uploader(
            "Choose your timesheet file",
            type=['csv', 'xlsx', 'xls'],
            help="Upload Excel or CSV timesheet files"
        )
        
        # Business Rules Display
        st.subheader("🎯 Business Rules")
        st.markdown("""
        **Day Shift (8AM-5PM):**
        - Overtime after 5:00 PM
        - Min: 30 minutes, Max: 1.5 hours
        
        **Night Shift (6PM-3AM):**
        - Overtime after 3:00 AM
        - Min: 30 minutes, Max: 3 hours
        
        **Consolidation Rules:**
        - Start Time: FIRST check-in
        - End Time: LAST check-out
        """)
    
    # Main Content Area
    if uploaded_file is not None:
        # Load and display file info
        st.subheader("📊 File Analysis")
        
        with st.spinner("Loading timesheet data..."):
            raw_data = processor.load_timesheet_file(uploaded_file)
        
        if raw_data is not None:
            # File Overview
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("📄 Total Records", f"{len(raw_data):,}")
            with col2:
                st.metric("👥 Unique Employees", raw_data['Name'].nunique())
            with col3:
                st.metric("📅 Date Range", f"{len(raw_data['Date'].unique())} days")
            with col4:
                st.metric("🔢 Columns", len(raw_data.columns))
            
            # Show sample data
            st.subheader("📋 Sample Data")
            st.dataframe(raw_data[['Name', 'Date', 'Time', 'Status']].head(10), use_container_width=True)
            
            # Duplicate Analysis
            st.subheader("🔍 Duplicate Entry Analysis")
            
            duplicate_analysis = raw_data.groupby(['Name', 'Date']).size().reset_index(name='Entry_Count')
            multiple_entries = duplicate_analysis[duplicate_analysis['Entry_Count'] > 1]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("📊 Employee-Date Combinations", f"{len(duplicate_analysis):,}")
            with col2:
                st.metric("🔄 With Multiple Entries", f"{len(multiple_entries):,}")
            with col3:
                duplicate_pct = len(multiple_entries)/len(duplicate_analysis)*100
                st.metric("📈 Duplicate Percentage", f"{duplicate_pct:.1f}%")
            
            # Entry Distribution Chart
            entry_distribution = duplicate_analysis['Entry_Count'].value_counts().sort_index()
            
            fig_dist = px.bar(
                x=entry_distribution.index,
                y=entry_distribution.values,
                title="📈 Entry Count Distribution",
                labels={'x': 'Entries per Day', 'y': 'Number of Employee-Days'},
                color=entry_distribution.values,
                color_continuous_scale='Blues'
            )
            fig_dist.update_layout(showlegend=False)
            st.plotly_chart(fig_dist, use_container_width=True)
            
            # Consolidation Process
            st.subheader("🚀 Data Consolidation")
            
            if st.button("🧹 Start Consolidation Process", type="primary"):
                with st.spinner("Consolidating duplicate entries and applying business rules..."):
                    consolidated_data = processor.consolidate_timesheet_data(raw_data)
                
                if not consolidated_data.empty:
                    # Store in session state for later use
                    st.session_state['consolidated_data'] = consolidated_data
                    st.session_state['raw_data'] = raw_data
                    
                    # Success message
                    st.markdown("""
                    <div class="success-box">
                    <h3>✅ Consolidation Completed Successfully!</h3>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Consolidation Summary
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("📊 Original Records", f"{len(raw_data):,}")
                    with col2:
                        st.metric("🧹 Consolidated Records", f"{len(consolidated_data):,}")
                    with col3:
                        reduction = len(raw_data) - len(consolidated_data)
                        st.metric("🗑️ Entries Removed", f"{reduction:,}")
                    with col4:
                        reduction_pct = (reduction / len(raw_data)) * 100
                        st.metric("📉 Reduction %", f"{reduction_pct:.1f}%")
    
    # Results Section (if data is consolidated)
    if 'consolidated_data' in st.session_state:
        consolidated_data = st.session_state['consolidated_data']
        
        st.header("📋 Consolidated Results")
        
        # Display consolidated data
        st.subheader("📊 Consolidated Timesheet Data")
        display_columns = ['Name', 'Date', 'Start Time', 'End Time', 'Shift Time', 
                          'Total Hours', 'Regular Hours', 'Overtime Hours']
        st.dataframe(consolidated_data[display_columns], use_container_width=True)
        
        # Analytics Section
        st.subheader("📈 Analytics & Insights")
        
        # Create tabs for different analytics
        tab1, tab2, tab3, tab4 = st.tabs(["🎯 Overview", "👥 By Employee", "📅 By Date", "💼 Overtime"])
        
        with tab1:
            # Shift Distribution
            col1, col2 = st.columns(2)
            
            with col1:
                shift_counts = consolidated_data['Shift Time'].value_counts()
                fig_pie = px.pie(
                    values=shift_counts.values,
                    names=shift_counts.index,
                    title="🎯 Shift Distribution",
                    color_discrete_sequence=['#1f77b4', '#ff7f0e']
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Overtime Analysis
                overtime_shifts = consolidated_data[consolidated_data['Overtime Hours'] > 0]
                total_overtime = consolidated_data['Overtime Hours'].sum()
                
                st.metric("💼 Shifts with Overtime", f"{len(overtime_shifts):,}")
                st.metric("⏰ Total Overtime Hours", f"{total_overtime:.2f}")
                st.metric("📊 Average OT per Shift", f"{total_overtime/len(consolidated_data):.2f}h")
        
        with tab2:
            # Employee Analysis
            employee_stats = consolidated_data.groupby('Name').agg({
                'Total Hours': 'sum',
                'Overtime Hours': 'sum',
                'Date': 'count'
            }).reset_index()
            employee_stats.columns = ['Employee', 'Total Hours', 'Overtime Hours', 'Days Worked']
            employee_stats = employee_stats.sort_values('Total Hours', ascending=False)
            
            st.dataframe(employee_stats, use_container_width=True)
            
            # Top performers chart
            top_10 = employee_stats.head(10)
            fig_emp = px.bar(
                top_10,
                x='Employee',
                y='Total Hours',
                title="🏆 Top 10 Employees by Total Hours",
                color='Total Hours',
                color_continuous_scale='Blues'
            )
            fig_emp.update_xaxes(tickangle=45)
            st.plotly_chart(fig_emp, use_container_width=True)
        
        with tab3:
            # Date Analysis
            consolidated_data['Date_parsed'] = pd.to_datetime(consolidated_data['Date'], format='%d/%m/%Y')
            daily_stats = consolidated_data.groupby('Date_parsed').agg({
                'Total Hours': 'sum',
                'Overtime Hours': 'sum',
                'Name': 'count'
            }).reset_index()
            daily_stats.columns = ['Date', 'Total Hours', 'Overtime Hours', 'Employees']
            
            fig_daily = px.line(
                daily_stats,
                x='Date',
                y='Total Hours',
                title="📅 Daily Total Hours Trend",
                markers=True
            )
            st.plotly_chart(fig_daily, use_container_width=True)
        
        with tab4:
            # Overtime Analysis
            overtime_data = consolidated_data[consolidated_data['Overtime Hours'] > 0]
            
            if not overtime_data.empty:
                # Overtime distribution
                fig_ot = px.histogram(
                    overtime_data,
                    x='Overtime Hours',
                    title="💼 Overtime Hours Distribution",
                    nbins=20,
                    color_discrete_sequence=['#ff7f0e']
                )
                st.plotly_chart(fig_ot, use_container_width=True)
                
                # Overtime by shift type
                ot_by_shift = overtime_data.groupby('Shift Time')['Overtime Hours'].agg(['count', 'sum', 'mean']).reset_index()
                ot_by_shift.columns = ['Shift Type', 'Count', 'Total OT', 'Average OT']
                st.dataframe(ot_by_shift, use_container_width=True)
            else:
                st.info("📊 No overtime hours found in the data")
        
        # Export Section
        st.subheader("💾 Export Data")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # CSV Export
            csv_data = consolidated_data[display_columns].to_csv(index=False)
            st.download_button(
                label="📄 Download CSV",
                data=csv_data,
                file_name=f"consolidated_timesheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                type="primary"
            )
        
        with col2:
            # Excel Export
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                consolidated_data[display_columns].to_excel(writer, sheet_name='Consolidated_Data', index=False)
                
                # Add summary sheet
                summary_data = {
                    'Metric': [
                        'Total Consolidated Records',
                        'Unique Employees',
                        'Date Range Start',
                        'Date Range End',
                        'Day Shift Records',
                        'Night Shift Records',
                        'Records with Overtime',
                        'Total Overtime Hours'
                    ],
                    'Value': [
                        len(consolidated_data),
                        consolidated_data['Name'].nunique(),
                        consolidated_data['Date'].min(),
                        consolidated_data['Date'].max(),
                        len(consolidated_data[consolidated_data['Shift Time'] == 'Day Shift']),
                        len(consolidated_data[consolidated_data['Shift Time'] == 'Night Shift']),
                        len(consolidated_data[consolidated_data['Overtime Hours'] > 0]),
                        f"{consolidated_data['Overtime Hours'].sum():.2f}"
                    ]
                }
                pd.DataFrame(summary_data).to_excel(writer, sheet_name='Summary', index=False)
            
            excel_data = output.getvalue()
            st.download_button(
                label="📊 Download Excel",
                data=excel_data,
                file_name=f"consolidated_timesheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                type="secondary"
            )
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666;">
    <p>🧹 <strong>Timesheet Consolidator Dashboard</strong> | Professional Data Processing System | October 2025</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    create_dashboard()