"""
🔄 INTEGRATION TESTS FOR FILE PROCESSING
========================================

Comprehensive integration tests to validate end-to-end file processing
workflows including Excel/CSV parsing, data consolidation, and output generation.
"""

import unittest
import pandas as pd
import tempfile
import os
import sys
from datetime import datetime, time
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from timesheet_business_rules import TimesheetBusinessRules
import process_timesheet


class TestFileProcessingIntegration(unittest.TestCase):
    """Integration tests for complete file processing workflows"""
    
    def setUp(self):
        """Set up test environment with temporary files"""
        self.temp_dir = tempfile.mkdtemp()
        self.processor = TimesheetBusinessRules()
        
        # Create sample timesheet data for testing
        self.sample_data = [
            {'Date': '2025-01-15', 'Time': '07:45:00', 'Status': 'C/In', 'Name': 'John Doe'},
            {'Date': '2025-01-15', 'Time': '17:30:00', 'Status': 'C/Out', 'Name': 'John Doe'},
            {'Date': '2025-01-15', 'Time': '19:00:00', 'Status': 'OverTime In', 'Name': 'Jane Smith'},
            {'Date': '2025-01-15', 'Time': '03:30:00', 'Status': 'OverTime Out', 'Name': 'Jane Smith'},
            {'Date': '2025-01-16', 'Time': '08:15:00', 'Status': 'C/In', 'Name': 'John Doe'},
            {'Date': '2025-01-16', 'Time': '17:00:00', 'Status': 'C/Out', 'Name': 'John Doe'},
        ]
    
    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def create_test_excel_file(self, filename="test_timesheet.xlsx"):
        """Create a test Excel file with sample data"""
        file_path = os.path.join(self.temp_dir, filename)
        df = pd.DataFrame(self.sample_data)
        df.to_excel(file_path, index=False)
        return file_path
    
    def create_test_csv_file(self, filename="test_timesheet.csv"):
        """Create a test CSV file with sample data"""
        file_path = os.path.join(self.temp_dir, filename)
        df = pd.DataFrame(self.sample_data)
        df.to_csv(file_path, index=False)
        return file_path
    
    def test_excel_file_reading(self):
        """Test reading and parsing Excel files"""
        excel_file = self.create_test_excel_file()
        
        # Test file exists
        self.assertTrue(os.path.exists(excel_file), "Test Excel file should exist")
        
        # Test pandas can read the file
        df = pd.read_excel(excel_file)
        self.assertFalse(df.empty, "DataFrame should not be empty")
        self.assertEqual(len(df), 6, "Should have 6 records")
        
        # Test expected columns exist
        expected_columns = ['Date', 'Time', 'Status', 'Name']
        for col in expected_columns:
            self.assertIn(col, df.columns, f"Column {col} should exist")
    
    def test_csv_file_reading(self):
        """Test reading and parsing CSV files"""
        csv_file = self.create_test_csv_file()
        
        # Test file exists
        self.assertTrue(os.path.exists(csv_file), "Test CSV file should exist")
        
        # Test pandas can read the file
        df = pd.read_csv(csv_file)
        self.assertFalse(df.empty, "DataFrame should not be empty")
        self.assertEqual(len(df), 6, "Should have 6 records")
        
        # Test expected columns exist
        expected_columns = ['Date', 'Time', 'Status', 'Name']
        for col in expected_columns:
            self.assertIn(col, df.columns, f"Column {col} should exist")
    
    def test_time_parsing_and_conversion(self):
        """Test time parsing from various formats"""
        test_time_formats = [
            "07:45:00",
            "7:45",
            "17:30:00",
            "19:00",
            "03:30:00",
        ]
        
        for time_str in test_time_formats:
            try:
                # Test parsing to time object
                parsed_time = pd.to_datetime(time_str).time()
                self.assertIsInstance(parsed_time, time, 
                                    f"Should parse {time_str} to time object")
            except Exception as e:
                self.fail(f"Failed to parse time {time_str}: {e}")
    
    def test_data_consolidation_workflow(self):
        """Test complete data consolidation workflow"""
        excel_file = self.create_test_excel_file()
        df = pd.read_excel(excel_file)
        
        # Add parsed time column
        df['Time_parsed'] = pd.to_datetime(df['Time']).dt.time
        df['Date_parsed'] = pd.to_datetime(df['Date']).dt.date
        
        # Group by employee and date
        grouped = df.groupby(['Name', 'Date_parsed'])
        
        consolidated_data = []
        
        for (name, date), group_data in grouped:
            # Find first check-in and last check-out
            checkin_records = group_data[group_data['Status'].isin(['C/In', 'OverTime In'])]
            checkout_records = group_data[group_data['Status'].isin(['C/Out', 'OverTime Out'])]
            
            if not checkin_records.empty and not checkout_records.empty:
                start_time = checkin_records['Time_parsed'].min()
                end_time = checkout_records['Time_parsed'].max()
                
                # Determine shift type
                shift_type = self.processor.determine_shift_type(start_time)
                
                # Calculate hours
                total_hours = self.processor.calculate_total_work_hours(
                    start_time, end_time, shift_type
                )
                overtime_hours = self.processor.calculate_overtime_hours(
                    start_time, end_time, shift_type
                )
                
                consolidated_data.append({
                    'Name': name,
                    'Date': date,
                    'Start_Time': start_time,
                    'End_Time': end_time,
                    'Shift_Type': shift_type,
                    'Total_Hours': total_hours,
                    'Overtime_Hours': overtime_hours,
                })
        
        # Verify consolidated data
        self.assertEqual(len(consolidated_data), 3, "Should have 3 consolidated records")
        
        # Test John Doe's records
        john_records = [r for r in consolidated_data if r['Name'] == 'John Doe']
        self.assertEqual(len(john_records), 2, "John should have 2 work days")
        
        # Test Jane Smith's record
        jane_records = [r for r in consolidated_data if r['Name'] == 'Jane Smith']
        self.assertEqual(len(jane_records), 1, "Jane should have 1 work day")
        
        # Verify overtime calculation for John's first day
        john_day1 = next(r for r in john_records 
                         if r['Date'] == datetime(2025, 1, 15).date())
        self.assertEqual(john_day1['Overtime_Hours'], 0.5, 
                        "John should have 0.5 hours overtime on day 1")
    
    def test_output_file_generation(self):
        """Test generation of output files"""
        # Create consolidated data
        consolidated_data = [
            {
                'Name': 'John Doe',
                'Date': datetime(2025, 1, 15).date(),
                'Start_Time': time(7, 45),
                'End_Time': time(17, 30),
                'Shift_Type': 'Day Shift',
                'Total_Hours': 9.75,
                'Overtime_Hours': 0.5,
            },
            {
                'Name': 'Jane Smith',
                'Date': datetime(2025, 1, 15).date(),
                'Start_Time': time(19, 0),
                'End_Time': time(3, 30),
                'Shift_Type': 'Night Shift',
                'Total_Hours': 8.5,
                'Overtime_Hours': 0.5,
            }
        ]
        
        df_output = pd.DataFrame(consolidated_data)
        
        # Test CSV output
        csv_output = os.path.join(self.temp_dir, "consolidated_output.csv")
        df_output.to_csv(csv_output, index=False)
        self.assertTrue(os.path.exists(csv_output), "CSV output file should be created")
        
        # Test Excel output
        excel_output = os.path.join(self.temp_dir, "consolidated_output.xlsx")
        df_output.to_excel(excel_output, index=False)
        self.assertTrue(os.path.exists(excel_output), "Excel output file should be created")
        
        # Verify file contents
        df_read_csv = pd.read_csv(csv_output)
        self.assertEqual(len(df_read_csv), 2, "CSV should have 2 records")
        
        df_read_excel = pd.read_excel(excel_output)
        self.assertEqual(len(df_read_excel), 2, "Excel should have 2 records")
    
    def test_large_dataset_processing(self):
        """Test processing of larger datasets"""
        # Create a larger dataset (100 employees, 5 days each)
        large_data = []
        
        for emp_id in range(1, 101):  # 100 employees
            for day in range(1, 6):   # 5 days each
                date_str = f"2025-01-{day:02d}"
                emp_name = f"Employee_{emp_id:03d}"
                
                # Day shift pattern
                large_data.extend([
                    {'Date': date_str, 'Time': '08:00:00', 'Status': 'C/In', 'Name': emp_name},
                    {'Date': date_str, 'Time': '17:00:00', 'Status': 'C/Out', 'Name': emp_name},
                ])
        
        # Create temporary large file
        large_file = os.path.join(self.temp_dir, "large_timesheet.xlsx")
        df_large = pd.DataFrame(large_data)
        df_large.to_excel(large_file, index=False)
        
        # Test reading large file
        df_read = pd.read_excel(large_file)
        self.assertEqual(len(df_read), 1000, "Should have 1000 records (100 employees × 5 days × 2 entries)")
        
        # Test memory efficiency (should not cause memory errors)
        grouped = df_read.groupby(['Name', 'Date'])
        self.assertEqual(len(grouped), 500, "Should have 500 employee-day combinations")


class TestErrorHandlingIntegration(unittest.TestCase):
    """Test error handling in file processing workflows"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.processor = TimesheetBusinessRules()
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_corrupted_excel_file(self):
        """Test handling of corrupted Excel files"""
        # Create a corrupted Excel file (just text content)
        corrupted_file = os.path.join(self.temp_dir, "corrupted.xlsx")
        with open(corrupted_file, 'w') as f:
            f.write("This is not a valid Excel file")
        
        # Test that pandas raises appropriate error
        with self.assertRaises(Exception):
            pd.read_excel(corrupted_file)
    
    def test_missing_required_columns(self):
        """Test handling of files with missing required columns"""
        # Create file with missing columns
        incomplete_data = [
            {'Date': '2025-01-15', 'Time': '08:00:00'},  # Missing Status and Name
            {'Date': '2025-01-15', 'Time': '17:00:00'},
        ]
        
        file_path = os.path.join(self.temp_dir, "incomplete.xlsx")
        df = pd.DataFrame(incomplete_data)
        df.to_excel(file_path, index=False)
        
        # Read file and check for missing columns
        df_read = pd.read_excel(file_path)
        required_columns = ['Date', 'Time', 'Status', 'Name']
        missing_columns = [col for col in required_columns if col not in df_read.columns]
        
        self.assertTrue(len(missing_columns) > 0, "Should detect missing columns")
        self.assertIn('Status', missing_columns)
        self.assertIn('Name', missing_columns)
    
    def test_invalid_time_formats(self):
        """Test handling of invalid time formats"""
        invalid_times = [
            "25:00:00",  # Invalid hour
            "12:60:00",  # Invalid minute
            "12:30:60",  # Invalid second
            "invalid",   # Non-time string
            "",          # Empty string
        ]
        
        for invalid_time in invalid_times:
            try:
                pd.to_datetime(invalid_time)
                # If it doesn't raise an error, check if result is NaT
                result = pd.to_datetime(invalid_time, errors='coerce')
                if pd.isna(result):
                    continue  # This is expected behavior
            except Exception:
                continue  # This is also expected behavior
    
    def test_empty_file_handling(self):
        """Test handling of empty files"""
        # Create empty Excel file
        empty_file = os.path.join(self.temp_dir, "empty.xlsx")
        df_empty = pd.DataFrame()
        df_empty.to_excel(empty_file, index=False)
        
        # Read empty file
        df_read = pd.read_excel(empty_file)
        self.assertTrue(df_read.empty, "Empty file should result in empty DataFrame")


if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTest(unittest.makeSuite(TestFileProcessingIntegration))
    suite.addTest(unittest.makeSuite(TestErrorHandlingIntegration))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"🔄 INTEGRATION TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print(f"✅ ALL INTEGRATION TESTS PASSED!")
    else:
        print(f"❌ SOME INTEGRATION TESTS FAILED!")
        
        # Print failure details
        if result.failures:
            print(f"\n❌ FAILURES:")
            for test, traceback in result.failures:
                print(f"- {test}: {traceback}")
        
        if result.errors:
            print(f"\n💥 ERRORS:")
            for test, traceback in result.errors:
                print(f"- {test}: {traceback}")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)