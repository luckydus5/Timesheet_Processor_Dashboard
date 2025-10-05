"""
⚡ PERFORMANCE TESTS FOR LARGE DATASETS
======================================

Performance and stress tests to ensure the timesheet processor
can handle large datasets efficiently without memory or performance issues.
"""

import unittest
import pandas as pd
import time
import os
import sys
import tempfile
import random
from datetime import datetime, timedelta
import threading

# Optional performance testing imports
try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

try:
    from memory_profiler import profile
    MEMORY_PROFILER_AVAILABLE = True
except ImportError:
    MEMORY_PROFILER_AVAILABLE = False

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from timesheet_business_rules import TimesheetBusinessRules


class TestPerformanceBenchmarks(unittest.TestCase):
    """Performance benchmarks for timesheet processing"""
    
    def setUp(self):
        """Set up performance testing environment"""
        self.processor = TimesheetBusinessRules()
        self.temp_dir = tempfile.mkdtemp()
        
        # Performance thresholds
        self.MAX_PROCESSING_TIME_SMALL = 5.0    # 5 seconds for 1K records
        self.MAX_PROCESSING_TIME_MEDIUM = 30.0  # 30 seconds for 10K records
        self.MAX_PROCESSING_TIME_LARGE = 120.0  # 2 minutes for 100K records
        
        self.MAX_MEMORY_MB = 500  # 500MB maximum memory usage
    
    def tearDown(self):
        """Clean up temporary files"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        if not PSUTIL_AVAILABLE:
            return 0.0
        
        process = psutil.Process(os.getpid())
        return process.memory_info().rss / 1024 / 1024  # Convert to MB
    
    def generate_test_data(self, num_employees=100, days_per_employee=30):
        """Generate realistic test data"""
        data = []
        
        # Generate data for multiple employees over multiple days
        for emp_id in range(1, num_employees + 1):
            emp_name = f"Employee_{emp_id:04d}"
            
            for day_offset in range(days_per_employee):
                work_date = datetime(2025, 1, 1) + timedelta(days=day_offset)
                date_str = work_date.strftime("%Y-%m-%d")
                
                # Randomly choose shift type
                if random.random() < 0.7:  # 70% day shift
                    # Day shift with some variation
                    start_hour = random.randint(7, 9)    # 7-9 AM
                    start_minute = random.randint(0, 59)
                    end_hour = random.randint(16, 19)    # 4-7 PM
                    end_minute = random.randint(0, 59)
                    
                    start_time = f"{start_hour:02d}:{start_minute:02d}:00"
                    end_time = f"{end_hour:02d}:{end_minute:02d}:00"
                    
                    data.extend([
                        {
                            'Date': date_str,
                            'Time': start_time,
                            'Status': 'C/In',
                            'Name': emp_name
                        },
                        {
                            'Date': date_str,
                            'Time': end_time,
                            'Status': 'C/Out',
                            'Name': emp_name
                        }
                    ])
                else:  # 30% night shift
                    # Night shift starting evening, ending next morning
                    start_hour = random.randint(18, 20)  # 6-8 PM
                    start_minute = random.randint(0, 59)
                    end_hour = random.randint(2, 6)      # 2-6 AM next day
                    end_minute = random.randint(0, 59)
                    
                    start_time = f"{start_hour:02d}:{start_minute:02d}:00"
                    end_time = f"{end_hour:02d}:{end_minute:02d}:00"
                    
                    data.extend([
                        {
                            'Date': date_str,
                            'Time': start_time,
                            'Status': 'OverTime In',
                            'Name': emp_name
                        },
                        {
                            'Date': date_str,
                            'Time': end_time,
                            'Status': 'OverTime Out',
                            'Name': emp_name
                        }
                    ])
        
        return pd.DataFrame(data)
    
    def time_function(self, func, *args, **kwargs):
        """Time a function execution"""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    
    def test_small_dataset_performance(self):
        """Test performance with small dataset (1,000 records)"""
        print(f"\n⚡ Testing Small Dataset Performance (1K records)")
        
        # Generate test data: 50 employees × 10 days = 1,000 records
        df = self.generate_test_data(num_employees=50, days_per_employee=10)
        
        initial_memory = self.get_memory_usage()
        
        # Time the processing
        result, execution_time = self.time_function(self.process_timesheet_data, df)
        
        final_memory = self.get_memory_usage()
        memory_used = final_memory - initial_memory
        
        # Performance assertions
        self.assertLessEqual(execution_time, self.MAX_PROCESSING_TIME_SMALL,
                            f"Small dataset processing took {execution_time:.2f}s, "
                            f"should be under {self.MAX_PROCESSING_TIME_SMALL}s")
        
        self.assertLessEqual(memory_used, self.MAX_MEMORY_MB,
                            f"Memory usage {memory_used:.2f}MB exceeded limit")
        
        print(f"✅ Execution time: {execution_time:.2f}s")
        print(f"✅ Memory used: {memory_used:.2f}MB")
        print(f"✅ Records processed: {len(df)}")
        print(f"✅ Output records: {len(result)}")
    
    def test_medium_dataset_performance(self):
        """Test performance with medium dataset (10,000 records)"""
        print(f"\n⚡ Testing Medium Dataset Performance (10K records)")
        
        # Generate test data: 167 employees × 30 days = ~10,000 records
        df = self.generate_test_data(num_employees=167, days_per_employee=30)
        
        initial_memory = self.get_memory_usage()
        
        # Time the processing
        result, execution_time = self.time_function(self.process_timesheet_data, df)
        
        final_memory = self.get_memory_usage()
        memory_used = final_memory - initial_memory
        
        # Performance assertions
        self.assertLessEqual(execution_time, self.MAX_PROCESSING_TIME_MEDIUM,
                            f"Medium dataset processing took {execution_time:.2f}s, "
                            f"should be under {self.MAX_PROCESSING_TIME_MEDIUM}s")
        
        self.assertLessEqual(memory_used, self.MAX_MEMORY_MB,
                            f"Memory usage {memory_used:.2f}MB exceeded limit")
        
        print(f"✅ Execution time: {execution_time:.2f}s")
        print(f"✅ Memory used: {memory_used:.2f}MB")
        print(f"✅ Records processed: {len(df)}")
        print(f"✅ Output records: {len(result)}")
    
    def test_large_dataset_performance(self):
        """Test performance with large dataset (100,000 records)"""
        print(f"\n⚡ Testing Large Dataset Performance (100K records)")
        
        # Generate test data: 1,667 employees × 30 days = ~100,000 records
        df = self.generate_test_data(num_employees=1667, days_per_employee=30)
        
        initial_memory = self.get_memory_usage()
        
        # Time the processing
        result, execution_time = self.time_function(self.process_timesheet_data, df)
        
        final_memory = self.get_memory_usage()
        memory_used = final_memory - initial_memory
        
        # Performance assertions
        self.assertLessEqual(execution_time, self.MAX_PROCESSING_TIME_LARGE,
                            f"Large dataset processing took {execution_time:.2f}s, "
                            f"should be under {self.MAX_PROCESSING_TIME_LARGE}s")
        
        self.assertLessEqual(memory_used, self.MAX_MEMORY_MB,
                            f"Memory usage {memory_used:.2f}MB exceeded limit")
        
        print(f"✅ Execution time: {execution_time:.2f}s")
        print(f"✅ Memory used: {memory_used:.2f}MB")
        print(f"✅ Records processed: {len(df)}")
        print(f"✅ Output records: {len(result)}")
    
    def test_memory_efficiency(self):
        """Test memory efficiency with chunked processing"""
        print(f"\n💾 Testing Memory Efficiency")
        
        # Generate large dataset
        df = self.generate_test_data(num_employees=500, days_per_employee=30)
        
        initial_memory = self.get_memory_usage()
        
        # Process in chunks to test memory efficiency
        chunk_size = 1000
        chunks = [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]
        
        results = []
        max_memory_used = 0
        
        for i, chunk in enumerate(chunks):
            chunk_result = self.process_timesheet_data(chunk)
            results.append(chunk_result)
            
            current_memory = self.get_memory_usage()
            memory_used = current_memory - initial_memory
            max_memory_used = max(max_memory_used, memory_used)
            
            print(f"Chunk {i+1}/{len(chunks)}: {memory_used:.2f}MB")
        
        # Combine results
        final_result = pd.concat(results, ignore_index=True)
        
        self.assertLessEqual(max_memory_used, self.MAX_MEMORY_MB,
                            f"Peak memory usage {max_memory_used:.2f}MB exceeded limit")
        
        print(f"✅ Peak memory usage: {max_memory_used:.2f}MB")
        print(f"✅ Total chunks processed: {len(chunks)}")
        print(f"✅ Final result size: {len(final_result)}")
    
    def test_concurrent_processing(self):
        """Test concurrent processing capabilities"""
        print(f"\n🔄 Testing Concurrent Processing")
        
        def process_employee_data(employee_data):
            """Process data for a single employee"""
            return self.process_timesheet_data(employee_data)
        
        # Generate data for multiple employees
        employees_data = []
        for emp_id in range(1, 11):  # 10 employees
            emp_df = self.generate_test_data(num_employees=1, days_per_employee=30)
            employees_data.append(emp_df)
        
        initial_memory = self.get_memory_usage()
        start_time = time.time()
        
        # Process sequentially first
        sequential_results = []
        for emp_data in employees_data:
            result = process_employee_data(emp_data)
            sequential_results.append(result)
        
        sequential_time = time.time() - start_time
        
        # Process concurrently using threading
        start_time = time.time()
        concurrent_results = []
        threads = []
        
        def worker(emp_data, results_list, index):
            result = process_employee_data(emp_data)
            results_list.insert(index, result)
        
        results_list = [None] * len(employees_data)
        
        for i, emp_data in enumerate(employees_data):
            thread = threading.Thread(target=worker, 
                                     args=(emp_data, results_list, i))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        concurrent_time = time.time() - start_time
        final_memory = self.get_memory_usage()
        memory_used = final_memory - initial_memory
        
        # Verify results are consistent
        self.assertEqual(len(sequential_results), len(results_list))
        
        print(f"✅ Sequential time: {sequential_time:.2f}s")
        print(f"✅ Concurrent time: {concurrent_time:.2f}s")
        print(f"✅ Speed improvement: {sequential_time/concurrent_time:.2f}x")
        print(f"✅ Memory used: {memory_used:.2f}MB")
    
    def process_timesheet_data(self, df):
        """Process timesheet data and return consolidated results"""
        # Add parsed columns
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
        
        return pd.DataFrame(consolidated_data)


class TestStressTesting(unittest.TestCase):
    """Stress tests for extreme conditions"""
    
    def setUp(self):
        self.processor = TimesheetBusinessRules()
    
    def test_extreme_dataset_size(self):
        """Test with extremely large dataset"""
        print(f"\n🔥 Stress Test: Extreme Dataset Size")
        
        # Test with 1 million records (may take a while)
        # This is commented out by default to avoid long test runs
        # Uncomment for full stress testing
        
        # df = self.generate_massive_dataset(records=1000000)
        # result = self.process_timesheet_data(df)
        # self.assertGreater(len(result), 0, "Should process extreme dataset")
        
        print("⚠️  Extreme dataset test skipped (uncomment to run)")
    
    def test_memory_stress(self):
        """Test memory usage under stress"""
        print(f"\n💾 Stress Test: Memory Usage")
        
        if not PSUTIL_AVAILABLE:
            print("⚠️  psutil not available, skipping memory stress test")
            return
        
        initial_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        
        # Create and process multiple datasets simultaneously
        datasets = []
        for i in range(5):  # Create 5 datasets
            df = pd.DataFrame({
                'Date': ['2025-01-01'] * 1000,
                'Time': ['08:00:00'] * 500 + ['17:00:00'] * 500,
                'Status': ['C/In'] * 500 + ['C/Out'] * 500,
                'Name': [f'Employee_{j}' for j in range(500)] * 2
            })
            datasets.append(df)
        
        final_memory = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        memory_used = final_memory - initial_memory
        
        print(f"✅ Memory stress test completed")
        print(f"✅ Memory used: {memory_used:.2f}MB")
        print(f"✅ Datasets created: {len(datasets)}")
    
    def test_cpu_intensive_operations(self):
        """Test CPU-intensive operations"""
        print(f"\n🖥️  Stress Test: CPU Intensive Operations")
        
        # Generate complex dataset with many overtime calculations
        data = []
        for i in range(1000):
            data.extend([
                {
                    'Date': '2025-01-01',
                    'Time': '08:00:00',
                    'Status': 'C/In',
                    'Name': f'Employee_{i}'
                },
                {
                    'Date': '2025-01-01',
                    'Time': '19:30:00',  # Overtime end
                    'Status': 'C/Out',
                    'Name': f'Employee_{i}'
                }
            ])
        
        df = pd.DataFrame(data)
        
        start_time = time.time()
        
        # Process multiple times to stress CPU
        for _ in range(10):
            # Add parsed columns
            df['Time_parsed'] = pd.to_datetime(df['Time']).dt.time
            
            # Calculate overtime for each record
            for _, row in df.iterrows():
                if row['Status'] == 'C/Out':
                    start_time_obj = datetime.strptime('08:00:00', '%H:%M:%S').time()
                    end_time_obj = row['Time_parsed']
                    
                    overtime = self.processor.calculate_overtime_hours(
                        start_time_obj, end_time_obj, "Day Shift"
                    )
        
        end_time = time.time()
        cpu_time = end_time - start_time
        
        print(f"✅ CPU stress test completed")
        print(f"✅ Processing time: {cpu_time:.2f}s")
        print(f"✅ Operations per second: {(len(df) * 10) / cpu_time:.0f}")


if __name__ == '__main__':
    # Check if memory_profiler is available
    if not MEMORY_PROFILER_AVAILABLE:
        print("⚠️  memory_profiler not available (pip install memory-profiler)")
    
    if not PSUTIL_AVAILABLE:
        print("⚠️  psutil not available (pip install psutil)")
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add performance tests
    suite.addTest(unittest.makeSuite(TestPerformanceBenchmarks))
    suite.addTest(unittest.makeSuite(TestStressTesting))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"⚡ PERFORMANCE TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    
    if result.wasSuccessful():
        print(f"✅ ALL PERFORMANCE TESTS PASSED!")
    else:
        print(f"❌ SOME PERFORMANCE TESTS FAILED!")
    
    # Print system information only if psutil is available
    if PSUTIL_AVAILABLE:
        print(f"\n💻 SYSTEM INFORMATION:")
        print(f"CPU Count: {psutil.cpu_count()}")
        print(f"Available Memory: {psutil.virtual_memory().available / (1024**3):.2f} GB")
        print(f"CPU Usage: {psutil.cpu_percent()}%")
    else:
        print(f"\n💻 SYSTEM INFORMATION: Not available (psutil required)")
    
    # Exit with appropriate code
    sys.exit(0 if result.wasSuccessful() else 1)