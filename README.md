# 🎯 Rolling Monthly Target Allocation System

A production-ready Streamlit application for automated target allocation across multiple outlets based on historical sales contribution percentages.

## 📋 Features

- ✅ **Automatic Column Detection** - Identifies outlets, months, and target columns
- ✅ **Contribution-Based Allocation** - Allocates targets proportionally based on historical sales
- ✅ **Data Validation** - Comprehensive validation with error handling
- ✅ **Rounding Precision** - Ensures total always equals target (within 0.01 tolerance)
- ✅ **Dynamic Column Structure** - Works with any number of monthly columns
- ✅ **Contribution % Column** - Automatically calculates and displays contribution percentages
- ✅ **Excel Export** - Download updated file with allocations and formatting
- ✅ **Monthly Workflow Support** - No code changes needed when adding new months

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Virtual Environment (already created)

### Installation

1. **Ensure virtual environment is activated:**
   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

2. **Install dependencies:**
   ```powershell
   pip install -r requirements.txt
   ```

3. **Run the Streamlit app:**
   ```powershell
   streamlit run app.py
   ```

The app will open in your default browser at `http://localhost:8501`

## 📊 Excel File Format

### Required Structure

```
| OUTLET NAME | July 2025 | Aug 2025 | Sep 2025 | ... | Jan 2026 | Feb 2026 Target |
|---|---|---|---|---|---|---|
| Downtown Shop | 1,500,000 | 1,600,000 | 1,550,000 | ... | 1,750,000 | |
| Mall Branch | 2,000,000 | 2,100,000 | 2,050,000 | ... | 2,250,000 | |
| ... | ... | ... | ... | ... | ... | |
| TOTAL | 11,200,000 | 11,900,000 | 11,540,000 | ... | 13,000,000 | |
```

### Requirements
- **First Column:** Must be named "OUTLET NAME"
- **Month Columns:** Follow format "Month YYYY" (e.g., "July 2025")
- **Target Column:** Contains word "Target" in the header
- **Total Row:** Must have "TOTAL" in outlet column
- **Values:** Must be numeric

## 🔄 Monthly Workflow

### When a month ends:

1. **Rename the Target Column:**
   - Example: "Feb 2026 Target" → "Feb 2026"
   - This converts it to an actual sales column

2. **Add New Target Column:**
   - Example: Add "Mar 2026 Target" at the end

3. **Upload Updated File:**
   - System automatically detects new structure
   - No code changes required!

## 📈 How It Works

### Calculation Process

1. **Historical Total** = Sum of all actual sales for each outlet across all months
2. **Company Total** = Sum of all outlet historical totals  
3. **Contribution %** = (Outlet Historical Total / Company Total) × 100
4. **Allocated Target** = (Contribution % / 100) × New Target
5. **Validation** = Sum of allocated targets ≈ New target (within 0.01)
6. **Rounding Adjustment** = Distributed proportionally if needed

### Ignored Elements
- ❌ TOTAL row
- ❌ Columns containing "Target"
- ❌ Non-numeric values

## 💾 Output File

The downloaded Excel file includes:

| Column | Description |
|---|---|
| OUTLET NAME | Shop/outlet name |
| Contribution % | Historical sales share percentage |
| All Historical Months | Original sales data |
| Target Column | Calculated allocations |

All currency values are formatted as numbers with 2 decimal places.

## 🎯 Example Calculation

**Input:**
- Downtown Shop historical total: ₨ 11,700,000
- Company historical total: ₨ 92,540,000
- New target: ₨ 3,200,000

**Calculation:**
- Contribution % = (11,700,000 / 92,540,000) × 100 = 12.64%
- Allocated Target = (12.64 / 100) × 3,200,000 = ₨ 404,480.00

## 📝 Sample Data

A sample Excel file is included: `sales_data_sample.xlsx`

**Generate new sample data:**
```powershell
python sample_data.py
```

## ⚙️ Configuration

### Streamlit Settings

Edit `.streamlit/config.toml` (if needed):

```toml
[theme]
primaryColor = "#0D78F2"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"

[server]
maxUploadSize = 50
```

## 🔍 Troubleshooting

### Issue: "Column names don't match"
- Ensure first column is exactly "OUTLET NAME"
- Ensure outlet names for each shop are in this column
- Ensure TOTAL row has exactly "TOTAL" (case-insensitive)

### Issue: "Non-numeric values detected"
- Check that all sales columns contain only numbers
- Remove commas from numbers - use plain numbers or decimals

### Issue: "Allocation total doesn't equal target"
- This is handled automatically with rounding adjustment
- The system finds the discrepancy and adjusts the largest allocation

## 📦 File Structure

```
CC Target/
├── app.py                    # Main Streamlit application
├── sample_data.py            # Sample data generator
├── requirements.txt          # Python dependencies
├── sales_data_sample.xlsx    # Sample Excel file
└── README.md                 # This file
```

## 🔒 Data Validation

The system validates:
- ✓ Outlet names are not empty
- ✓ All values are numeric
- ✓ Column headers are properly formatted
- ✓ Total row exists and is properly identified
- ✓ Sum of allocations equals target (within 0.01 tolerance)

## 📱 System Requirements

- **OS:** Windows, macOS, or Linux
- **Python:** 3.8 or higher
- **Memory:** Minimum 512 MB RAM
- **Browser:** Any modern web browser

## 🚀 Performance

- Handles up to 500 outlets without performance issues
- Processes typical Excel files (50 outlets × 12 months) in < 1 second
- File upload limit: 50 MB (configurable)

## 📄 License

Production-ready system - Use as needed

## 👥 Support

For issues or questions, check:
1. README.md (this file)
2. File format guide in the app
3. Technical details section in the app

---

**Version:** 1.0 | **Status:** Production Ready | **Last Updated:** Feb 2026
