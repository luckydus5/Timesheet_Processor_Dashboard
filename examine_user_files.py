import pandas as pd

print("="*80)
print("EXAMINING EXCEL FILES")
print("="*80)

# Check 88888888.xlsx
print("\n=== FILE: 88888888.xlsx ===")
try:
    xl = pd.ExcelFile('88888888.xlsx')
    print(f"Sheets: {xl.sheet_names}")
    
    for sheet in xl.sheet_names[:3]:  # First 3 sheets
        print(f"\n--- Sheet: {sheet} ---")
        df = pd.read_excel('88888888.xlsx', sheet_name=sheet, nrows=5)
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nFirst 3 rows:")
        print(df.head(3))
except Exception as e:
    print(f"Error: {e}")

# Check Book2.xlsx
print("\n\n=== FILE: Book2.xlsx ===")
try:
    xl = pd.ExcelFile('Book2.xlsx')
    print(f"Sheets: {xl.sheet_names}")
    
    for sheet in xl.sheet_names[:3]:  # First 3 sheets
        print(f"\n--- Sheet: {sheet} ---")
        df = pd.read_excel('Book2.xlsx', sheet_name=sheet, nrows=5)
        print(f"Shape: {df.shape}")
        print(f"Columns: {df.columns.tolist()}")
        print("\nFirst 3 rows:")
        print(df.head(3))
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*80)
print("ANALYSIS COMPLETE")
print("="*80)
