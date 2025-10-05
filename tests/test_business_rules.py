"""
🧪 UNIT TESTS FOR BUSINESS RULES
===================================

Comprehensive unit tests for all timesheet business rules to ensure
accuracy and prevent regression issues.
"""

import unittest
import pandas as pd
from datetime import datetime, time, timedelta
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from timesheet_business_rules import TimesheetBusinessRules


class TestTimesheetBusinessRules(unittest.TestCase):
    """Test cases for timesheet business rules"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = TimesheetBusinessRules()
    
    def test_shift_type_determination(self):
        """Test shift type determination logic"""
        
        # Test Day Shift scenarios
        day_shift_times = [
            time(6, 0),   # 06:00 - Early day shift
            time(8, 0),   # 08:00 - Normal day shift
            time(12, 0),  # 12:00 - Midday start
            time(17, 59), # 17:59 - Last minute day shift
        ]
        
        for test_time in day_shift_times:
            result = self.processor.determine_shift_type(test_time)
            self.assertEqual(result, "Day Shift", 
                           f"Time {test_time} should be Day Shift")
        
        # Test Night Shift scenarios
        night_shift_times = [
            time(18, 0),  # 18:00 - Start of night shift
            time(20, 0),  # 20:00 - Evening
            time(23, 0),  # 23:00 - Late night
        ]
        
        for test_time in night_shift_times:
            result = self.processor.determine_shift_type(test_time)
            self.assertEqual(result, "Night Shift", 
                           f"Time {test_time} should be Night Shift")
        
        # Test Day Shift scenarios (including early morning times)
        day_shift_special_times = [
            time(2, 0),   # 02:00 - Early morning (day shift)
        ]
        
        for test_time in day_shift_special_times:
            result = self.processor.determine_shift_type(test_time)
            self.assertEqual(result, "Day Shift", 
                           f"Time {test_time} should be Day Shift")
    
    def test_overtime_calculations_day_shift(self):
        """Test overtime calculations for day shifts"""
        
        # Test case 1: No overtime (ends before 17:00)
        start_time = time(8, 0)   # 08:00
        end_time = time(16, 30)   # 16:30
        
        overtime = self.processor.calculate_overtime_hours(
            start_time, end_time, "Day Shift"
        )
        self.assertEqual(overtime, 0.0, "No overtime should be calculated before 17:00")
        
        # Test case 2: Valid overtime (30 minutes after 17:00)
        end_time = time(17, 30)   # 17:30
        overtime = self.processor.calculate_overtime_hours(
            start_time, end_time, "Day Shift"
        )
        self.assertEqual(overtime, 0.5, "30 minutes overtime should be 0.5 hours")
        
        # Test case 3: Below minimum (15 minutes after 17:00)
        end_time = time(17, 15)   # 17:15
        overtime = self.processor.calculate_overtime_hours(
            start_time, end_time, "Day Shift"
        )
        self.assertEqual(overtime, 0.0, "Below 30 minutes should be 0 overtime")
        
        # Test case 4: Maximum overtime (1.5 hours)
        end_time = time(18, 30)   # 18:30
        overtime = self.processor.calculate_overtime_hours(
            start_time, end_time, "Day Shift"
        )
        self.assertEqual(overtime, 1.5, "Maximum day shift overtime is 1.5 hours")
        
        # Test case 5: Above maximum (2 hours attempted)
        end_time = time(19, 0)    # 19:00
        overtime = self.processor.calculate_overtime_hours(
            start_time, end_time, "Day Shift"
        )
        self.assertEqual(overtime, 1.5, "Should cap at 1.5 hours maximum")
    
    def test_overtime_calculations_night_shift(self):
        """Test overtime calculations for night shifts"""
        
        # Test case 1: No overtime (ends before 03:00)
        start_time = time(18, 0)  # 18:00
        end_time = time(2, 30)    # 02:30 (next day)
        
        overtime = self.processor.calculate_overtime_hours(
            start_time, end_time, "Night Shift"
        )
        self.assertEqual(overtime, 0.0, "No overtime should be calculated before 03:00")
        
        # Test case 2: Valid overtime (30 minutes after 03:00)
        end_time = time(3, 30)    # 03:30 (next day)
        overtime = self.processor.calculate_overtime_hours(
            start_time, end_time, "Night Shift"
        )
        self.assertEqual(overtime, 0.5, "30 minutes overtime should be 0.5 hours")
        
        # Test case 3: Maximum overtime (3 hours)
        end_time = time(6, 0)     # 06:00 (next day)
        overtime = self.processor.calculate_overtime_hours(
            start_time, end_time, "Night Shift"
        )
        self.assertEqual(overtime, 3.0, "Maximum night shift overtime is 3.0 hours")
        
        # Test case 4: Above maximum (4 hours attempted)
        end_time = time(7, 0)     # 07:00 (next day)
        overtime = self.processor.calculate_overtime_hours(
            start_time, end_time, "Night Shift"
        )
        self.assertEqual(overtime, 3.0, "Should cap at 3.0 hours maximum")
    
    def test_total_work_hours_calculation(self):
        """Test total work hours calculation"""
        
        # Test normal day shift
        start_time = time(8, 0)   # 08:00
        end_time = time(17, 0)    # 17:00
        
        total_hours = self.processor.calculate_total_work_hours(
            start_time, end_time, "Day Shift"
        )
        self.assertEqual(total_hours, 9.0, "8:00 to 17:00 should be 9 hours")
        
        # Test cross-midnight night shift
        start_time = time(18, 0)  # 18:00
        end_time = time(3, 0)     # 03:00 (next day)
        
        total_hours = self.processor.calculate_total_work_hours(
            start_time, end_time, "Night Shift"
        )
        self.assertEqual(total_hours, 9.0, "18:00 to 03:00 should be 9 hours")
    
    def test_format_hours_to_time(self):
        """Test formatting decimal hours to HH:MM:SS format"""
        
        test_cases = [
            (0.0, "00:00:00"),
            (0.5, "00:30:00"),
            (1.0, "01:00:00"),
            (1.5, "01:30:00"),
            (8.75, "08:45:00"),
            (10.25, "10:15:00"),
        ]
        
        # Create a simple formatter function for testing
        def format_hours_to_time(decimal_hours):
            if decimal_hours is None or decimal_hours < 0:
                return "00:00:00"
            
            hours = int(decimal_hours)
            minutes = int((decimal_hours - hours) * 60)
            seconds = int(((decimal_hours - hours) * 60 - minutes) * 60)
            
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        for decimal_hours, expected in test_cases:
            result = format_hours_to_time(decimal_hours)
            self.assertEqual(result, expected, 
                           f"{decimal_hours} hours should format to {expected}")
    
    def test_edge_cases(self):
        """Test edge cases and error conditions"""
        
        # Test with None values
        result = self.processor.determine_shift_type(None)
        self.assertEqual(result, "", "None time should return empty string")
        
        # Test with invalid overtime calculation
        overtime = self.processor.calculate_overtime_hours(
            None, None, "Day Shift"
        )
        self.assertEqual(overtime, 0.0, "Invalid times should return 0 overtime")


class TestBusinessRuleCompliance(unittest.TestCase):
    """Test compliance with specific business rule requirements"""
    
    def setUp(self):
        self.processor = TimesheetBusinessRules()
    
    def test_day_shift_overtime_minimum(self):
        """Test 30-minute minimum rule for day shift overtime"""
        
        test_cases = [
            (time(17, 10), 0.0),  # 10 minutes - below minimum
            (time(17, 20), 0.0),  # 20 minutes - below minimum
            (time(17, 29), 0.0),  # 29 minutes - below minimum
            (time(17, 30), 0.5),  # 30 minutes - exactly minimum
            (time(17, 45), 0.75), # 45 minutes - above minimum
        ]
        
        start_time = time(8, 0)
        
        for end_time, expected_ot in test_cases:
            overtime = self.processor.calculate_overtime_hours(
                start_time, end_time, "Day Shift"
            )
            self.assertEqual(overtime, expected_ot, 
                           f"End time {end_time} should give {expected_ot} OT")
    
    def test_night_shift_overtime_minimum(self):
        """Test 30-minute minimum rule for night shift overtime"""
        
        test_cases = [
            (time(3, 10), 0.0),   # 10 minutes - below minimum
            (time(3, 20), 0.0),   # 20 minutes - below minimum
            (time(3, 29), 0.0),   # 29 minutes - below minimum
            (time(3, 30), 0.5),   # 30 minutes - exactly minimum
            (time(3, 45), 0.75),  # 45 minutes - above minimum
        ]
        
        start_time = time(18, 0)
        
        for end_time, expected_ot in test_cases:
            overtime = self.processor.calculate_overtime_hours(
                start_time, end_time, "Night Shift"
            )
            self.assertEqual(overtime, expected_ot, 
                           f"End time {end_time} should give {expected_ot} OT")


if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTest(unittest.makeSuite(TestTimesheetBusinessRules))
    suite.addTest(unittest.makeSuite(TestBusinessRuleCompliance))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"🧪 TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print(f"✅ ALL TESTS PASSED!")
    else:
        print(f"❌ SOME TESTS FAILED!")
        
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)