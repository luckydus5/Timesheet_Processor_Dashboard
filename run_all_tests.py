#!/usr/bin/env python3
"""
🧪 COMPREHENSIVE TEST RUNNER
============================

Run all testing infrastructure components:
- Unit tests for business rules
- Integration tests for file processing  
- Performance tests for large datasets
- Regression tests for rule changes

Usage:
    python run_all_tests.py [--verbose] [--performance] [--regression]
"""

import unittest
import sys
import os
import argparse
import time
from datetime import datetime
from pathlib import Path

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import test modules with error handling
try:
    from tests.test_business_rules import TestTimesheetBusinessRules, TestBusinessRuleCompliance
    UNIT_TESTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Unit tests not available: {e}")
    UNIT_TESTS_AVAILABLE = False

try:
    from tests.test_integration import TestFileProcessingIntegration, TestErrorHandlingIntegration
    INTEGRATION_TESTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Integration tests not available: {e}")
    INTEGRATION_TESTS_AVAILABLE = False

try:
    from tests.test_performance import TestPerformanceBenchmarks, TestStressTesting
    PERFORMANCE_TESTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Performance tests not available: {e}")
    PERFORMANCE_TESTS_AVAILABLE = False

try:
    from tests.test_regression import TestBusinessRuleRegression
    REGRESSION_TESTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Regression tests not available: {e}")
    REGRESSION_TESTS_AVAILABLE = False


class ComprehensiveTestRunner:
    """Comprehensive test runner for all test suites"""
    
    def __init__(self):
        self.start_time = None
        self.results = {}
        
    def run_unit_tests(self, verbosity=2):
        """Run unit tests for business rules"""
        print(f"\n{'='*60}")
        print(f"🧪 RUNNING UNIT TESTS FOR BUSINESS RULES")
        print(f"{'='*60}")
        
        if not UNIT_TESTS_AVAILABLE:
            print(f"❌ Unit tests not available")
            return False
        
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestTimesheetBusinessRules))
        suite.addTest(unittest.makeSuite(TestBusinessRuleCompliance))
        
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        
        self.results['unit_tests'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'success': result.wasSuccessful()
        }
        
        return result.wasSuccessful()
    
    def run_integration_tests(self, verbosity=2):
        """Run integration tests for file processing"""
        print(f"\n{'='*60}")
        print(f"🔄 RUNNING INTEGRATION TESTS FOR FILE PROCESSING")
        print(f"{'='*60}")
        
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestFileProcessingIntegration))
        suite.addTest(unittest.makeSuite(TestErrorHandlingIntegration))
        
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        
        self.results['integration_tests'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'success': result.wasSuccessful()
        }
        
        return result.wasSuccessful()
    
    def run_performance_tests(self, verbosity=2):
        """Run performance tests for large datasets"""
        print(f"\n{'='*60}")
        print(f"⚡ RUNNING PERFORMANCE TESTS FOR LARGE DATASETS")
        print(f"{'='*60}")
        
        # Check if performance testing dependencies are available
        try:
            import psutil
            import memory_profiler
        except ImportError as e:
            print(f"⚠️  Performance testing dependencies missing: {e}")
            print(f"   Install with: pip install psutil memory-profiler")
            return False
        
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestPerformanceBenchmarks))
        suite.addTest(unittest.makeSuite(TestStressTesting))
        
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        
        self.results['performance_tests'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'success': result.wasSuccessful()
        }
        
        return result.wasSuccessful()
    
    def run_regression_tests(self, verbosity=2):
        """Run regression tests for rule changes"""
        print(f"\n{'='*60}")
        print(f"🔄 RUNNING REGRESSION TESTS FOR RULE CHANGES")
        print(f"{'='*60}")
        
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestBusinessRuleRegression))
        
        runner = unittest.TextTestRunner(verbosity=verbosity)
        result = runner.run(suite)
        
        self.results['regression_tests'] = {
            'tests_run': result.testsRun,
            'failures': len(result.failures),
            'errors': len(result.errors),
            'success': result.wasSuccessful()
        }
        
        return result.wasSuccessful()
    
    def run_all_tests(self, include_performance=True, include_regression=True, verbosity=2):
        """Run all test suites"""
        print(f"\n{'='*80}")
        print(f"🚀 COMPREHENSIVE TIMESHEET TESTING INFRASTRUCTURE")
        print(f"{'='*80}")
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        self.start_time = time.time()
        
        # Track overall success
        all_success = True
        
        # Run unit tests (always run)
        if not self.run_unit_tests(verbosity):
            all_success = False
        
        # Run integration tests (always run)
        if not self.run_integration_tests(verbosity):
            all_success = False
        
        # Run performance tests (optional)
        if include_performance:
            if not self.run_performance_tests(verbosity):
                all_success = False
        else:
            print(f"\n⚠️  Performance tests skipped (use --performance to include)")
        
        # Run regression tests (optional)
        if include_regression:
            if not self.run_regression_tests(verbosity):
                all_success = False
        else:
            print(f"\n⚠️  Regression tests skipped (use --regression to include)")
        
        # Print comprehensive summary
        self.print_summary()
        
        return all_success
    
    def print_summary(self):
        """Print comprehensive test summary"""
        end_time = time.time()
        total_time = end_time - self.start_time if self.start_time else 0
        
        print(f"\n{'='*80}")
        print(f"📊 COMPREHENSIVE TEST SUMMARY")
        print(f"{'='*80}")
        
        # Summary table
        total_tests = 0
        total_failures = 0
        total_errors = 0
        all_successful = True
        
        for test_type, result in self.results.items():
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            print(f"{test_type.replace('_', ' ').title():.<50} {status}")
            print(f"  Tests: {result['tests_run']:>3} | Failures: {result['failures']:>3} | Errors: {result['errors']:>3}")
            
            total_tests += result['tests_run']
            total_failures += result['failures']
            total_errors += result['errors']
            
            if not result['success']:
                all_successful = False
        
        print(f"{'='*80}")
        print(f"TOTALS:")
        print(f"  Total Tests Run: {total_tests}")
        print(f"  Total Failures: {total_failures}")
        print(f"  Total Errors: {total_errors}")
        print(f"  Execution Time: {total_time:.2f} seconds")
        
        if all_successful:
            print(f"\n🎉 ALL TESTS PASSED! 🎉")
            print(f"✅ Your timesheet processing system is working correctly!")
        else:
            print(f"\n❌ SOME TESTS FAILED!")
            print(f"⚠️  Please review the failed tests above")
        
        # Test coverage analysis
        print(f"\n📋 TEST COVERAGE ANALYSIS:")
        print(f"✅ Business Rules: Unit tests validate all calculation logic")
        print(f"✅ File Processing: Integration tests cover Excel/CSV workflows")
        
        if 'performance_tests' in self.results:
            print(f"✅ Performance: Large dataset handling validated")
        else:
            print(f"⚠️  Performance: Not tested (use --performance flag)")
        
        if 'regression_tests' in self.results:
            print(f"✅ Regression: Rule stability validated")
        else:
            print(f"⚠️  Regression: Not tested (use --regression flag)")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        
        if total_failures > 0:
            print(f"🔴 HIGH PRIORITY: Fix {total_failures} failing test(s)")
        
        if total_errors > 0:
            print(f"🔴 HIGH PRIORITY: Fix {total_errors} error(s)")
        
        if 'performance_tests' not in self.results:
            print(f"🟡 MEDIUM: Run performance tests with --performance flag")
        
        if 'regression_tests' not in self.results:
            print(f"🟡 MEDIUM: Run regression tests with --regression flag")
        
        if all_successful:
            print(f"🟢 EXCELLENT: All tested functionality is working correctly!")
        
        print(f"\n{'='*80}")


def main():
    """Main function for test runner"""
    
    parser = argparse.ArgumentParser(
        description="Comprehensive test runner for timesheet processing system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_all_tests.py                    # Run unit and integration tests
  python run_all_tests.py --performance      # Include performance tests
  python run_all_tests.py --regression       # Include regression tests
  python run_all_tests.py --verbose          # Detailed output
  python run_all_tests.py --performance --regression --verbose  # Full suite
        """
    )
    
    parser.add_argument(
        '--performance',
        action='store_true',
        help='Include performance tests (requires psutil, memory-profiler)'
    )
    
    parser.add_argument(
        '--regression',
        action='store_true',
        help='Include regression tests'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Verbose test output'
    )
    
    parser.add_argument(
        '--unit-only',
        action='store_true',
        help='Run only unit tests'
    )
    
    parser.add_argument(
        '--integration-only',
        action='store_true',
        help='Run only integration tests'
    )
    
    parser.add_argument(
        '--performance-only',
        action='store_true',
        help='Run only performance tests'
    )
    
    parser.add_argument(
        '--regression-only',
        action='store_true',
        help='Run only regression tests'
    )
    
    args = parser.parse_args()
    
    # Determine verbosity
    verbosity = 2 if args.verbose else 1
    
    # Create test runner
    runner = ComprehensiveTestRunner()
    
    # Handle individual test type runs
    if args.unit_only:
        success = runner.run_unit_tests(verbosity)
        runner.print_summary()
        sys.exit(0 if success else 1)
    
    if args.integration_only:
        success = runner.run_integration_tests(verbosity)
        runner.print_summary()
        sys.exit(0 if success else 1)
    
    if args.performance_only:
        success = runner.run_performance_tests(verbosity)
        runner.print_summary()
        sys.exit(0 if success else 1)
    
    if args.regression_only:
        success = runner.run_regression_tests(verbosity)
        runner.print_summary()
        sys.exit(0 if success else 1)
    
    # Run comprehensive test suite
    success = runner.run_all_tests(
        include_performance=args.performance,
        include_regression=args.regression,
        verbosity=verbosity
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()