# 🚀 Quick Start Guide

## In 60 Seconds

### 1. Start the App
```powershell
.\run_app.ps1
```

### 2. Upload Your File
- Sidebar → "Upload Excel file with sales data"
- Select your Excel file

### 3. Calculate Allocations
- Enter monthly target (e.g., ₨ 3,200,000)
- Click "🔄 Calculate Allocations"
- Review outlet-wise allocations

### 4. Download Results
- Click "📥 Download Updated Excel"
- File includes contribution % and allocations

---

## Testing with Sample Data

### Generate Sample File
```powershell
python sample_data.py
```

This creates: `sales_data_sample.xlsx`

### Test Workflow
1. Run `.\run_app.ps1`
2. Upload `sales_data_sample.xlsx`
3. Enter target: 3,200,000
4. Click "Calculate Allocations"
5. Download and review the file

---

## File Structure

```
CC Target/
├── app.py                    ← Main Streamlit app
├── requirements.txt          ← Dependencies
├── README.md                 ← Full documentation
├── USER_GUIDE.md            ← Detailed user guide
├── QUICK_START.md           ← This file
├── sample_data.py           ← Sample data generator
├── sales_data_sample.xlsx   ← Sample Excel file
├── run_app.ps1              ← PowerShell launcher
├── run_app.bat              ← Command prompt launcher
├── setup.ps1                ← Setup script
└── .streamlit/
    └── config.toml          ← Streamlit configuration
```

---

## System Features

✅ **Automatic Column Detection**
- Identifies outlets, months, and targets automatically
- No configuration needed

✅ **Proportional Allocation**
- Each outlet gets target share = (Historical Sales ÷ Total) × Target

✅ **Contribution % Column**
- Shows each outlet's sales contribution
- Helps verify allocations

✅ **Validation & Rounding**
- Ensures allocations = target (within ±0.01)
- AutomaticallyAdjusts for rounding discrepancies

✅ **Excel Export**
- Download updated file with all allocations
- Formatted and ready to use

✅ **Monthly Workflow Support**
- Just rename columns and re-upload
- System auto-detects new structure

---

## Example Allocation

**Input:**
- Downtown Shop historical sales: ₨ 11,700,000
- Company total: ₨ 92,540,000
- Monthly target: ₨ 3,200,000

**Calculation:**
- Contribution: (11,700,000 ÷ 92,540,000) × 100 = 12.64%
- Allocation: 12.64% × ₨ 3,200,000 = **₨ 404,480.00**

---

## Next Steps

1. ✅ Virtual environment created and activated
2. ✅ All dependencies installed
3. 👉 Run: `.\run_app.ps1`
4. 👉 Upload your Excel file
5. 👉 Enter target budget
6. 👉 Download results

---

## Common Commands

### Start the app
```powershell
.\run_app.ps1
```

### Regenerate sample data
```powershell
python sample_data.py
```

### Install/Update dependencies
```powershell
pip install -r requirements.txt
```

### Verify Streamlit installation
```powershell
streamlit --version
```

---

## Troubleshooting

**App won't start?**
- Ensure virtual environment is activated: `.\venv\Scripts\Activate.ps1`
- Check all dependencies: `pip install -r requirements.txt`

**Upload fails?**
- Verify Excel file format (must be .xlsx or .xls)
- Check file size (max 50 MB)
- Ensure first column is named "OUTLET NAME"

**Allocations seem wrong?**
- Check "Contribution %" column - should sum to 100%
- Verify company total is non-zero
- Ensure all values are numeric

---

**Ready to start?** Run: `.\run_app.ps1`

For detailed documentation, see:
-📖 USER_GUIDE.md
- 📋 README.md
- 🔧 In-app help sections
