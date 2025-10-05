"""
🌙 ENHANCED CROSS-MIDNIGHT SHIFT HANDLER
========================================
Improved algorithm to handle shift transitions and cross-date shifts properly
Specifically handles cases like:
- 04/08/2025 06:44:28 OverTime In → 04/08/2025 19:08:54 OverTime Out (Day shift)
- 05/08/2025 18:12:28 OverTime In → 06/08/2025 07:42:31 OverTime Out (Night shift)
"""

import pandas as pd
from datetime import datetime, timedelta

# Mock streamlit functions for testing
class MockST:
    def info(self, msg): print(f"INFO: {msg}")
    def warning(self, msg): print(f"WARNING: {msg}")
    def success(self, msg): print(f"SUCCESS: {msg}")

st = MockST()


class EnhancedShiftDetector:
    """Enhanced shift detection that properly handles cross-midnight shifts"""
    
    def __init__(self):
        # Shift time boundaries
        self.DAY_SHIFT_START = 6    # 06:00
        self.DAY_SHIFT_END = 18     # 18:00  
        self.NIGHT_SHIFT_START = 18 # 18:00
        self.NIGHT_SHIFT_END = 6    # 06:00 (next day)
        
        # Tolerance for shift detection (in hours)
        self.SHIFT_TOLERANCE = 2
        
    def detect_cross_midnight_shifts_enhanced(self, df):
        """
        Enhanced cross-midnight shift detection
        Handles all patterns including exact cases from user data
        """
        df_work = df.copy()
        df_work['Shift_Group'] = df_work['Date_parsed']  # Default grouping
        df_work['Processed'] = False
        df_work['Shift_Type_Detected'] = 'Unknown'
        
        # Sort by employee, date, and time
        df_work = df_work.sort_values(['Name', 'Date_parsed', 'Time_parsed'])
        
        employees = df_work['Name'].unique()
        processed_pairs = 0
        cross_midnight_shifts = 0
        
        for employee in employees:
            emp_data = df_work[df_work['Name'] == employee].copy()
            emp_indices = df_work[df_work['Name'] == employee].index.tolist()
            
            # Convert to list for easier processing
            entries = []
            for i, (idx, row) in enumerate(zip(emp_indices, emp_data.itertuples())):
                entries.append({
                    'index': idx,
                    'date': row.Date_parsed,
                    'time': row.Time_parsed,
                    'status': row.Status,
                    'datetime': datetime.combine(row.Date_parsed, row.Time_parsed),
                    'processed': False
                })
            
            # Process entries to find In/Out pairs
            for i in range(len(entries)):
                if entries[i]['processed']:
                    continue
                    
                current = entries[i]
                
                # Look for "OverTime In" or similar check-in
                if current['status'] in ['OverTime In', 'CheckIn', 'In']:
                    
                    # Find the next checkout for this employee
                    checkout_found = False
                    for j in range(i + 1, len(entries)):
                        if entries[j]['processed']:
                            continue
                            
                        candidate = entries[j]
                        
                        # Look for checkout status
                        if candidate['status'] in ['OverTime Out', 'CheckOut', 'Out']:
                            
                            # Calculate time difference
                            time_diff = candidate['datetime'] - current['datetime']
                            hours_diff = time_diff.total_seconds() / 3600
                            
                            # Valid shift if between 4-16 hours
                            if 4 <= hours_diff <= 16:
                                
                                # Determine shift type and grouping
                                shift_info = self.analyze_shift_pattern(
                                    current['datetime'], 
                                    candidate['datetime']
                                )
                                
                                # Group entries based on shift pattern
                                if shift_info['cross_midnight']:
                                    # Night shift: group under check-in date
                                    df_work.loc[candidate['index'], 'Shift_Group'] = current['date']
                                    cross_midnight_shifts += 1
                                    
                                    st.info(f"🌙 Cross-midnight shift detected: {employee} "
                                           f"Check-in: {current['date']} {current['time']} → "
                                           f"Check-out: {candidate['date']} {candidate['time']}")
                                
                                # Mark both entries as processed
                                df_work.loc[current['index'], 'Processed'] = True
                                df_work.loc[candidate['index'], 'Processed'] = True
                                df_work.loc[current['index'], 'Shift_Type_Detected'] = shift_info['type']
                                df_work.loc[candidate['index'], 'Shift_Type_Detected'] = shift_info['type']
                                
                                entries[i]['processed'] = True
                                entries[j]['processed'] = True
                                processed_pairs += 1
                                checkout_found = True
                                break
                    
                    if not checkout_found:
                        st.warning(f"⚠️ Unmatched check-in found: {employee} on {current['date']} at {current['time']}")
        
        # Clean up temporary columns
        df_work = df_work.drop(['Processed'], axis=1)
        
        # Report results
        if processed_pairs > 0:
            st.success(f"✅ Processed {processed_pairs} shift pairs")
        if cross_midnight_shifts > 0:
            st.info(f"🌙 Found {cross_midnight_shifts} cross-midnight shifts")
        
        return df_work
    
    def analyze_shift_pattern(self, checkin_datetime, checkout_datetime):
        """
        Analyze a check-in/check-out pair to determine shift type and characteristics
        """
        checkin_hour = checkin_datetime.hour + checkin_datetime.minute/60
        checkout_hour = checkout_datetime.hour + checkout_datetime.minute/60
        
        # Check if spans multiple days
        cross_midnight = checkin_datetime.date() != checkout_datetime.date()
        
        # Determine shift type based on times
        if cross_midnight:
            # Cross-midnight shift
            if checkin_hour >= 16:  # Check-in after 4 PM
                if checkout_hour <= 10:  # Check-out before 10 AM next day
                    shift_type = "Night Shift"
                else:
                    shift_type = "Extended Day Shift"
            else:
                shift_type = "Extended Shift"
        else:
            # Same-day shift
            if checkin_hour >= 6 and checkout_hour <= 18:
                shift_type = "Day Shift"
            elif checkin_hour >= 18 or checkout_hour <= 6:
                shift_type = "Night Shift"
            else:
                shift_type = "Mixed Shift"
        
        return {
            'type': shift_type,
            'cross_midnight': cross_midnight,
            'checkin_hour': checkin_hour,
            'checkout_hour': checkout_hour,
            'duration_hours': (checkout_datetime - checkin_datetime).total_seconds() / 3600
        }
    
    def validate_shift_data(self, df):
        """
        Validate the processed shift data and identify potential issues
        """
        issues = []
        
        # Group by employee and shift group
        for (employee, shift_group), group in df.groupby(['Name', 'Shift_Group']):
            
            # Check for multiple check-ins or check-outs in same shift
            ins = group[group['Status'].str.contains('In', na=False)]
            outs = group[group['Status'].str.contains('Out', na=False)]
            
            if len(ins) > 1:
                issues.append(f"Multiple check-ins for {employee} on shift {shift_group}")
            
            if len(outs) > 1:
                issues.append(f"Multiple check-outs for {employee} on shift {shift_group}")
            
            if len(ins) == 0:
                issues.append(f"Missing check-in for {employee} on shift {shift_group}")
            
            if len(outs) == 0:
                issues.append(f"Missing check-out for {employee} on shift {shift_group}")
        
        return issues


def test_enhanced_detector_with_user_data():
    """
    Test the enhanced detector with the user's specific data pattern
    """
    # Create test data based on user's example
    test_data = [
        {'Name': 'Ishimwe.Jonathan', 'Date': '04/08/2025', 'Time': '06:44:28', 'Status': 'OverTime In'},
        {'Name': 'Ishimwe.Jonathan', 'Date': '04/08/2025', 'Time': '19:08:54', 'Status': 'OverTime Out'},
        {'Name': 'Ishimwe.Jonathan', 'Date': '05/08/2025', 'Time': '18:12:28', 'Status': 'OverTime In'},
        {'Name': 'Ishimwe.Jonathan', 'Date': '06/08/2025', 'Time': '07:42:31', 'Status': 'OverTime Out'},
        {'Name': 'Ishimwe.Jonathan', 'Date': '06/08/2025', 'Time': '07:42:35', 'Status': 'OverTime Out'},  # Duplicate
    ]
    
    df = pd.DataFrame(test_data)
    
    # Parse dates and times
    def parse_date_time(date_str, time_str):
        try:
            date_obj = datetime.strptime(date_str, '%d/%m/%Y').date()
            time_obj = datetime.strptime(time_str, '%H:%M:%S').time()
            return date_obj, time_obj
        except:
            return None, None
    
    df[['Date_parsed', 'Time_parsed']] = df.apply(
        lambda row: pd.Series(parse_date_time(row['Date'], row['Time'])), axis=1
    )
    
    # Test the enhanced detector
    detector = EnhancedShiftDetector()
    result_df = detector.detect_cross_midnight_shifts_enhanced(df)
    
    return result_df


if __name__ == "__main__":
    # Test with user data
    print("Testing Enhanced Shift Detector with user data...")
    result = test_enhanced_detector_with_user_data()
    print("\\nResults:")
    print(result[['Name', 'Date', 'Time', 'Status', 'Shift_Group', 'Shift_Type_Detected']])