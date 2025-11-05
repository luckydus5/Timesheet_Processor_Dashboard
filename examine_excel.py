import pandas as pd
import openpyxl

print("=== Examining Consolidated_OT management2.xlsx ===\n")

# Read Overal sheet
print("--- OVERAL SHEET ---")
df_overal = pd.read_excel('Consolidated_OT management2.xlsx', sheet_name='Overal', header=2)
print(f"Shape: {df_overal.shape}")
print(f"Columns: {df_overal.columns.tolist()[:15]}")
print("\nFirst 5 rows (columns A-H):")
print(df_overal.iloc[:5, :8])

# Read Consolidated sheet
print("\n\n--- CONSOLIDATED SHEET ---")
df_cons = pd.read_excel('Consolidated_OT management2.xlsx', sheet_name='Consolidated', header=0)
print(f"Shape: {df_cons.shape}")
print(f"Columns: {df_cons.columns.tolist()[:10]}")
print("\nFirst 5 rows:")
print(df_cons.iloc[:5, :6])

# Check H column specifically
print("\n\n--- COLUMN H (Hrs at 1.5 rate) in Overal ---")
print("Column H name:", df_overal.columns[7] if len(df_overal.columns) > 7 else "N/A")
print("Sample values:")
print(df_overal.iloc[:10, 7])
