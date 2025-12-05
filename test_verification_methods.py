#!/usr/bin/env python3
"""
Test script for verification method analysis feature.
Tests the calculate_verification_methods() function with real data.
"""

import pandas as pd
from attendance_analyzer import load_attendance_file, calculate_verification_methods

def test_verification_methods(file_path: str):
    """Test verification method analysis on a file."""
    print(f"\n{'='*80}")
    print(f"Testing Verification Methods Analysis")
    print(f"File: {file_path}")
    print(f"{'='*80}\n")
    
    # Load the file
    print("Loading attendance data...")
    df = load_attendance_file(file_path)
    print(f"✅ Loaded {len(df):,} records for {df['Name'].nunique()} employees\n")
    
    # Check if VerifyCode column exists
    if 'VerifyCode' not in df.columns:
        print("❌ ERROR: No VerifyCode column found!")
        return
    
    # Calculate verification method statistics
    print("Calculating verification method statistics...")
    verify_stats = calculate_verification_methods(df)
    print("✅ Analysis complete!\n")
    
    # Display overall method summary
    print("=" * 80)
    print("📊 OVERALL METHOD USAGE SUMMARY")
    print("=" * 80)
    print(verify_stats['by_method'].to_string(index=False))
    print()
    
    # Display top users for each method
    print("=" * 80)
    print("🖐️ TOP 10 FINGERPRINT USERS")
    print("=" * 80)
    if not verify_stats['method_users']['FP'].empty:
        print(verify_stats['method_users']['FP'].head(10).to_string(index=False))
    else:
        print("No fingerprint users found")
    print()
    
    print("=" * 80)
    print("🔑 TOP 10 PASSWORD USERS")
    print("=" * 80)
    if not verify_stats['method_users']['PW'].empty:
        print(verify_stats['method_users']['PW'].head(10).to_string(index=False))
    else:
        print("No password users found")
    print()
    
    print("=" * 80)
    print("📡 RFID USERS (ALL)")
    print("=" * 80)
    if not verify_stats['method_users']['RF'].empty:
        print(verify_stats['method_users']['RF'].to_string(index=False))
    else:
        print("No RFID users found")
    print()
    
    # Display employee-level summary statistics
    print("=" * 80)
    print("👥 EMPLOYEE-LEVEL STATISTICS")
    print("=" * 80)
    by_employee = verify_stats['by_employee']
    print(f"Total employees: {len(by_employee)}")
    print(f"Employees using FP: {(by_employee['FP_Count'] > 0).sum()}")
    print(f"Employees using PW: {(by_employee['PW_Count'] > 0).sum()}")
    print(f"Employees using RF: {(by_employee['RF_Count'] > 0).sum()}")
    print()
    
    # Primary method breakdown
    print("Primary method distribution:")
    primary_counts = by_employee['Primary_Method'].value_counts()
    for method, count in primary_counts.items():
        percentage = (count / len(by_employee) * 100)
        print(f"  {method}: {count} employees ({percentage:.1f}%)")
    print()
    
    # Display a few sample employees
    print("=" * 80)
    print("📋 SAMPLE EMPLOYEES (Top 5 by total records)")
    print("=" * 80)
    sample = by_employee.head(5)[['Name', 'Department', 'FP_Count', 'PW_Count', 'RF_Count', 'Total_Records', 'Primary_Method']]
    print(sample.to_string(index=False))
    print()
    
    print("=" * 80)
    print("✅ TEST COMPLETE!")
    print("=" * 80)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        test_verification_methods(file_path)
    else:
        # Test with the sample file
        test_file = "Office Attendance fingerprint.xlsx"
        test_verification_methods(test_file)
