"""
🧹 TIMESHEET PROCESSOR DASHBOARD
================================
A beautiful web dashboard that replicates all functionality from Timesheet_Consolidator.ipynb
Processes, analyzes, cleans and creates consolidated timesheet data
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, time, timedelta
import plotly.express as px
import plotly.graph_objects as go
import io
import base64
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configure page
st.set_page_config(
    page_title="🧹 Timesheet Processor",
    page_icon="🧹",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Beautiful CSS styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Inter', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }
    
    .processing-step {
        background: rgba(255,255,255,0.95);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    
    .stSuccess {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border-radius: 8px;
    }
    
    .stError {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border-radius: 8px;
    }
</style>
""", unsafe_allow_html=True)

class TimesheetProcessor:
    def __init__(self):
        self.business_rules = {
            'day_shift_start': 8,
            'day_shift_end': 17,
            'night_shift_start': 18,
            'night_shift_end': 3,
            'min_overtime_minutes': 30,
            'max_day_overtime_hours': 1.5,
            'max_night_overtime_hours': 3.0
        }
    
    def parse_date_time(self, date_str, time_str):
        """Parse separate date and time strings"""
        if pd.isna(date_str) or pd.isna(time_str) or date_str == '' or time_str == '':
            return None, None
        try:
            # Parse date string (various formats supported, always output DD/MM/YYYY)
            date_obj = pd.to_datetime(date_str, dayfirst=True).date()
            
            # Parse time string
            time_obj = pd.to_datetime(time_str, format='%H:%M:%S').time()
            
            return date_obj, time_obj
        except:
            return None, None
    
    def detect_cross_midnight_shifts(self, df):
        """Detect and group cross-midnight shifts properly"""
        df_work = df.copy()
        df_work['Shift_Group'] = df_work['Date_parsed']  # Default: group by original date
        
        # Sort by employee, date, and time
        df_work = df_work.sort_values(['Name', 'Date_parsed', 'Time_parsed'])
        
        employees = df_work['Name'].unique()
        cross_midnight_count = 0
        
        for employee in employees:
            emp_data = df_work[df_work['Name'] == employee].copy()
            
            for i in range(len(emp_data) - 1):
                current_row = emp_data.iloc[i]
                next_row = emp_data.iloc[i + 1]
                
                # Check for cross-midnight pattern
                if (current_row['Status'] in ['OverTime In'] and 
                    next_row['Status'] in ['OverTime Out'] and
                    current_row['Date_parsed'] != next_row['Date_parsed']):
                    
                    # Calculate days between entries
                    days_diff = (next_row['Date_parsed'] - current_row['Date_parsed']).days
                    
                    # If it's next day and looks like night shift
                    if days_diff == 1:
                        current_time_decimal = current_row['Time_parsed'].hour + current_row['Time_parsed'].minute/60
                        next_time_decimal = next_row['Time_parsed'].hour + next_row['Time_parsed'].minute/60
                        
                        # Night shift pattern: start in evening (16:00+), end in morning (before 12:00)
                        if current_time_decimal >= 16.0 and next_time_decimal <= 12.0:
                            # Group both entries under the START date (the check-in date)
                            df_work.loc[df_work.index[df_work['Name'] == employee].tolist()[i+1], 'Shift_Group'] = current_row['Date_parsed']
                            cross_midnight_count += 1
        
        if cross_midnight_count > 0:
            st.info(f"🌙 Detected {cross_midnight_count} cross-midnight shift entries")
        
        return df_work

    def format_hours_as_time(self, hours):
        """Convert decimal hours to HH:MM format"""
        if hours == 0:
            return "0:00"
        
        # Extract whole hours
        whole_hours = int(hours)
        
        # Extract minutes from decimal part
        minutes_decimal = (hours - whole_hours) * 60
        whole_minutes = int(minutes_decimal)
        
        return f"{whole_hours}:{whole_minutes:02d}"

    def detect_cross_midnight_shifts(self, df):
        """Enhanced cross-midnight shift detection - handles all patterns including orphaned entries"""
        df_work = df.copy()
        df_work['Shift_Group'] = df_work['Date_parsed']  # Default: group by original date
        df_work['Processed'] = False  # Track which entries we've processed
        
        # Sort by employee, date, and time
        df_work = df_work.sort_values(['Name', 'Date_parsed', 'Time_parsed'])
        
        employees = df_work['Name'].unique()
        cross_midnight_count = 0
        
        for employee in employees:
            emp_data = df_work[df_work['Name'] == employee].copy()
            emp_indices = df_work[df_work['Name'] == employee].index.tolist()
            
            # STEP 1: Find direct cross-midnight patterns (In → Out next day)
            for i in range(len(emp_data) - 1):
                current_idx = emp_indices[i]
                next_idx = emp_indices[i + 1]
                
                current_row = emp_data.iloc[i]
                next_row = emp_data.iloc[i + 1]
                
                # Skip if already processed
                if df_work.loc[current_idx, 'Processed'] or df_work.loc[next_idx, 'Processed']:
                    continue
                
                # Check for cross-midnight pattern
                if (current_row['Status'] in ['OverTime In'] and 
                    next_row['Status'] in ['OverTime Out'] and
                    current_row['Date_parsed'] != next_row['Date_parsed']):
                    
                    days_diff = (next_row['Date_parsed'] - current_row['Date_parsed']).days
                    
                    if days_diff == 1:
                        current_time_decimal = current_row['Time_parsed'].hour + current_row['Time_parsed'].minute/60
                        next_time_decimal = next_row['Time_parsed'].hour + next_row['Time_parsed'].minute/60
                        
                        # Night shift pattern: start in evening (16:00+), end in morning (before 12:00)
                        if current_time_decimal >= 16.0 and next_time_decimal <= 12.0:
                            # Group both entries under the START date
                            df_work.loc[next_idx, 'Shift_Group'] = current_row['Date_parsed']
                            df_work.loc[current_idx, 'Processed'] = True
                            df_work.loc[next_idx, 'Processed'] = True
                            cross_midnight_count += 2
            
            # STEP 2: Find orphaned evening check-ins (night shift starts)
            for i in range(len(emp_data)):
                current_idx = emp_indices[i]
                current_row = emp_data.iloc[i]
                
                # Skip if already processed
                if df_work.loc[current_idx, 'Processed']:
                    continue
                
                # Look for evening OverTime In that might be start of night shift
                if current_row['Status'] == 'OverTime In':
                    current_time_decimal = current_row['Time_parsed'].hour + current_row['Time_parsed'].minute/60
                    
                    # Evening check-in (16:00 or later)
                    if current_time_decimal >= 16.0:
                        # Look for matching Out on next day(s)
                        current_date = current_row['Date_parsed']
                        
                        # Search next few days for matching checkout
                        for j in range(i + 1, min(i + 4, len(emp_data))):  # Look up to 3 days ahead
                            next_idx = emp_indices[j]
                            next_row = emp_data.iloc[j]
                            
                            # Skip if already processed
                            if df_work.loc[next_idx, 'Processed']:
                                continue
                            
                            # Look for morning checkout
                            if (next_row['Status'] in ['OverTime Out'] and 
                                next_row['Date_parsed'] > current_date):
                                
                                next_time_decimal = next_row['Time_parsed'].hour + next_row['Time_parsed'].minute/60
                                days_diff = (next_row['Date_parsed'] - current_date).days
                                
                                # Morning checkout (before 12:00) within reasonable time
                                if next_time_decimal <= 12.0 and days_diff <= 2:
                                    # Group checkout under the check-in date
                                    df_work.loc[next_idx, 'Shift_Group'] = current_date
                                    df_work.loc[current_idx, 'Processed'] = True
                                    df_work.loc[next_idx, 'Processed'] = True
                                    cross_midnight_count += 2
                                    break
            
            # STEP 3: Handle remaining orphaned morning checkouts
            for i in range(len(emp_data)):
                current_idx = emp_indices[i]
                current_row = emp_data.iloc[i]
                
                # Skip if already processed
                if df_work.loc[current_idx, 'Processed']:
                    continue
                
                # Look for morning OverTime Out that might be end of night shift
                if current_row['Status'] == 'OverTime Out':
                    current_time_decimal = current_row['Time_parsed'].hour + current_row['Time_parsed'].minute/60
                    
                    # Morning checkout (before 12:00)
                    if current_time_decimal <= 12.0:
                        current_date = current_row['Date_parsed']
                        
                        # Look for matching In on previous day(s)
                        for j in range(i - 1, max(i - 4, -1), -1):  # Look up to 3 days back
                            prev_idx = emp_indices[j]
                            prev_row = emp_data.iloc[j]
                            
                            # Skip if already processed
                            if df_work.loc[prev_idx, 'Processed']:
                                continue
                            
                            # Look for evening check-in
                            if (prev_row['Status'] in ['OverTime In'] and 
                                prev_row['Date_parsed'] < current_date):
                                
                                prev_time_decimal = prev_row['Time_parsed'].hour + prev_row['Time_parsed'].minute/60
                                days_diff = (current_date - prev_row['Date_parsed']).days
                                
                                # Evening check-in (16:00+) within reasonable time
                                if prev_time_decimal >= 16.0 and days_diff <= 2:
                                    # Group checkout under the check-in date
                                    df_work.loc[current_idx, 'Shift_Group'] = prev_row['Date_parsed']
                                    df_work.loc[prev_idx, 'Processed'] = True
                                    df_work.loc[current_idx, 'Processed'] = True
                                    cross_midnight_count += 2
                                    break
        
        # Clean up the temporary column
        df_work = df_work.drop('Processed', axis=1)
        
        if cross_midnight_count > 0:
            st.info(f"🌙 Enhanced detection: {cross_midnight_count} cross-midnight entries processed")
        
        return df_work

    def find_first_checkin_last_checkout(self, employee_day_records):
        """Find FIRST check-in and LAST check-out for an employee on a specific date"""
        if employee_day_records.empty:
            return None, None, None, None
        
        sorted_records = employee_day_records.sort_values('Time_parsed')
        
        # Find all check-ins and check-outs
        checkins = sorted_records[sorted_records['Status'].isin(['C/In', 'OverTime In'])]
        checkouts = sorted_records[sorted_records['Status'].isin(['C/Out', 'OverTime Out'])]
        
        start_time = None
        end_time = None
        start_date = None
        end_date = None
        
        # Get FIRST check-in
        if not checkins.empty:
            first_checkin = checkins.iloc[0]
            start_time = first_checkin['Time_parsed']
            start_date = first_checkin['Date_parsed']
        
        # Get LAST check-out
        if not checkouts.empty:
            last_checkout = checkouts.iloc[-1]
            end_time = last_checkout['Time_parsed']
            end_date = last_checkout['Date_parsed']
        
        return start_time, end_time, start_date, end_date

    def determine_shift_type(self, start_time, end_time, start_date=None, end_date=None):
        """Determine shift type based on check-in and check-out times
        
        Night Shift: Official 18:00 PM - 3:00 AM, but workers can check in as early as 16:20 PM
        """
        if start_time is None:
            return ""
        
        start_hour = start_time.hour
        start_minute = start_time.minute
        end_hour = end_time.hour if end_time else start_hour
        end_minute = end_time.minute if end_time else 0
        
        # Convert to decimal hours for easier comparison
        start_decimal = start_hour + start_minute/60
        end_decimal = end_hour + end_minute/60 if end_time else start_decimal
        
        # Case 1: Cross-midnight shift (start and end on different dates)
        if start_date and end_date and start_date != end_date:
            # If shift spans multiple dates, it's almost certainly a night shift
            return "Night Shift"
        
        # Case 2: Early Night Shift Detection (16:20 PM or later)
        # Check if start time is 16:20 (16.33) or later
        if start_decimal >= 16.33:  # 16:20 PM = 16.33 in decimal
            # If check-in is after 16:20 PM, likely night shift
            # Verify with check-out time if available
            if end_time:
                # If check-out is late night/early morning (18:00+ or 00:00-06:00), definitely night shift
                if end_decimal >= 18.0 or end_decimal <= 6.0:
                    return "Night Shift"
                # If check-out is very late same day (after 20:00), likely night shift
                elif end_decimal >= 20.0:
                    return "Night Shift"
            # Even without clear check-out, assume night shift if check-in >= 16:20
            return "Night Shift"
        
        # Case 3: Clear Day Shift (check-in between 6:00 AM and 4:19 PM)
        elif 6.0 <= start_decimal < 16.33:
            # Verify it's not a night shift ending in the morning
            if end_time and 0.0 <= end_decimal <= 6.0:
                # If check-out is early morning, might be night shift ending
                return "Night Shift"
            else:
                return "Day Shift"
        
        # Case 4: Late Night Shift (18:00 PM or later)
        elif start_decimal >= 18.0:
            return "Night Shift"
        
        # Case 5: Very early morning check-in (00:00 - 05:59)
        elif 0.0 <= start_decimal < 6.0:
            # If both check-in and check-out are in early morning, likely night shift ending
            if end_time and 0.0 <= end_decimal <= 12.0:
                return "Night Shift"
            # If check-out is later in the day, might be very early day shift
            else:
                return "Day Shift"
        
        # Default case (shouldn't happen, but safety)
        return "Day Shift"

    def calculate_total_work_hours(self, start_time, end_time, start_date, end_date, shift_type):
        """Calculate total work hours between start and end time"""
        if start_time is None or end_time is None:
            return 0
        
        # Create full datetime objects
        start_dt = datetime.combine(start_date, start_time)
        
        # Handle cross-midnight shifts
        if start_date != end_date:
            # Use actual end date for cross-midnight shifts
            end_dt = datetime.combine(end_date, end_time)
        else:
            # Same day shift
            end_dt = datetime.combine(start_date, end_time)
            
            # Handle case where end time is earlier than start time (cross-midnight on same date grouping)
            if shift_type == "Night Shift" and end_time < start_time:
                # Add one day to end time for cross-midnight calculation
                end_dt += timedelta(days=1)
        
        total_duration = end_dt - start_dt
        total_hours = total_duration.total_seconds() / 3600
        return round(total_hours, 2)

    def calculate_overtime_hours(self, start_time, end_time, start_date, end_date, shift_type):
        """Calculate overtime hours based on company business rules"""
        if start_time is None or end_time is None or shift_type == "":
            return 0
        
        overtime = 0
        end_decimal = end_time.hour + end_time.minute/60 + end_time.second/3600
        
        if shift_type == "Day Shift":
            if end_decimal > 17.0:  # After 5:00 PM
                overtime = end_decimal - 17.0
                if overtime < 0.5:
                    overtime = 0
                elif overtime > 1.5:
                    overtime = 1.5
                    
        elif shift_type == "Night Shift":
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

    def load_timesheet_file(self, uploaded_file):
        """Load timesheet data from uploaded file"""
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            
            # Handle different file formats
            if 'Date/Time' in df.columns:
                df['DateTime_parsed'] = pd.to_datetime(df['Date/Time'], errors='coerce')
                df['Date'] = df['DateTime_parsed'].dt.strftime('%d/%m/%Y')  # Ensure DD/MM/YYYY format
                df['Time'] = df['DateTime_parsed'].dt.strftime('%H:%M:%S')
            
            # Check for required columns
            required_cols = ['Name', 'Date', 'Time', 'Status']
            missing_cols = [col for col in required_cols if col not in df.columns]
            
            if missing_cols:
                st.error(f"❌ Missing required columns: {missing_cols}")
                return None
            
            return df
            
        except Exception as e:
            st.error(f"❌ Error loading file: {str(e)}")
            return None

    def analyze_duplicates(self, df):
        """Analyze duplicate entries in the data"""
        duplicate_analysis = df.groupby(['Name', 'Date']).size().reset_index(name='Entry_Count')
        multiple_entries = duplicate_analysis[duplicate_analysis['Entry_Count'] > 1]
        
        return {
            'total_combinations': len(duplicate_analysis),
            'multiple_entries': len(multiple_entries),
            'duplicate_percentage': len(multiple_entries)/len(duplicate_analysis)*100 if len(duplicate_analysis) > 0 else 0,
            'entry_distribution': duplicate_analysis['Entry_Count'].value_counts().sort_index(),
            'top_cases': multiple_entries.nlargest(3, 'Entry_Count')
        }

    def consolidate_timesheet_data(self, df):
        """Master function to consolidate timesheet data and apply business rules"""
        
        # Make a copy to avoid modifying original
        df_work = df.copy()
        
        # Remove unnecessary columns
        unnecessary_cols = [col for col in df_work.columns if 'Unnamed' in col]
        for col in unnecessary_cols:
            df_work = df_work.drop(col, axis=1)
        
        # Parse Date and Time
        df_work[['Date_parsed', 'Time_parsed']] = df_work.apply(
            lambda row: pd.Series(self.parse_date_time(row['Date'], row['Time'])), axis=1
        )
        
        # Remove rows where parsing failed
        df_work = df_work[df_work['Date_parsed'].notna()]
        df_work = df_work[df_work['Time_parsed'].notna()]
        
        # Detect cross-midnight shifts
        df_work = self.detect_cross_midnight_shifts(df_work)
        
        # Consolidate entries by employee and shift group (not just date)
        consolidated_rows = []
        employee_shifts = df_work.groupby(['Name', 'Shift_Group'])
        
        for (name, shift_date), group_data in employee_shifts:
            start_time, end_time, start_date, end_date = self.find_first_checkin_last_checkout(group_data)
            
            if start_time and end_time:
                shift_type = self.determine_shift_type(start_time, end_time, start_date, end_date)
                total_hours = self.calculate_total_work_hours(start_time, end_time, start_date, end_date, shift_type)
                overtime_hours = self.calculate_overtime_hours(start_time, end_time, start_date, end_date, shift_type)
                regular_hours = self.calculate_regular_hours(total_hours, overtime_hours)
                
                # Use start date for display
                display_date = start_date.strftime('%d/%m/%Y')
                
                consolidated_row = {
                    'Name': name,
                    'Date': display_date,
                    'Start Time': start_time.strftime('%H:%M:%S'),
                    'End Time': end_time.strftime('%H:%M:%S'),
                    'Shift Time': shift_type,
                    'Total Hours': total_hours,
                    'Regular Hours': regular_hours,
                    'Overtime Hours': self.format_hours_as_time(overtime_hours),
                    'Original Entries': len(group_data),
                    'Entry Details': ', '.join([f"{row['Date']}-{row['Time']}({row['Status']})" for _, row in group_data.iterrows()]),
                    'Cross_Midnight': 'Yes' if start_date != end_date else 'No'
                }
                
                consolidated_rows.append(consolidated_row)
        
        consolidated_df = pd.DataFrame(consolidated_rows)
        consolidated_df = consolidated_df.sort_values(['Name', 'Date'])
        
        return consolidated_df

def create_charts(df):
    """Create beautiful visualizations"""
    
    # Shift distribution
    shift_counts = df['Shift Time'].value_counts()
    fig_pie = px.pie(
        values=shift_counts.values, 
        names=shift_counts.index,
        title="🕐 Shift Distribution",
        color_discrete_sequence=['#667eea', '#764ba2', '#f093fb']
    )
    fig_pie.update_layout(font_family="Inter")
    
    # Top performers
    top_performers = df.groupby('Name')['Total Hours'].sum().sort_values(ascending=False).head(10)
    fig_bar = px.bar(
        x=top_performers.values,
        y=top_performers.index,
        orientation='h',
        title="🏆 Top 10 Performers (Total Hours)",
        color=top_performers.values,
        color_continuous_scale='Viridis'
    )
    fig_bar.update_layout(font_family="Inter")
    
    # Overtime analysis
    overtime_data = df[df['Overtime Hours'] != '0:00']
    if len(overtime_data) > 0:
        # Convert formatted overtime back to decimal for charting
        def parse_formatted_time(time_str):
            if time_str == '0:00':
                return 0
            parts = time_str.split(':')
            return int(parts[0]) + int(parts[1])/60
        
        overtime_values = overtime_data['Overtime Hours'].apply(parse_formatted_time)
        
        fig_overtime = px.histogram(
            x=overtime_values,
            title="📊 Overtime Hours Distribution",
            color_discrete_sequence=['#667eea'],
            labels={'x': 'Overtime Hours (decimal)'}
        )
        fig_overtime.update_layout(font_family="Inter")
    else:
        fig_overtime = None
    
    return fig_pie, fig_bar, fig_overtime

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🧹 Timesheet Processor Dashboard</h1>
        <p>Process, Analyze, Clean and Consolidate Timesheet Data</p>
    </div>
    """, unsafe_allow_html=True)
    
    processor = TimesheetProcessor()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 🎛️ Processing Controls")
        
        uploaded_file = st.file_uploader(
            "📁 Upload Timesheet File",
            type=['csv', 'xlsx', 'xls'],
            help="Upload Excel or CSV timesheet file"
        )
        
        st.markdown("---")
        st.markdown("### ⚙️ Business Rules")
        st.info("""
        **Day Shift**: 8:00 AM - 17:00 PM  
        **Night Shift**: 18:00 PM - 3:00 AM  
        **Overtime**: Min 30min, Max 1.5h (day) / 3h (night)  
        **Logic**: FIRST check-in → LAST check-out
        """)
    
    # Main processing area
    if uploaded_file is not None:
        # Load data
        with st.spinner("📊 Loading timesheet data..."):
            raw_data = processor.load_timesheet_file(uploaded_file)
        
        if raw_data is not None:
            st.success(f"✅ Successfully loaded {len(raw_data):,} records from {raw_data['Name'].nunique()} employees!")
            
            # Show sample data
            with st.expander("📋 View Sample Data", expanded=False):
                st.dataframe(raw_data[['Name', 'Date', 'Time', 'Status']].head(10))
            
            # Analyze duplicates
            st.markdown("### 🔍 Duplicate Entry Analysis")
            
            duplicate_info = processor.analyze_duplicates(raw_data)
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{duplicate_info['total_combinations']:,}</div>
                    <div class="metric-label">Employee-Date Combinations</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{duplicate_info['multiple_entries']:,}</div>
                    <div class="metric-label">Days with Multiple Entries</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{duplicate_info['duplicate_percentage']:.1f}%</div>
                    <div class="metric-label">Duplicate Rate</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                avg_entries = raw_data.groupby(['Name', 'Date']).size().mean()
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-value">{avg_entries:.1f}</div>
                    <div class="metric-label">Avg Entries/Day</div>
                </div>
                """, unsafe_allow_html=True)
            
            # Show entry distribution
            st.markdown("### 📈 Entry Distribution")
            distribution_data = duplicate_info['entry_distribution']
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.bar_chart(distribution_data)
            
            with col2:
                for count, frequency in distribution_data.items():
                    st.write(f"**{count} entries per day**: {frequency:,} employee-dates")
            
            # Process button
            if st.button("🧹 **PROCESS & CONSOLIDATE DATA**", type="primary"):
                with st.spinner("🔄 Consolidating duplicate entries and applying business rules..."):
                    consolidated_data = processor.consolidate_timesheet_data(raw_data)
                
                if consolidated_data is not None and not consolidated_data.empty:
                    st.success(f"🎉 Successfully consolidated {len(raw_data):,} records → {len(consolidated_data):,} clean records!")
                    
                    # Store in session state
                    st.session_state.consolidated_data = consolidated_data
                    st.session_state.original_data = raw_data
                    
                    # Show processing summary
                    st.markdown("### 📊 Processing Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{len(consolidated_data):,}</div>
                            <div class="metric-label">Final Records</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col2:
                        reduction = len(raw_data) - len(consolidated_data)
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{reduction:,}</div>
                            <div class="metric-label">Duplicates Removed</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col3:
                        overtime_shifts = len(consolidated_data[consolidated_data['Overtime Hours'] != '0:00'])
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">{overtime_shifts:,}</div>
                            <div class="metric-label">Overtime Shifts</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    with col4:
                        st.markdown(f"""
                        <div class="metric-card">
                            <div class="metric-value">📊</div>
                            <div class="metric-label">See Data Table</div>
                        </div>
                        """, unsafe_allow_html=True)
    
    # Show results if data is processed
    if 'consolidated_data' in st.session_state and st.session_state.consolidated_data is not None:
        consolidated_data = st.session_state.consolidated_data
        
        st.markdown("---")
        st.markdown("### 📊 Consolidated Results")
        
        # Create tabs for different views
        tab1, tab2, tab3, tab4 = st.tabs(["📋 Consolidated Data", "📈 Analytics", "🔍 Examples", "💾 Export"])
        
        with tab1:
            st.markdown("#### Clean Consolidated Timesheet Data")
            display_columns = ['Name', 'Date', 'Start Time', 'End Time', 'Shift Time', 
                             'Total Hours', 'Regular Hours', 'Overtime Hours']
            st.dataframe(consolidated_data[display_columns], use_container_width=True)
        
        with tab2:
            st.markdown("#### Visual Analytics")
            
            fig_pie, fig_bar, fig_overtime = create_charts(consolidated_data)
            
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(fig_pie, use_container_width=True)
            with col2:
                st.plotly_chart(fig_bar, use_container_width=True)
            
            if fig_overtime:
                st.plotly_chart(fig_overtime, use_container_width=True)
        
        with tab3:
            st.markdown("#### Consolidation Examples")
            
            # Show examples of complex consolidations
            multi_entry_cases = consolidated_data[consolidated_data['Original Entries'] > 1]
            if len(multi_entry_cases) > 0:
                top_cases = multi_entry_cases.nlargest(5, 'Original Entries')
                
                for _, row in top_cases.iterrows():
                    with st.expander(f"👤 {row['Name']} on {row['Date']} ({row['Original Entries']} entries)"):
                        st.write(f"**Entry Pattern**: {row['Entry Details']}")
                        st.write(f"**Consolidated Result**: {row['Start Time']} → {row['End Time']}")
                        st.write(f"**Shift Type**: {row['Shift Time']}")
                        st.write(f"**Hours**: {row['Total Hours']}h total, {row['Regular Hours']}h regular, {row['Overtime Hours']}h overtime")
        
        with tab4:
            st.markdown("#### Export Processed Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Excel export
                export_df = consolidated_data[['Name', 'Date', 'Start Time', 'End Time', 'Shift Time', 
                                            'Total Hours', 'Regular Hours', 'Overtime Hours']]
                
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    export_df.to_excel(writer, sheet_name='Consolidated_Data', index=False)
                    
                    # Summary sheet
                    summary_data = {
                        'Metric': ['Total Records', 'Unique Employees', 'Date Range Start', 'Date Range End',
                                 'Day Shifts', 'Night Shifts', 'Overtime Shifts', 'Total Overtime Hours'],
                        'Value': [len(consolidated_data), consolidated_data['Name'].nunique(),
                                consolidated_data['Date'].min(), consolidated_data['Date'].max(),
                                len(consolidated_data[consolidated_data['Shift Time'] == 'Day Shift']),
                                len(consolidated_data[consolidated_data['Shift Time'] == 'Night Shift']),
                                len(consolidated_data[consolidated_data['Overtime Hours'] != '0:00']),
                                f"See individual records for overtime totals"]
                    }
                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                st.download_button(
                    label="📊 Download Excel",
                    data=buffer.getvalue(),
                    file_name=f"Consolidated_Timesheet_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            with col2:
                # CSV export
                csv = export_df.to_csv(index=False)
                st.download_button(
                    label="📄 Download CSV",
                    data=csv,
                    file_name=f"Consolidated_Timesheet_{timestamp}.csv",
                    mime="text/csv"
                )
            
            st.success("✅ Data ready for payroll processing!")
    
    else:
        # Welcome message when no file is uploaded
        st.markdown("""
        ### 👋 Welcome to Timesheet Processor!
        
        This dashboard does exactly what your `Timesheet_Consolidator.ipynb` notebook does:
        
        **🧹 Processes & Cleans**:
        - Handles multiple check-ins/check-outs per employee per date
        - Consolidates duplicate entries into single rows
        
        **📊 Analyzes**:
        - Shows duplicate entry statistics
        - Visualizes shift distributions and performance
        
        **🎯 Applies Business Rules**:
        - Day Shift: 8:00 AM - 17:00 PM (overtime after 17:00 PM)
        - Night Shift: 18:00 PM - 3:00 AM (overtime after 3:00 AM)
        - FIRST check-in → LAST check-out logic
        
        **💾 Creates Clean Data**:
        - Professional Excel and CSV exports
        - Ready for payroll processing
        
        **📁 Upload your timesheet file to get started!**
        """)

if __name__ == "__main__":
    main()