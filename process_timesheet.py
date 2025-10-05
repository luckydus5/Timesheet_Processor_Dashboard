"""
🚀 TIMESHEET PROCESSOR - SIMPLE USAGE SCRIPT
============================================

This script demonstrates how to use the timesheet business rules
to process any Excel or CSV timesheet file.

Simply update the INPUT_FILE variable and run this script!
"""

from timesheet_business_rules import process_timesheet_file, TimesheetBusinessRules

def main():
    """Main function to process timesheet data"""
    
    # 🔧 CONFIGURATION - UPDATE THESE VALUES
    # =====================================
    INPUT_FILE = "TimeCheck.csv"  # Change this to your file path
    OUTPUT_NAME = "Company_Processed_Timesheet"  # Optional: change output name
    
    print("🚀 TIMESHEET PROCESSING SCRIPT")
    print("=" * 50)
    
    # Step 1: Show business rules
    print("\n🎯 BUSINESS RULES BEING APPLIED:")
    rules = TimesheetBusinessRules()
    
    # Step 2: Process the file
    print(f"\n📂 Processing file: {INPUT_FILE}")
    processed_data, csv_output, excel_output = process_timesheet_file(
        INPUT_FILE, 
        OUTPUT_NAME
    )
    
    # Step 3: Show results
    if processed_data is not None:
        print(f"\n🎉 SUCCESS! Files created:")
        if csv_output:
            print(f"   📄 CSV: {csv_output}")
        if excel_output:
            print(f"   📊 Excel: {excel_output}")
        
        # Show sample of processed data
        print(f"\n📋 SAMPLE OF PROCESSED DATA:")
        print("-" * 80)
        
        # Show a few examples
        sample = processed_data.head(5)
        for _, row in sample.iterrows():
            print(f"{row['Name']:20} | {row['Date']:12} | {row['Time']:8} | {row['Status']:12}")
            print(f"{'':20} | Start: {row['Start Time']:8} | End: {row['End Time']:8} | {row['Shift Time']:10}")
            print(f"{'':20} | Total: {row['Total Hours']:5}h | Regular: {row['Regular Hours']:5}h | OT: {row['Overtime Hours']:4}h")
            print("-" * 80)
        
        # Summary statistics
        print(f"\n📊 PROCESSING SUMMARY:")
        print(f"   Total Records: {len(processed_data):,}")
        print(f"   Unique Employees: {processed_data['Name'].nunique()}")
        
        day_shifts = len(processed_data[processed_data['Shift Time'] == 'Day Shift'])
        night_shifts = len(processed_data[processed_data['Shift Time'] == 'Night Shift'])
        print(f"   Day Shifts: {day_shifts:,} ({day_shifts/len(processed_data)*100:.1f}%)")
        print(f"   Night Shifts: {night_shifts:,} ({night_shifts/len(processed_data)*100:.1f}%)")
        
        overtime_count = len(processed_data[processed_data['Overtime Hours'] > 0])
        total_overtime = processed_data['Overtime Hours'].sum()
        print(f"   Overtime Records: {overtime_count:,} ({overtime_count/len(processed_data)*100:.1f}%)")
        print(f"   Total Overtime Hours: {total_overtime:.2f}")
        
    else:
        print("❌ Processing failed. Please check your input file.")


if __name__ == "__main__":
    main()