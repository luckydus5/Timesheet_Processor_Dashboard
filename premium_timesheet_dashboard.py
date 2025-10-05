#!/usr/bin/env python3
"""
🌟 PREMIUM TIMESHEET MANAGER - OneDrive Style Dashboard
Professional Cloud-Style Interface for Timesheet Processing

Features:
- OneDrive-inspired modern design
- File management interface
- Preserve original Excel structure
- Add calculated columns without sorting
- Premium visual experience
- Professional cloud-style UI

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
import zipfile
from pathlib import Path

# Page Configuration - Premium Style
st.set_page_config(
    page_title="Premium Timesheet Manager",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "Premium Timesheet Manager - Professional Cloud Experience"
    }
)

# Premium CSS Styling - OneDrive Inspired
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Cloud Theme */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Main Container */
    .main-container {
        background: white;
        border-radius: 12px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin: 20px;
        padding: 0;
        overflow: hidden;
    }
    
    /* Header Bar - OneDrive Style */
    .header-bar {
        background: #0078d4;
        color: white;
        padding: 16px 24px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #e1e5e9;
    }
    
    .header-title {
        font-size: 20px;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    
    .header-actions {
        display: flex;
        gap: 12px;
        align-items: center;
    }
    
    /* Breadcrumb Navigation */
    .breadcrumb {
        background: #f8f9fa;
        padding: 12px 24px;
        border-bottom: 1px solid #e1e5e9;
        font-size: 14px;
        color: #323130;
    }
    
    .breadcrumb-item {
        color: #0078d4;
        text-decoration: none;
        cursor: pointer;
    }
    
    .breadcrumb-separator {
        margin: 0 8px;
        color: #605e5c;
    }
    
    /* File List Container */
    .file-container {
        padding: 24px;
        background: white;
    }
    
    /* File Item - OneDrive Style */
    .file-item {
        display: flex;
        align-items: center;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 4px;
        transition: all 0.2s ease;
        cursor: pointer;
        border: 1px solid transparent;
    }
    
    .file-item:hover {
        background: #f3f2f1;
        border-color: #edebe9;
    }
    
    .file-item.selected {
        background: #deecf9;
        border-color: #0078d4;
    }
    
    .file-icon {
        width: 32px;
        height: 32px;
        margin-right: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    
    .file-info {
        flex: 1;
        min-width: 0;
    }
    
    .file-name {
        font-weight: 500;
        color: #323130;
        font-size: 14px;
        margin-bottom: 2px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .file-details {
        font-size: 12px;
        color: #605e5c;
    }
    
    .file-meta {
        display: flex;
        gap: 24px;
        align-items: center;
        font-size: 13px;
        color: #605e5c;
        min-width: 400px;
    }
    
    /* Upload Zone */
    .upload-zone {
        border: 2px dashed #d1d1d1;
        border-radius: 8px;
        padding: 40px;
        text-align: center;
        margin: 24px;
        background: #fafafa;
        transition: all 0.3s ease;
    }
    
    .upload-zone:hover {
        border-color: #0078d4;
        background: #f3f9ff;
    }
    
    .upload-icon {
        font-size: 48px;
        color: #0078d4;
        margin-bottom: 16px;
    }
    
    .upload-text {
        font-size: 16px;
        color: #323130;
        margin-bottom: 8px;
    }
    
    .upload-subtext {
        font-size: 14px;
        color: #605e5c;
    }
    
    /* Processing Panel */
    .processing-panel {
        background: white;
        border-radius: 8px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Metrics Cards */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 16px;
        margin: 24px 0;
    }
    
    .metric-card {
        background: white;
        border-radius: 8px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid #e1e5e9;
        transition: all 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #0078d4;
        margin-bottom: 4px;
    }
    
    .metric-label {
        font-size: 14px;
        color: #605e5c;
        font-weight: 500;
    }
    
    /* Action Buttons */
    .action-button {
        background: #0078d4;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.2s ease;
        display: inline-flex;
        align-items: center;
        gap: 8px;
    }
    
    .action-button:hover {
        background: #106ebe;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(0,120,212,0.3);
    }
    
    .action-button.secondary {
        background: #f3f2f1;
        color: #323130;
        border: 1px solid #d1d1d1;
    }
    
    .action-button.secondary:hover {
        background: #edebe9;
        transform: translateY(-1px);
    }
    
    /* Status Indicators */
    .status-success {
        background: #d4edda;
        color: #155724;
        padding: 12px 16px;
        border-radius: 6px;
        border-left: 4px solid #28a745;
        margin: 16px 0;
    }
    
    .status-error {
        background: #f8d7da;
        color: #721c24;
        padding: 12px 16px;
        border-radius: 6px;
        border-left: 4px solid #dc3545;
        margin: 16px 0;
    }
    
    .status-info {
        background: #cce7ff;
        color: #004578;
        padding: 12px 16px;
        border-radius: 6px;
        border-left: 4px solid #0078d4;
        margin: 16px 0;
    }
    
    /* Data Tables */
    .data-table {
        border: 1px solid #e1e5e9;
        border-radius: 8px;
        overflow: hidden;
        margin: 16px 0;
    }
    
    .data-table thead {
        background: #f8f9fa;
    }
    
    .data-table th {
        padding: 12px 16px;
        font-weight: 600;
        color: #323130;
        border-bottom: 1px solid #e1e5e9;
    }
    
    .data-table td {
        padding: 12px 16px;
        border-bottom: 1px solid #f1f1f1;
    }
    
    /* Progress Bars */
    .progress-container {
        background: #f3f2f1;
        border-radius: 4px;
        height: 8px;
        margin: 8px 0;
        overflow: hidden;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #0078d4, #40e0d0);
        height: 100%;
        transition: width 0.3s ease;
        border-radius: 4px;
    }
    
    /* Animation Classes */
    .fade-in {
        animation: fadeIn 0.5s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .slide-up {
        animation: slideUp 0.3s ease-out;
    }
    
    @keyframes slideUp {
        from { transform: translateY(10px); opacity: 0; }
        to { transform: translateY(0); opacity: 1; }
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .header-bar {
            flex-direction: column;
            gap: 12px;
            text-align: center;
        }
        
        .file-meta {
            display: none;
        }
        
        .metrics-grid {
            grid-template-columns: 1fr;
        }
    }
</style>
""", unsafe_allow_html=True)

class PremiumTimesheetManager:
    """Premium cloud-style timesheet processor"""
    
    def __init__(self):
        self.BASE_FOLDER = "/home/luckdus/Desktop/Data Cleaner"
        self.processed_files = []
        
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

    def calculate_work_metrics(self, df_original):
        """Calculate metrics while preserving original structure"""
        
        # Create a copy with calculated columns
        df_enhanced = df_original.copy()
        
        # Parse datetime if needed
        if 'Date/Time' in df_enhanced.columns:
            df_enhanced['DateTime_parsed'] = pd.to_datetime(df_enhanced['Date/Time'], errors='coerce')
            df_enhanced['Date_Calc'] = df_enhanced['DateTime_parsed'].dt.strftime('%d/%m/%Y')
            df_enhanced['Time_Calc'] = df_enhanced['DateTime_parsed'].dt.strftime('%H:%M:%S')
        else:
            df_enhanced['Date_Calc'] = df_enhanced['Date']
            df_enhanced['Time_Calc'] = df_enhanced['Time']
        
        # Add parsing columns
        df_enhanced[['Date_parsed', 'Time_parsed']] = df_enhanced.apply(
            lambda row: pd.Series(self.parse_date_time(row.get('Date_Calc'), row.get('Time_Calc'))), axis=1
        )
        
        # Group by employee and date to calculate daily metrics
        daily_metrics = []
        
        for (name, date), group in df_enhanced.groupby(['Name', 'Date_parsed']):
            if pd.isna(date):
                continue
                
            # Find first check-in and last check-out
            sorted_group = group.sort_values('Time_parsed')
            checkins = sorted_group[sorted_group['Status'].isin(['C/In', 'OverTime In'])]
            checkouts = sorted_group[sorted_group['Status'].isin(['C/Out', 'OverTime Out'])]
            
            if not checkins.empty and not checkouts.empty:
                start_time = checkins.iloc[0]['Time_parsed']
                end_time = checkouts.iloc[-1]['Time_parsed']
                
                # Calculate metrics
                shift_type = self.determine_shift_type(start_time)
                total_hours = self.calculate_total_hours(start_time, end_time, shift_type)
                overtime_hours = self.calculate_overtime(start_time, end_time, shift_type)
                regular_hours = max(total_hours - overtime_hours, 0)
                
                daily_metrics.append({
                    'Name': name,
                    'Date_parsed': date,
                    'Start_Time': start_time,
                    'End_Time': end_time,
                    'Shift_Type': shift_type,
                    'Total_Hours': total_hours,
                    'Regular_Hours': regular_hours,
                    'Overtime_Hours': overtime_hours,
                    'Entry_Count': len(group)
                })
        
        # Create daily metrics dataframe
        daily_df = pd.DataFrame(daily_metrics)
        
        # Merge calculated columns back to original data (preserving order)
        if not daily_df.empty:
            # Create lookup dictionary
            metrics_lookup = {}
            for _, row in daily_df.iterrows():
                key = (row['Name'], row['Date_parsed'])
                metrics_lookup[key] = {
                    'Calculated_Start_Time': row['Start_Time'].strftime('%H:%M:%S') if row['Start_Time'] else '',
                    'Calculated_End_Time': row['End_Time'].strftime('%H:%M:%S') if row['End_Time'] else '',
                    'Calculated_Shift_Type': row['Shift_Type'],
                    'Calculated_Total_Hours': row['Total_Hours'],
                    'Calculated_Regular_Hours': row['Regular_Hours'],
                    'Calculated_Overtime_Hours': row['Overtime_Hours'],
                    'Daily_Entry_Count': row['Entry_Count']
                }
            
            # Add calculated columns to original data
            for key, metrics in metrics_lookup.items():
                mask = (df_enhanced['Name'] == key[0]) & (df_enhanced['Date_parsed'] == key[1])
                for col, value in metrics.items():
                    df_enhanced.loc[mask, col] = value
        
        return df_enhanced, daily_df
    
    def determine_shift_type(self, start_time):
        """Determine shift type"""
        if start_time is None:
            return ""
        start_decimal = start_time.hour + start_time.minute/60
        return "Day Shift" if start_decimal < 18.0 else "Night Shift"
    
    def calculate_total_hours(self, start_time, end_time, shift_type):
        """Calculate total work hours"""
        if start_time is None or end_time is None:
            return 0
        
        start_dt = datetime.combine(datetime.today(), start_time)
        end_dt = datetime.combine(datetime.today(), end_time)
        
        if shift_type == "Night Shift" and end_time < start_time:
            end_dt += timedelta(days=1)
        
        total_duration = end_dt - start_dt
        return round(total_duration.total_seconds() / 3600, 2)
    
    def calculate_overtime(self, start_time, end_time, shift_type):
        """Calculate overtime hours"""
        if start_time is None or end_time is None:
            return 0
        
        overtime = 0
        end_decimal = end_time.hour + end_time.minute/60
        
        if shift_type == "Day Shift" and end_decimal > 17.0:
            overtime = end_decimal - 17.0
            overtime = 0 if overtime < 0.5 else min(overtime, 1.5)
        elif shift_type == "Night Shift" and end_decimal <= 12.0 and end_decimal > 3.0:
            overtime = end_decimal - 3.0
            overtime = 0 if overtime < 0.5 else min(overtime, 3.0)
        
        return round(overtime, 2)

def render_header():
    """Render OneDrive-style header"""
    st.markdown("""
    <div class="main-container">
        <div class="header-bar">
            <div class="header-title">
                <span>☁️</span>
                <span>Premium Timesheet Manager</span>
            </div>
            <div class="header-actions">
                <span style="font-size: 14px;">Professional Cloud Experience</span>
            </div>
        </div>
        
        <div class="breadcrumb">
            <span class="breadcrumb-item">📁 My files</span>
            <span class="breadcrumb-separator">›</span>
            <span class="breadcrumb-item">💼 WORK</span>
            <span class="breadcrumb-separator">›</span>
            <span style="color: #323130; font-weight: 600;">⏰ Working Timesheet</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_file_manager():
    """Render OneDrive-style file manager"""
    
    # Check for existing files
    data_folder = "/home/luckdus/Desktop/Data Cleaner"
    files = []
    
    if os.path.exists(data_folder):
        for file in os.listdir(data_folder):
            if file.endswith(('.xlsx', '.xls', '.csv')):
                file_path = os.path.join(data_folder, file)
                stat = os.stat(file_path)
                
                # Determine file icon and type
                if file.endswith('.xlsx') or file.endswith('.xls'):
                    icon = "📊"
                    file_type = "Excel Workbook"
                else:
                    icon = "📄"
                    file_type = "CSV File"
                
                files.append({
                    'name': file,
                    'icon': icon,
                    'type': file_type,
                    'size': f"{stat.st_size / 1024:.1f} KB",
                    'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%B %d, %Y'),
                    'path': file_path
                })
    
    # File manager container
    st.markdown('<div class="file-container">', unsafe_allow_html=True)
    
    # Show existing files
    if files:
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
            <h3 style="margin: 0; color: #323130;">📂 Timesheet Files</h3>
            <span style="color: #605e5c; font-size: 14px;">{} files</span>
        </div>
        """.format(len(files)), unsafe_allow_html=True)
        
        # File list header
        st.markdown("""
        <div style="display: flex; align-items: center; padding: 8px 16px; background: #f8f9fa; border-radius: 6px; margin-bottom: 8px; font-weight: 600; color: #323130; font-size: 13px;">
            <div style="width: 50px;"></div>
            <div style="flex: 1;">Name</div>
            <div style="width: 120px;">Modified</div>
            <div style="width: 80px;">File size</div>
            <div style="width: 80px;">Sharing</div>
        </div>
        """, unsafe_allow_html=True)
        
        # File items
        for file in files:
            file_key = f"file_{file['name']}"
            
            if st.button(
                f"{file['icon']} {file['name']}", 
                key=file_key,
                help=f"Process {file['name']}",
                use_container_width=True
            ):
                st.session_state['selected_file'] = file
                st.rerun()
            
            # File details in columns
            col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
            with col2:
                st.caption(file['modified'])
            with col3:
                st.caption(file['size'])
            with col4:
                st.caption("Private")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return files

def render_upload_zone():
    """Render OneDrive-style upload zone"""
    
    st.markdown("""
    <div class="upload-zone">
        <div class="upload-icon">📤</div>
        <div class="upload-text">Upload timesheet files</div>
        <div class="upload-subtext">Drag files here or click to browse</div>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose your timesheet file",
        type=['csv', 'xlsx', 'xls'],
        help="Upload Excel or CSV timesheet files",
        label_visibility="hidden"
    )
    
    return uploaded_file

def render_processing_panel(df_original, df_enhanced, daily_metrics):
    """Render processing results panel"""
    
    st.markdown('<div class="processing-panel slide-up">', unsafe_allow_html=True)
    
    # Success message
    st.markdown("""
    <div class="status-success">
        <strong>✅ Processing Complete!</strong><br>
        Your timesheet has been enhanced with calculated fields while preserving the original structure.
    </div>
    """, unsafe_allow_html=True)
    
    # Metrics grid
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{len(df_original):,}</div>
            <div class="metric-label">Original Records</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{df_original['Name'].nunique()}</div>
            <div class="metric-label">Employees</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if not daily_metrics.empty:
            total_hours = daily_metrics['Total_Hours'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{total_hours:.1f}</div>
                <div class="metric-label">Total Hours</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col4:
        if not daily_metrics.empty:
            overtime_hours = daily_metrics['Overtime_Hours'].sum()
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{overtime_hours:.1f}</div>
                <div class="metric-label">Overtime Hours</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def create_premium_dashboard():
    """Main premium dashboard"""
    
    # Initialize manager
    manager = PremiumTimesheetManager()
    
    # Render header
    render_header()
    
    # Main content area
    st.markdown('<div class="fade-in" style="padding: 24px;">', unsafe_allow_html=True)
    
    # File manager
    files = render_file_manager()
    
    # Upload zone
    uploaded_file = render_upload_zone()
    
    # Process selected or uploaded file
    file_to_process = None
    
    if 'selected_file' in st.session_state:
        file_info = st.session_state['selected_file']
        file_to_process = file_info['path']
        st.info(f"📊 Selected: {file_info['name']}")
    
    if uploaded_file is not None:
        file_to_process = uploaded_file
        st.info(f"📤 Uploaded: {uploaded_file.name}")
    
    # Process file if available
    if file_to_process is not None:
        
        try:
            # Load data
            if isinstance(file_to_process, str):
                # Local file
                if file_to_process.endswith('.csv'):
                    df_original = pd.read_csv(file_to_process)
                else:
                    df_original = pd.read_excel(file_to_process)
            else:
                # Uploaded file
                if uploaded_file.name.endswith('.csv'):
                    df_original = pd.read_csv(uploaded_file)
                else:
                    df_original = pd.read_excel(uploaded_file)
            
            # Process with enhanced calculations
            with st.spinner("🔄 Processing timesheet data..."):
                df_enhanced, daily_metrics = manager.calculate_work_metrics(df_original)
            
            # Render processing panel
            render_processing_panel(df_original, df_enhanced, daily_metrics)
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Enhanced Data", 
                "📋 Original Data", 
                "📈 Daily Summary", 
                "💾 Export"
            ])
            
            with tab1:
                st.subheader("📊 Enhanced Timesheet (Original + Calculated Fields)")
                st.info("✨ Original data preserved with calculated columns added")
                
                # Show calculated columns
                calc_columns = [col for col in df_enhanced.columns if col.startswith('Calculated_')]
                if calc_columns:
                    st.markdown("**🧮 New Calculated Columns:**")
                    for col in calc_columns:
                        st.markdown(f"• `{col}`")
                
                st.dataframe(df_enhanced, use_container_width=True, height=400)
            
            with tab2:
                st.subheader("📋 Original Data (Unchanged)")
                st.info("🔒 Your original data structure is completely preserved")
                st.dataframe(df_original, use_container_width=True, height=400)
            
            with tab3:
                if not daily_metrics.empty:
                    st.subheader("📈 Daily Summary")
                    
                    # Summary metrics
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Shift distribution
                        shift_counts = daily_metrics['Shift_Type'].value_counts()
                        fig_pie = px.pie(
                            values=shift_counts.values,
                            names=shift_counts.index,
                            title="🎯 Shift Distribution",
                            color_discrete_sequence=['#0078d4', '#40e0d0']
                        )
                        fig_pie.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)'
                        )
                        st.plotly_chart(fig_pie, use_container_width=True)
                    
                    with col2:
                        # Hours by employee
                        emp_hours = daily_metrics.groupby('Name')['Total_Hours'].sum().sort_values(ascending=False).head(10)
                        fig_bar = px.bar(
                            x=emp_hours.values,
                            y=emp_hours.index,
                            orientation='h',
                            title="👥 Top Employees by Hours",
                            color=emp_hours.values,
                            color_continuous_scale='Blues'
                        )
                        fig_bar.update_layout(
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            yaxis={'categoryorder': 'total ascending'}
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)
                    
                    # Daily summary table
                    summary_display = daily_metrics.copy()
                    summary_display['Date'] = summary_display['Date_parsed'].dt.strftime('%d/%m/%Y')
                    summary_display['Start Time'] = summary_display['Start_Time'].dt.strftime('%H:%M:%S')
                    summary_display['End Time'] = summary_display['End_Time'].dt.strftime('%H:%M:%S')
                    
                    display_cols = ['Name', 'Date', 'Start Time', 'End Time', 'Shift_Type', 
                                  'Total_Hours', 'Regular_Hours', 'Overtime_Hours', 'Entry_Count']
                    
                    st.dataframe(
                        summary_display[display_cols], 
                        use_container_width=True,
                        column_config={
                            'Total_Hours': st.column_config.NumberColumn('Total Hours', format="%.2f"),
                            'Regular_Hours': st.column_config.NumberColumn('Regular Hours', format="%.2f"),
                            'Overtime_Hours': st.column_config.NumberColumn('Overtime Hours', format="%.2f"),
                        }
                    )
            
            with tab4:
                st.subheader("💾 Export Enhanced Data")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Enhanced data export
                    enhanced_csv = df_enhanced.to_csv(index=False)
                    st.download_button(
                        label="📊 Download Enhanced Data (CSV)",
                        data=enhanced_csv,
                        file_name=f"Enhanced_Timesheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        help="Original data + calculated columns"
                    )
                
                with col2:
                    # Excel with multiple sheets
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine='openpyxl') as writer:
                        # Enhanced data
                        df_enhanced.to_excel(writer, sheet_name='Enhanced_Data', index=False)
                        
                        # Original data
                        df_original.to_excel(writer, sheet_name='Original_Data', index=False)
                        
                        # Daily summary
                        if not daily_metrics.empty:
                            summary_export = daily_metrics.copy()
                            summary_export['Date'] = summary_export['Date_parsed'].dt.strftime('%d/%m/%Y')
                            summary_export['Start_Time'] = summary_export['Start_Time'].dt.strftime('%H:%M:%S')
                            summary_export['End_Time'] = summary_export['End_Time'].dt.strftime('%H:%M:%S')
                            export_cols = ['Name', 'Date', 'Start_Time', 'End_Time', 'Shift_Type', 
                                         'Total_Hours', 'Regular_Hours', 'Overtime_Hours', 'Entry_Count']
                            summary_export[export_cols].to_excel(writer, sheet_name='Daily_Summary', index=False)
                    
                    excel_data = output.getvalue()
                    st.download_button(
                        label="📊 Download Premium Excel",
                        data=excel_data,
                        file_name=f"Premium_Timesheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        help="Multi-sheet workbook with all data"
                    )
                
                # Additional export options
                st.markdown("---")
                
                if not daily_metrics.empty:
                    col3, col4 = st.columns(2)
                    
                    with col3:
                        # Daily summary only
                        summary_csv = summary_display[display_cols].to_csv(index=False)
                        st.download_button(
                            label="📈 Download Daily Summary (CSV)",
                            data=summary_csv,
                            file_name=f"Daily_Summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            help="Consolidated daily metrics"
                        )
                    
                    with col4:
                        # Original data only
                        original_csv = df_original.to_csv(index=False)
                        st.download_button(
                            label="📋 Download Original Data (CSV)",
                            data=original_csv,
                            file_name=f"Original_Timesheet_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv",
                            help="Unchanged original data"
                        )
                
        except Exception as e:
            st.markdown(f"""
            <div class="status-error">
                <strong>❌ Error Processing File</strong><br>
                {str(e)}
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; padding: 40px 0; color: #605e5c; border-top: 1px solid #e1e5e9; margin-top: 40px;">
        <p><strong>☁️ Premium Timesheet Manager</strong> • Professional Cloud Experience • October 2025</p>
        <p style="font-size: 12px;">✨ Preserves original data • 🧮 Adds calculations • 🎨 Beautiful interface</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    create_premium_dashboard()