# 🏗️ Type of Work Dropdown Feature

## ✅ Feature Added!

A dropdown selector has been added to the **Attendance Consolidation** tab (Tab 2) to specify the type of work being processed.

---

## 🎯 Available Work Types

The system now supports the following work types:

1. **Wagon** 🚃
2. **Superloader** 🚛
3. **Bulldozer/Superloader** 🚜
4. **Pump** ⚙️
5. **Miller** 🏭
6. **Regular Work** (default)
7. **Overtime Work**

---

## 📋 How to Use

### Step 1: Upload File
Navigate to **Tab 2: Attendance Consolidation**

### Step 2: Select Type of Work
Before converting, select the appropriate work type from the dropdown:

```
🏗️ Select Type of Work
┌─────────────────────────────────────┐
│ Choose the type of work:            │
│ ▼ Wagon                             │
│   Superloader                       │
│   Bulldozer/Superloader             │
│   Pump                              │
│   Miller                            │
│   Regular Work  ← Default           │
│   Overtime Work                     │
└─────────────────────────────────────┘
```

### Step 3: Convert
Click **"🔄 Convert to OT Management Format"**

---

## 📊 Output Format

### Type of Work Column Behavior:

#### For Complete Records (with both Check In & Check Out):
```
Type of Work: [Selected Type]
or
Type of Work: [Selected Type] - OT  (if overtime exists)
```

**Examples:**
- `Wagon` (no overtime)
- `Wagon - OT` (with overtime)
- `Superloader` (no overtime)
- `Bulldozer/Superloader - OT` (with overtime)

#### For Incomplete Records:
```
Type of Work: [Selected Type] - Incomplete
```

**Examples:**
- `Wagon - Incomplete` (missing check-in or check-out)
- `Pump - Incomplete`

#### For Missing Records:
```
Type of Work: [Selected Type] - No Record
```

**Examples:**
- `Miller - No Record` (both check-in and check-out missing)

---

## 🎨 Visual Example

### Input: OPERATORS file with Wagon workers
### Selected: "Wagon" from dropdown
### Output:

```
┌────┬────────────────┬─────────────┬────────┬────────┬───────────┬────────┬─────────────────────┐
│ SN │ EMPLOYEE NAME  │ Date        │ Start  │ End    │ No. Hours │ OT Hrs │ Type of Work        │
├────┼────────────────┼─────────────┼────────┼────────┼───────────┼────────┼─────────────────────┤
│ 1  │ John Doe       │ 09-Oct-2025 │ 07:45  │ 15:30  │ 07:45:00  │ 0.00   │ Wagon               │
│ 2  │ John Doe       │ 10-Oct-2025 │ 07:45  │ 18:00  │ 10:15:00  │ 1.00   │ Wagon - OT          │
│ 3  │ Jane Smith     │ 09-Oct-2025 │ 08:00  │ N/A    │ 00:00:00  │ 0.00   │ Wagon - Incomplete  │
│ 4  │ Mike Johnson   │ 11-Oct-2025 │ N/A    │ N/A    │ 00:00:00  │ 0.00   │ Wagon - No Record   │
└────┴────────────────┴─────────────┴────────┴────────┴───────────┴────────┴─────────────────────┘
```

---

## 🔍 Use Cases

### 1. **Wagon Operations**
- Select "Wagon" for workers operating wagons
- Easy to track wagon-specific overtime and hours

### 2. **Superloader Teams**
- Select "Superloader" for loading equipment operators
- Separate reporting for superloader operations

### 3. **Bulldozer/Superloader Mixed**
- Select "Bulldozer/Superloader" for workers using both
- Combined tracking for dual-equipment operators

### 4. **Pump Operations**
- Select "Pump" for pump operators
- Dedicated category for pump maintenance/operation

### 5. **Miller Operations**
- Select "Miller" for milling equipment workers
- Track miller-specific work hours

---

## 💡 Benefits

### ✅ **Clear Classification**
- Know exactly what type of work was performed
- Easy filtering and reporting by work type

### ✅ **Overtime Tracking**
- Automatically adds " - OT" suffix when overtime detected
- Clear distinction between regular and OT hours

### ✅ **Data Quality**
- " - Incomplete" suffix for records with missing times
- " - No Record" suffix for completely missing data

### ✅ **Flexible Reporting**
- Filter by work type in Excel
- Analyze productivity by equipment/operation type
- Generate equipment-specific reports

---

## 📈 Analysis Capabilities

### Filter by Work Type in Excel:
```
1. Open downloaded Excel file
2. Click on "Type of Work" column header
3. Use AutoFilter to select specific types
4. Analyze hours by equipment type
```

### Example Analyses:
- **Total Wagon hours this month**
- **Superloader overtime trends**
- **Pump vs Miller productivity**
- **Equipment-specific labor costs**

---

## 🔄 Workflow

### Processing Multiple Work Types:

If you have different work types in different files:

1. **Upload Wagon file** → Select "Wagon" → Convert → Download
2. **Upload Superloader file** → Select "Superloader" → Convert → Download
3. **Upload Pump file** → Select "Pump" → Convert → Download

Each file gets its own work type classification!

---

## 📝 Technical Details

### Function Signature:
```python
def convert_attendance_to_overtime(
    attendance_df: pd.DataFrame, 
    column_mapping: Dict[str, Any], 
    type_of_work: str = "Regular Work"
) -> Tuple[pd.DataFrame, pd.DataFrame]:
```

### Default Value:
If no selection is made, defaults to **"Regular Work"**

### Dropdown Location:
Tab 2: Attendance Consolidation, between format detection and convert button

---

## 🎯 Examples by Category

### Wagon Workers:
```
Type of Work: Wagon
Type of Work: Wagon - OT
Type of Work: Wagon - Incomplete
Type of Work: Wagon - No Record
```

### Superloader Operators:
```
Type of Work: Superloader
Type of Work: Superloader - OT
Type of Work: Superloader - Incomplete
```

### Bulldozer/Superloader:
```
Type of Work: Bulldozer/Superloader
Type of Work: Bulldozer/Superloader - OT
```

### Pump Operations:
```
Type of Work: Pump
Type of Work: Pump - OT
Type of Work: Pump - Incomplete
```

### Miller Teams:
```
Type of Work: Miller
Type of Work: Miller - OT
Type of Work: Miller - No Record
```

---

## 🚀 Quick Start

1. **Go to Tab 2** (🔄 Attendance Consolidation)
2. **Upload your file** (e.g., OPERATORS 09-13.csv)
3. **Select work type** from dropdown (e.g., "Wagon")
4. **Click Convert**
5. **Download Excel** with work type classification

---

## ✨ Summary

| Feature | Description |
|---------|-------------|
| **Location** | Tab 2: Attendance Consolidation |
| **Work Types** | 7 options (Wagon, Superloader, Bulldozer/Superloader, Pump, Miller, Regular, Overtime) |
| **Output** | Type of Work column with selected type + status suffix |
| **Default** | Regular Work |
| **Suffixes** | None, " - OT", " - Incomplete", " - No Record" |

---

**Feature Status:** ✅ **READY TO USE**

Upload your file, select the work type, and see the classification in action! 🎯
