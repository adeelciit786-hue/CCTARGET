import pandas as pd
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

# Create sample data
data = {
    'OUTLET NAME': [
        'Downtown Shop',
        'Mall Branch',
        'Airport Store',
        'Downtown West',
        'North Plaza',
        'South Center',
        'East Wing',
        'West Gate',
        'TOTAL'
    ],
    'July 2025': [1500000, 2000000, 1200000, 1800000, 900000, 1100000, 1300000, 1400000, 11200000],
    'Aug 2025': [1600000, 2100000, 1300000, 1900000, 950000, 1150000, 1400000, 1500000, 11900000],
    'Sep 2025': [1550000, 2050000, 1250000, 1850000, 920000, 1120000, 1350000, 1450000, 11540000],
    'Oct 2025': [1700000, 2200000, 1400000, 2000000, 1000000, 1200000, 1500000, 1600000, 12600000],
    'Nov 2025': [1800000, 2300000, 1500000, 2100000, 1050000, 1250000, 1600000, 1700000, 13300000],
    'Dec 2025': [1900000, 2400000, 1600000, 2200000, 1100000, 1300000, 1700000, 1800000, 14000000],
    'Jan 2026': [1750000, 2250000, 1450000, 2050000, 1000000, 1200000, 1550000, 1700000, 13000000],
}

df = pd.DataFrame(data)

# Save to Excel
df.to_excel('sales_data_sample.xlsx', index=False, sheet_name='Sales')

print("✅ Sample Excel file created: sales_data_sample.xlsx")
print("\nSample data preview:")
print(df.to_string())
