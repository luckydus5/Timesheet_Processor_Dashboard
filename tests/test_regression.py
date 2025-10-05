"""
🔄 REGRESSION TESTS FOR RULE CHANGES
====================================

Comprehensive regression tests to ensure that changes to business rules
don't break existing functionality or introduce unexpected behavior.
"""

import unittest
import pandas as pd
import json
import os
import sys
import tempfile
from datetime import datetime, time, timedelta
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from timesheet_business_rules import TimesheetBusinessRules


class TestBusinessRuleRegression(unittest.TestCase):
    """Regression tests for business rule changes"""
    
    def setUp(self):
        """Set up regression testing environment"""
        self.processor = TimesheetBusinessRules()
        self.temp_dir = tempfile.mkdtemp()
        
        # Known good results from previous versions
        self.baseline_results = self.load_baseline_results()
    
    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def load_baseline_results(self):
        """Load baseline results for regression testing"""
        return {
            "day_shift_scenarios": [
                {
                    "description": "Normal day shift",
                    "start_time": "08:00:00",
                    "end_time": "17:00:00",
                    "expected_total_hours": 9.0,
                    "expected_overtime": 0.0,
                    "expected_shift_type": "Day Shift"
                },
                {
                    "description": "Day shift with 30min overtime",
                    "start_time": "08:00:00",
                    "end_time": "17:30:00",
                    "expected_total_hours": 9.5,
                    "expected_overtime": 0.5,
                    "expected_shift_type": "Day Shift"
                },
                {
                    "description": "Day shift with max overtime",
                    "start_time": "08:00:00",
                    "end_time": "18:30:00",
                    "expected_total_hours": 10.5,
                    "expected_overtime": 1.5,
                    "expected_shift_type": "Day Shift"
                },
                {
                    "description": "Early check-in day shift",
                    "start_time": "07:00:00",
                    "end_time": "17:00:00",
                    "expected_total_hours": 10.0,
                    "expected_overtime": 0.0,
                    "expected_shift_type": "Day Shift"
                },
                {
                    "description": "Below minimum overtime",
                    "start_time": "08:00:00",
                    "end_time": "17:15:00",
                    "expected_total_hours": 9.25,
                    "expected_overtime": 0.0,
                    "expected_shift_type": "Day Shift"
                }
            ],
            "night_shift_scenarios": [
                {
                    "description": "Normal night shift",
                    "start_time": "18:00:00",
                    "end_time": "03:00:00",
                    "expected_total_hours": 9.0,
                    "expected_overtime": 0.0,
                    "expected_shift_type": "Night Shift"
                },
                {
                    "description": "Night shift with 30min overtime",
                    "start_time": "18:00:00",
                    "end_time": "03:30:00",
                    "expected_total_hours": 9.5,
                    "expected_overtime": 0.5,
                    "expected_shift_type": "Night Shift"
                },
                {
                    "description": "Night shift with max overtime",
                    "start_time": "18:00:00",
                    "end_time": "06:00:00",
                    "expected_total_hours": 12.0,
                    "expected_overtime": 3.0,
                    "expected_shift_type": "Night Shift"
                },
                {
                    "description": "Early check-in night shift",
                    "start_time": "17:00:00",
                    "end_time": "03:00:00",
                    "expected_total_hours": 10.0,
                    "expected_overtime": 0.0,
                    "expected_shift_type": "Night Shift"
                }
            ],
            "edge_cases": [
                {
                    "description": "Midnight boundary",
                    "start_time": "23:30:00",
                    "end_time": "00:30:00",
                    "expected_total_hours": 1.0,
                    "expected_overtime": 0.0,
                    "expected_shift_type": "Night Shift"
                },
                {
                    "description": "Very short shift",
                    "start_time": "08:00:00",
                    "end_time": "08:30:00",
                    "expected_total_hours": 0.5,
                    "expected_overtime": 0.0,
                    "expected_shift_type": "Day Shift"
                }
            ]
        }
    
    def test_day_shift_regression(self):
        """Test that day shift calculations remain consistent"""
        print(f"\n🔄 Day Shift Regression Tests")
        
        for scenario in self.baseline_results["day_shift_scenarios"]:
            with self.subTest(scenario=scenario["description"]):
                start_time = datetime.strptime(scenario["start_time"], "%H:%M:%S").time()
                end_time = datetime.strptime(scenario["end_time"], "%H:%M:%S").time()
                
                # Test shift type determination
                shift_type = self.processor.determine_shift_type(start_time)
                self.assertEqual(shift_type, scenario["expected_shift_type"],
                               f"Shift type mismatch for {scenario['description']}")
                
                # Test total hours calculation
                total_hours = self.processor.calculate_total_work_hours(
                    start_time, end_time, shift_type
                )
                self.assertAlmostEqual(total_hours, scenario["expected_total_hours"], places=2,
                                     msg=f"Total hours mismatch for {scenario['description']}")
                
                # Test overtime calculation
                overtime = self.processor.calculate_overtime_hours(
                    start_time, end_time, shift_type
                )
                self.assertAlmostEqual(overtime, scenario["expected_overtime"], places=2,
                                     msg=f"Overtime mismatch for {scenario['description']}")
                
                print(f"✅ {scenario['description']}: {total_hours}h total, {overtime}h OT")
    
    def test_night_shift_regression(self):
        """Test that night shift calculations remain consistent"""
        print(f"\n🌙 Night Shift Regression Tests")
        
        for scenario in self.baseline_results["night_shift_scenarios"]:
            with self.subTest(scenario=scenario["description"]):
                start_time = datetime.strptime(scenario["start_time"], "%H:%M:%S").time()
                end_time = datetime.strptime(scenario["end_time"], "%H:%M:%S").time()
                
                # Test shift type determination
                shift_type = self.processor.determine_shift_type(start_time)
                self.assertEqual(shift_type, scenario["expected_shift_type"],
                               f"Shift type mismatch for {scenario['description']}")
                
                # Test total hours calculation
                total_hours = self.processor.calculate_total_work_hours(
                    start_time, end_time, shift_type
                )
                self.assertAlmostEqual(total_hours, scenario["expected_total_hours"], places=2,
                                     msg=f"Total hours mismatch for {scenario['description']}")
                
                # Test overtime calculation
                overtime = self.processor.calculate_overtime_hours(
                    start_time, end_time, shift_type
                )
                self.assertAlmostEqual(overtime, scenario["expected_overtime"], places=2,
                                     msg=f"Overtime mismatch for {scenario['description']}")
                
                print(f"✅ {scenario['description']}: {total_hours}h total, {overtime}h OT")
    
    def test_edge_cases_regression(self):
        """Test that edge cases remain handled correctly"""
        print(f"\n🎯 Edge Cases Regression Tests")
        
        for scenario in self.baseline_results["edge_cases"]:
            with self.subTest(scenario=scenario["description"]):
                start_time = datetime.strptime(scenario["start_time"], "%H:%M:%S").time()
                end_time = datetime.strptime(scenario["end_time"], "%H:%M:%S").time()
                
                # Test shift type determination
                shift_type = self.processor.determine_shift_type(start_time)
                self.assertEqual(shift_type, scenario["expected_shift_type"],
                               f"Shift type mismatch for {scenario['description']}")
                
                # Test total hours calculation
                total_hours = self.processor.calculate_total_work_hours(
                    start_time, end_time, shift_type
                )
                self.assertAlmostEqual(total_hours, scenario["expected_total_hours"], places=2,
                                     msg=f"Total hours mismatch for {scenario['description']}")
                
                # Test overtime calculation
                overtime = self.processor.calculate_overtime_hours(
                    start_time, end_time, shift_type
                )
                self.assertAlmostEqual(overtime, scenario["expected_overtime"], places=2,
                                     msg=f"Overtime mismatch for {scenario['description']}")
                
                print(f"✅ {scenario['description']}: {total_hours}h total, {overtime}h OT")
    
    def test_business_rule_constants_regression(self):
        """Test that business rule constants haven't changed unexpectedly"""
        print(f"\n📋 Business Rule Constants Regression")
        
        # Expected constants based on original specification
        expected_constants = {
            "DAY_SHIFT_START": time(8, 0, 0),
            "DAY_SHIFT_END": time(17, 0, 0),
            "NIGHT_SHIFT_START": time(18, 0, 0),
            "NIGHT_SHIFT_END": time(3, 0, 0),
            "MIN_OVERTIME_MINUTES": 30,
            "DAY_SHIFT_MAX_OVERTIME_HOURS": 1.5,
            "NIGHT_SHIFT_MAX_OVERTIME_HOURS": 3.0,
        }
        
        for constant_name, expected_value in expected_constants.items():
            actual_value = getattr(self.processor, constant_name)
            self.assertEqual(actual_value, expected_value,
                           f"Constant {constant_name} changed from {expected_value} to {actual_value}")
            print(f"✅ {constant_name}: {actual_value}")
    
    def test_historical_data_processing_regression(self):
        """Test processing of historical data remains consistent"""
        print(f"\n📊 Historical Data Processing Regression")
        
        # Create historical data that should always produce the same results
        historical_data = pd.DataFrame([
            # Employee 1 - Day shift with overtime
            {'Date': '2024-01-01', 'Time': '08:00:00', 'Status': 'C/In', 'Name': 'John Doe'},
            {'Date': '2024-01-01', 'Time': '18:00:00', 'Status': 'C/Out', 'Name': 'John Doe'},
            
            # Employee 2 - Night shift with overtime
            {'Date': '2024-01-01', 'Time': '18:00:00', 'Status': 'OverTime In', 'Name': 'Jane Smith'},
            {'Date': '2024-01-01', 'Time': '06:00:00', 'Status': 'OverTime Out', 'Name': 'Jane Smith'},
            
            # Employee 3 - Normal day shift
            {'Date': '2024-01-02', 'Time': '08:30:00', 'Status': 'C/In', 'Name': 'Bob Johnson'},
            {'Date': '2024-01-02', 'Time': '17:00:00', 'Status': 'C/Out', 'Name': 'Bob Johnson'},
        ])
        
        # Process the data
        historical_data['Time_parsed'] = pd.to_datetime(historical_data['Time']).dt.time
        historical_data['Date_parsed'] = pd.to_datetime(historical_data['Date']).dt.date
        
        # Expected results
        expected_results = {
            'John Doe': {'total_hours': 10.0, 'overtime_hours': 1.0, 'shift_type': 'Day Shift'},
            'Jane Smith': {'total_hours': 12.0, 'overtime_hours': 3.0, 'shift_type': 'Night Shift'},
            'Bob Johnson': {'total_hours': 8.5, 'overtime_hours': 0.0, 'shift_type': 'Day Shift'},
        }
        
        # Process each employee's data
        grouped = historical_data.groupby(['Name', 'Date_parsed'])
        
        for (name, date), group_data in grouped:
            checkin_records = group_data[group_data['Status'].isin(['C/In', 'OverTime In'])]
            checkout_records = group_data[group_data['Status'].isin(['C/Out', 'OverTime Out'])]
            
            if not checkin_records.empty and not checkout_records.empty:
                start_time = checkin_records['Time_parsed'].min()
                end_time = checkout_records['Time_parsed'].max()
                
                shift_type = self.processor.determine_shift_type(start_time)
                total_hours = self.processor.calculate_total_work_hours(
                    start_time, end_time, shift_type
                )
                overtime_hours = self.processor.calculate_overtime_hours(
                    start_time, end_time, shift_type
                )
                
                expected = expected_results[name]
                
                self.assertEqual(shift_type, expected['shift_type'],
                               f"Shift type regression for {name}")
                self.assertAlmostEqual(total_hours, expected['total_hours'], places=1,
                                     msg=f"Total hours regression for {name}")
                self.assertAlmostEqual(overtime_hours, expected['overtime_hours'], places=1,
                                     msg=f"Overtime hours regression for {name}")
                
                print(f"✅ {name}: {shift_type}, {total_hours}h total, {overtime_hours}h OT")
    
    def test_boundary_conditions_regression(self):
        """Test that boundary conditions are handled consistently"""
        print(f"\n🎯 Boundary Conditions Regression")
        
        boundary_tests = [
            # Exact shift boundaries
            {"start": "08:00:00", "end": "17:00:00", "expected_ot": 0.0, "desc": "Exact day shift"},
            {"start": "18:00:00", "end": "03:00:00", "expected_ot": 0.0, "desc": "Exact night shift"},
            
            # Minimum overtime boundaries
            {"start": "08:00:00", "end": "17:30:00", "expected_ot": 0.5, "desc": "Minimum day OT"},
            {"start": "18:00:00", "end": "03:30:00", "expected_ot": 0.5, "desc": "Minimum night OT"},
            
            # Maximum overtime boundaries
            {"start": "08:00:00", "end": "18:30:00", "expected_ot": 1.5, "desc": "Maximum day OT"},
            {"start": "18:00:00", "end": "06:00:00", "expected_ot": 3.0, "desc": "Maximum night OT"},
            
            # Just below minimum
            {"start": "08:00:00", "end": "17:29:00", "expected_ot": 0.0, "desc": "Below min day OT"},
            {"start": "18:00:00", "end": "03:29:00", "expected_ot": 0.0, "desc": "Below min night OT"},
        ]
        
        for test in boundary_tests:
            with self.subTest(test=test["desc"]):
                start_time = datetime.strptime(test["start"], "%H:%M:%S").time()
                end_time = datetime.strptime(test["end"], "%H:%M:%S").time()
                
                shift_type = self.processor.determine_shift_type(start_time)
                overtime = self.processor.calculate_overtime_hours(
                    start_time, end_time, shift_type
                )
                
                self.assertAlmostEqual(overtime, test["expected_ot"], places=2,
                                     msg=f"Boundary condition regression: {test['desc']}")
                
                print(f"✅ {test['desc']}: {overtime}h OT (expected {test['expected_ot']})")
    
    def test_data_type_consistency_regression(self):
        """Test that data types returned by functions remain consistent"""
        print(f"\n🔍 Data Type Consistency Regression")
        
        start_time = time(8, 0, 0)
        end_time = time(17, 30, 0)
        shift_type = "Day Shift"
        
        # Test return types
        shift_result = self.processor.determine_shift_type(start_time)
        self.assertIsInstance(shift_result, str, "Shift type should be string")
        
        total_hours_result = self.processor.calculate_total_work_hours(
            start_time, end_time, shift_type
        )
        self.assertIsInstance(total_hours_result, (int, float), "Total hours should be numeric")
        
        overtime_result = self.processor.calculate_overtime_hours(
            start_time, end_time, shift_type
        )
        self.assertIsInstance(overtime_result, (int, float), "Overtime should be numeric")
        
        # Test that numbers are non-negative
        self.assertGreaterEqual(total_hours_result, 0, "Total hours should be non-negative")
        self.assertGreaterEqual(overtime_result, 0, "Overtime should be non-negative")
        
        print(f"✅ Shift type: {type(shift_result).__name__}")
        print(f"✅ Total hours: {type(total_hours_result).__name__}")
        print(f"✅ Overtime: {type(overtime_result).__name__}")
    
    def test_save_regression_baseline(self):
        """Save current results as baseline for future regression testing"""
        # This test generates new baseline data
        # Uncomment and run when you want to update baselines
        
        baseline_file = os.path.join(self.temp_dir, "regression_baseline.json")
        
        current_results = {}
        
        # Generate current results for all test scenarios
        for category_name, scenarios in self.baseline_results.items():
            current_results[category_name] = []
            
            for scenario in scenarios:
                start_time = datetime.strptime(scenario["start_time"], "%H:%M:%S").time()
                end_time = datetime.strptime(scenario["end_time"], "%H:%M:%S").time()
                
                shift_type = self.processor.determine_shift_type(start_time)
                total_hours = self.processor.calculate_total_work_hours(
                    start_time, end_time, shift_type
                )
                overtime = self.processor.calculate_overtime_hours(
                    start_time, end_time, shift_type
                )
                
                current_results[category_name].append({
                    "description": scenario["description"],
                    "start_time": scenario["start_time"],
                    "end_time": scenario["end_time"],
                    "actual_total_hours": total_hours,
                    "actual_overtime": overtime,
                    "actual_shift_type": shift_type
                })
        
        # Save to file for manual review
        with open(baseline_file, 'w') as f:
            json.dump(current_results, f, indent=2, default=str)
        
        print(f"✅ Baseline saved to {baseline_file}")


if __name__ == '__main__':
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add regression tests
    suite.addTest(unittest.makeSuite(TestBusinessRuleRegression))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"🔄 REGRESSION TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print(f"✅ ALL REGRESSION TESTS PASSED!")
        print(f"✅ No regressions detected - business rules are stable")
    else:
        print(f"❌ REGRESSION DETECTED!")
        print(f"⚠️  Business rule changes may have broken existing functionality")
        
        # Print detailed failure information
        if result.failures:
            print(f"\n💥 FAILURES:")
            for test, traceback in result.failures:
                print(f"- {test}")
                print(f"  {traceback}")
        
        if result.errors:
            print(f"\n💥 ERRORS:")
            for test, traceback in result.errors:
                print(f"- {test}")
                print(f"  {traceback}")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)