# Target Allocation System - User Guide

## 📊 Getting Started

### Step 1: Prepare Your Excel File

Your Excel file should have this structure:

```
Column A: OUTLET NAME (first column, always required)
Columns B-N: Monthly Sales Data (format: "Month YYYY")
Column O: Target Column (format: "Feb 2026 Target")
Last Row: TOTAL
```

**Example:**

```
OUTLET NAME    | July 2025  | Aug 2025  | ... | Feb 2026 Target
Downtown Shop  | 1,500,000  | 1,600,000 | ... | 
Mall Branch    | 2,000,000  | 2,100,000 | ... |
...            | ...        | ...       | ... | ...
TOTAL          | 11,200,000 | 11,900,000| ... |
```

### Step 2: Start the Application

#### Option A: Using PowerShell (Recommended)
```powershell
.\run_app.ps1
```

#### Option B: Using Command Prompt
```cmd
run_app.bat
```

#### Option C: Manual
```powershell
.\venv\Scripts\Activate.ps1
streamlit run app.py
```

The app will open in your browser at: `http://localhost:8501`

### Step 3: Upload Your File

1. In the left sidebar, click "Upload Excel file with sales data"
2. Select your Excel file
3. The system automatically detects:
   - Number of outlets
   - Historical months
   - Target column

### Step 4: Enter Target Amount

1. In the "Target Allocation" section, enter the monthly target budget
2. Click "🔄 Calculate Allocations"
3. The system calculates and displays:
   - Each outlet's historical contribution %
   - Allocated target amount for each outlet
   - Validation status

### Step 5: Download Results

1. Click "📥 Download Updated Excel"
2. Open the file and verify the allocations
3. The file includes:
   - Original sales data
   - Contribution % column
   - Allocated Target column

---

## 📈 Understanding the Results

### Key Metrics Displayed

| Metric | Meaning |
|--------|---------|
| **Company Historical Total** | Sum of all sales across all outlets and months |
| **Target to Allocate** | The monthly budget you entered |
| **Avg. Outlet Allocation** | Target amount / Number of outlets (informational) |
| **Highest Allocation** | Maximum allocated to any single outlet |

### Outlet-wise Allocation Table

| Column | Meaning |
|--------|---------|
| **Outlet Name** | Store/shop identifier |
| **Historical Total** | Sum of this outlet's sales across all historical months |
| **Contribution %** | This outlet's share of total sales (%) |
| **Allocated Target** | Proportional target for this outlet |

**Example:**
```
Downtown Shop | ₨ 11,700,000 | 12.64% | ₨ 404,480.00
Mall Branch   | ₨ 15,900,000 | 17.19% | ₨ 550,080.00
```

---

## 🔄 Monthly Workflow

### When a Month Ends:

#### Workflow Step 1: Rename Target Column
- The "Feb 2026 Target" column contains your allocations
- Rename it to "Feb 2026" (remove "Target")
- This makes it part of historical data for next month

**Before:**
```
Jan 2026 | Feb 2026 Target | 
1,750,000 | 404,480.00 |
```

**After:**
```
Jan 2026 | Feb 2026 | Mar 2026 Target |
1,750,000 | 404,480.00 | (empty) |
```

#### Workflow Step 2: Add New Target Column
- Add a new column: "Mar 2026 Target" (next month)
- Leave it empty - the system will fill it

#### Workflow Step 3: Re-upload File
- Upload the updated file to the system
- No code changes needed!
- The system automatically detects:
  - Feb 2026 is now historical data
  - Mar 2026 Target is the new target column

---

## 🔢 Allocation Calculation Details

### Formula

For each outlet:

```
1. Historical Total = Sum of outlet's sales across all actual months

2. Contribution % = (Outlet Historical Total / Company Historical Total) × 100

3. Allocated Target = (Contribution % / 100) × New Monthly Target

4. Rounding = All values rounded to 2 decimal places

5. Validation = Sum(All Allocated Targets) ≈ New Monthly Target
   (Within ±0.01 tolerance, auto-adjusted if needed)
```

### Example Calculation

**Given:**
- Company historical total: ₨ 92,540,000
- Downtown Shop historical total: ₨ 11,700,000
- New monthly target: ₨ 3,200,000

**Step-by-step:**

1. Contribution % = (11,700,000 ÷ 92,540,000) × 100 = 12.64%
2. Allocated Target = (12.64% ÷ 100) × 3,200,000 = ₨ 404,480.00

---

## ✅ Validation Checks

### System Validates:

✓ **Outlet Names**
- No empty cells in outlet column
- Each outlet has a name

✓ **Numeric Values**
- All sales columns contain numbers only
- No text or special characters

✓ **Column Format**
- Month columns follow "Month YYYY" format
- Example: "July 2025", "Jan 2026"

✓ **Total Row**
- Identified as "TOTAL"
- Excluded from calculations

✓ **Allocation Accuracy**
- Sum of allocations = Target ± 0.01
- Automatically adjusted if needed

### Validation Messages

| Message | Meaning |
|---------|---------|
| ✅ Validation Passed! | Allocations are accurate |
| ⚠️ Rounding discrepancy | Auto-adjusted to match target |
| ❌ Non-numeric values | Check your sales data |

---

## 📁 File Requirements Checklist

Before uploading, verify:

- [ ] First column is named "OUTLET NAME"
- [ ] All outlet names are filled in (no blanks)
- [ ] Month columns follow "Month YYYY" format
- [ ] All sales values are numeric
- [ ] Last row has "TOTAL"
- [ ] Target column contains "Target" in name
- [ ] File is .xlsx, .xls, or .csv

---

## 🚨 Common Issues & Solutions

### Issue: "Column names don't match"
**Solution:** 
- Ensure first column header is exactly "OUTLET NAME" (case sensitive for detection)
- Check that month columns follow pattern: "Month YYYY"
- Verify target column has "Target" in the name

### Issue: "Non-numeric values detected"
**Solution:**
- Remove all commas from numbers
- Check for text characters in numeric columns
- Use decimals only where needed

### Issue: "Allocation doesn't equal target"
**Solution:**
- This is expected due to rounding
- System automatically adjusts the largest allocation
- Discrepancy shown in validation message

### Issue: "File upload fails"
**Solution:**
- Try converting to .xlsx format
- Ensure file size < 50 MB
- Verify file is not corrupted

---

## 💡 Tips & Best Practices

1. **Keep Data Clean**
   - Use consistent date format: "Month YYYY"
   - Always include TOTAL row
   - No extra blank columns

2. **Monthly Updates**
   - After renaming target → actual month
   - Update TOTAL row manually or use Excel SUM formula
   - Add new target column before uploading

3. **Data Backup**
   - Always keep original files
   - Downloaded files are versioned with timestamp
   - Example: `Target_Allocation_20260216_143022.xlsx`

4. **Performance**
   - System handles 500+ outlets efficiently
   - Files process in < 1 second
   - Suitable for daily use

---

## 📞 Support

For troubleshooting, refer to:
1. **README.md** - Technical overview
2. **File Format Guide** - In app, click "📖 File Format Guide"
3. **Technical Details** - In app, click "🔧 Technical Details"

---

## 🎯 Sample Workflow Timeline

### Month 1: Setup
- Upload file with Jan 2026 sales
- Enter Feb 2026 target: ₨ 3,200,000
- Download: `Target_Allocation_20260216_*****.xlsx`

### Month 2: Update
1. Rename "Feb 2026 Target" → "Feb 2026"
2. Add "Mar 2026 Target" column
3. Upload updated file
4. Enter Mar 2026 target: ₨ 3,300,000
5. Download new allocations

### Repeat
Continue monthly workflow - system adapts automatically!

---

**Version:** 1.0 | **Last Updated:** Feb 2026
