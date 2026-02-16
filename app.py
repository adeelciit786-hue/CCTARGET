import streamlit as st
import pandas as pd
import numpy as np
from io import BytesIO
from datetime import datetime, timedelta
import calendar
import re

st.set_page_config(
    page_title="Target Allocation System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Rolling Monthly Target Allocation System")

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def extract_month_year(column_name):
    """Extract month and year from column name."""
    # Pattern: Month YYYY (e.g., "July 2025", "Jan 2026")
    pattern = r'([A-Za-z]+)\s+(\d{4})'
    match = re.search(pattern, column_name)
    if match:
        return True
    return False


def parse_month_year(month_str):
    """
    Parse month string to datetime object.
    
    Format: "July 2025" or "Jul 2025" → datetime(2025, 7, 1)
    
    Returns: (datetime_obj, is_valid, error_message)
    """
    try:
        # Try full month name first (July)
        dt = datetime.strptime(month_str.strip(), "%B %Y")
        return dt, True, None
    except ValueError:
        try:
            # Try abbreviated month name (Jul)
            dt = datetime.strptime(month_str.strip(), "%b %Y")
            return dt, True, None
        except ValueError:
            return None, False, f"Invalid date format: '{month_str}'. Use 'July 2025' or 'Jul 2025'"


def get_days_in_month(year, month):
    """
    Get the actual number of days in a given month.
    
    Handles: 28, 29 (leap year), 30, 31 days
    Returns: (days_count, is_leap_year)
    """
    days = calendar.monthrange(year, month)[1]
    is_leap = calendar.isleap(year)
    return days, is_leap


def validate_target_month_format(target_col_name):
    """
    Extract and validate target month from column name.
    
    Example: "Mar 2026 Target" → (datetime(2026, 3, 1), True, None)
    
    Returns: (datetime_obj, is_valid, error_message)
    """
    if not target_col_name:
        return None, False, "Target column not found"
    
    # Extract month and year (remove "Target" suffix)
    month_year_str = target_col_name.replace("Target", "").strip()
    
    dt, is_valid, error = parse_month_year(month_year_str)
    return dt, is_valid, error


def calculate_total_historical_days(month_columns):
    """
    Calculate total days across all historical months.
    
    Example: ["July 2025", "Aug 2025", "Sep 2025"]
    Returns: 31 + 31 + 30 = 92 days
    
    Returns: (total_days, month_details, is_valid, error_message)
    """
    total_days = 0
    month_details = []
    
    for col in month_columns:
        dt, is_valid, error = parse_month_year(col)
        
        if not is_valid:
            return 0, [], False, error
        
        days, is_leap = get_days_in_month(dt.year, dt.month)
        total_days += days
        month_details.append({
            'month': col,
            'days': days,
            'is_leap': is_leap,
            'date': dt
        })
    
    return total_days, month_details, True, None


def validate_month_sequence(historical_months, target_month_dt):
    """
    Ensure target month is AFTER last historical month.
    
    Returns: (is_valid, error_message)
    """
    if not historical_months:
        return False, "No historical months found"
    
    # Parse last historical month
    last_col = historical_months[-1]
    last_dt, is_valid, error = parse_month_year(last_col)
    
    if not is_valid:
        return False, error
    
    # Check if target is after last historical month
    if target_month_dt <= last_dt:
        return False, f"Target month {target_month_dt.strftime('%b %Y')} must be AFTER last historical month {last_dt.strftime('%b %Y')}"
    
    return True, None


def validate_no_duplicate_months(month_columns):
    """
    Ensure no duplicate month columns.
    
    Returns: (is_valid, error_message, duplicates)
    """
    seen = set()
    duplicates = []
    
    for col in month_columns:
        dt, is_valid, error = parse_month_year(col)
        if is_valid:
            key = dt.strftime("%b %Y")
            if key in seen:
                duplicates.append(col)
            seen.add(key)
    
    if duplicates:
        return False, f"Duplicate months found: {duplicates}", duplicates
    
    return True, None, []


def classify_columns(df):
    """
    Classify columns with enhanced validation.
    
    Returns:
    - outlet_col: First column (outlet names)
    - month_cols: Columns with actual monthly data (no "Target")
    - target_col: Column containing "Target"
    - validation_errors: List of validation issues
    """
    columns = df.columns.tolist()
    outlet_col = columns[0]
    month_cols = []
    target_col = None
    validation_errors = []
    
    # Classify columns
    for col in columns[1:]:
        if 'target' in col.lower():
            target_col = col
        elif extract_month_year(col):
            month_cols.append(col)
    
    # Validation checks
    if not target_col:
        validation_errors.append("⚠️ No target column found (column should contain 'Target')")
    
    if not month_cols:
        validation_errors.append("❌ No historical months found (format: 'Month YYYY')")
    
    if month_cols:
        # Check for duplicate months
        is_valid, error, dups = validate_no_duplicate_months(month_cols)
        if not is_valid:
            validation_errors.append(f"❌ {error}")
    
    if month_cols and target_col:
        # Check month sequence
        target_dt, target_valid, target_error = validate_target_month_format(target_col)
        if target_valid:
            is_valid, seq_error = validate_month_sequence(month_cols, target_dt)
            if not is_valid:
                validation_errors.append(f"❌ {seq_error}")
    
    return outlet_col, month_cols, target_col, validation_errors


def is_total_row(value):
    """Check if a value represents the total row."""
    if pd.isna(value):
        return False
    value_str = str(value).strip().upper()
    return value_str == 'TOTAL'


def validate_data(df, outlet_col, month_cols):
    """Validate that data is numeric and properly formatted."""
    errors = []
    
    # Check for empty outlet names
    if df[outlet_col].isna().any():
        errors.append("⚠️ Found empty outlet names")
    
    # Check if month columns contain numeric data
    for col in month_cols:
        if not pd.api.types.is_numeric_dtype(df[col]):
            try:
                pd.to_numeric(df[col], errors='coerce')
            except:
                errors.append(f"⚠️ Column '{col}' contains non-numeric values")
    
    return errors


def validate_excel_structure(df, outlet_col_name="OUTLET NAME"):
    """
    Comprehensive validation of Excel file structure BEFORE processing.
    
    Checks:
    - OUTLET NAME column exists
    - TOTAL row exists
    - DIP PLANT outlet exists
    - At least 1 eligible shop exists
    - No empty outlet names
    
    Returns: (is_valid, list_of_errors)
    """
    errors = []
    
    # Check 1: OUTLET NAME column exists
    if outlet_col_name not in df.columns:
        errors.append(f"❌ Column '{outlet_col_name}' not found. First column must be '{outlet_col_name}'")
        return False, errors
    
    # Check 2: TOTAL row exists
    outlet_col_data = df[outlet_col_name].apply(lambda x: str(x).strip().upper() if pd.notna(x) else "")
    has_total = any(val == 'TOTAL' for val in outlet_col_data)
    if not has_total:
        errors.append("❌ TOTAL row not found. Last row must contain 'TOTAL' in outlet column")
    
    # Check 3: DIP PLANT exists
    has_dip_plant = any(val == 'DIP PLANT' for val in outlet_col_data)
    if not has_dip_plant:
        errors.append("❌ DIP PLANT outlet not found. Must have outlet named 'DIP PLANT'")
    
    # Check 4: At least 1 eligible outlet
    non_total_rows = df[~df[outlet_col_name].apply(is_total_row)]
    total_rows = len(non_total_rows)
    eligible_outlets = total_rows - 1  # Minus DIP PLANT if exists
    if eligible_outlets <= 0:
        errors.append(f"❌ No eligible outlets found. Need at least 1 shop (found {total_rows} total outlets)")
    
    # Check 5: No empty outlet names
    if df[outlet_col_name].isna().any() or (df[outlet_col_name] == '').any():
        errors.append("❌ Found empty outlet names. All outlets must have names.")
    
    return len(errors) == 0, errors


def calculate_allocations(df, outlet_col, month_cols, target_col, new_target):
    """
    Calculate day-aware target allocations for 27 shops ONLY.
    
    BUSINESS RULE: DIP PLANT excluded from allocation.
    
    Steps:
    1. Validate DIP PLANT exists
    2. Validate exactly 27 other shops exist
    3. Remove TOTAL row
    4. Temporarily remove DIP PLANT for calculations
    5. Calculate daily averages and contributions for 27 shops
    6. Allocate full target ONLY among 27 shops
    7. Reinsert DIP PLANT with 0 allocation
    
    Returns:
    - result_df: DataFrame with all calculations
    - metadata: Dict with calculation details
    - validation: Dict with validation results
    """
    result_df = df.copy()
    
    # ========== STEP 1: Parse Target Month ==========
    target_dt, target_valid, target_error = validate_target_month_format(target_col)
    if not target_valid:
        return None, {}, {'success': False, 'error': target_error}
    
    target_days, target_is_leap = get_days_in_month(target_dt.year, target_dt.month)
    
    # Calculate total historical days
    total_hist_days, month_details, days_valid, days_error = calculate_total_historical_days(month_cols)
    if not days_valid:
        return None, {}, {'success': False, 'error': days_error}
    
    # ========== STEP 2: Filter - Remove TOTAL Row ==========
    outlet_mask = ~result_df[outlet_col].apply(is_total_row)
    data_only = result_df[outlet_mask].copy()
    
    # ========== STEP 3: DIP PLANT Detection & Validation ==========
    dip_plant_mask = data_only[outlet_col].str.strip().str.upper() == 'DIP PLANT'
    dip_plant_detected = dip_plant_mask.any()
    
    if not dip_plant_detected:
        return None, {}, {'success': False, 'error': '❌ DIP PLANT outlet not found in data'}
    
    dip_plant_idx = dip_plant_mask.idxmax()
    
    # ========== STEP 4: Validate Eligible Shop Count (Dynamic) ==========
    # Total outlets minus DIP PLANT
    total_outlets = len(data_only)
    eligible_shops_count = total_outlets - 1  # All except DIP PLANT
    
    if eligible_shops_count <= 0:
        return None, {}, {
            'success': False,
            'error': f'❌ No eligible shops found. Total outlets: {total_outlets}'
        }
    
    # Debug output
    print(f"📊 ALLOCATION DEBUG INFO:")
    print(f"   Total Outlets: {total_outlets}")
    print(f"   Eligible Shops (excl. DIP PLANT): {eligible_shops_count}")
    print(f"   DIP PLANT Detected: {dip_plant_detected}")
    
    # ========== STEP 5: Separate DIP PLANT and Calculate for Others ==========
    # Create working dataframe with only 27 shops (excludes DIP PLANT)
    shops_only = data_only[~dip_plant_mask].copy()
    
    # Convert to numeric
    for col in month_cols:
        shops_only[col] = pd.to_numeric(shops_only[col], errors='coerce').fillna(0)
    
    # ========== STEP 6: Calculate Historical Sales ==========
    shops_only['Historical_Total_Sales'] = shops_only[month_cols].sum(axis=1)
    
    # ========== STEP 7: Calculate Daily Averages for 27 Shops ==========
    shops_only['Historical_Daily_Average'] = (
        shops_only['Historical_Total_Sales'] / total_hist_days
    ).round(2)
    
    # ========== STEP 8: Calculate Company Daily Average (27 shops only) ==========
    company_daily_average = shops_only['Historical_Daily_Average'].sum()
    
    if company_daily_average <= 0:
        return None, {}, {'success': False, 'error': '❌ Company daily average is zero. Check your data.'}
    
    # ========== STEP 9: Calculate Contribution % for 27 Shops ==========
    shops_only['Contribution_%'] = (
        (shops_only['Historical_Daily_Average'] / company_daily_average * 100)
    ).round(2)
    
    # ========== STEP 10: Allocate Full Target Among 27 Shops ==========
    shops_only['Allocated_Monthly_Target'] = (
        shops_only['Contribution_%'] / 100 * new_target
    ).round(2)
    
    # ========== STEP 11: Calculate Daily Target ==========
    shops_only['Allocated_Daily_Target'] = (
        shops_only['Allocated_Monthly_Target'] / target_days
    ).round(2)
    
    # ========== STEP 12: Validation & Rounding Adjustment ==========
    total_allocated_shops = shops_only['Allocated_Monthly_Target'].sum()
    allocation_difference = new_target - total_allocated_shops
    
    # If rounding causes discrepancy, adjust largest allocation
    if abs(allocation_difference) > 0.01:
        max_idx = shops_only['Allocated_Monthly_Target'].idxmax()
        shops_only.loc[max_idx, 'Allocated_Monthly_Target'] += allocation_difference
        # Recalculate daily target for adjusted outlet
        shops_only.loc[max_idx, 'Allocated_Daily_Target'] = (
            shops_only.loc[max_idx, 'Allocated_Monthly_Target'] / target_days
        ).round(2)
    
    # Final validation
    final_total_shops = shops_only['Allocated_Monthly_Target'].sum()
    validation_passed = abs(final_total_shops - new_target) < 0.01
    
    # ========== STEP 13: Reconstruct Working DataFrame with DIP PLANT ==========
    # Create result with all data
    working_df = data_only.copy()
    
    # Convert to numeric for DIP PLANT row as well (needed for output)
    for col in month_cols:
        working_df[col] = pd.to_numeric(working_df[col], errors='coerce').fillna(0)
    
    # Initialize calculation columns
    working_df['Historical_Total_Sales'] = 0.0
    working_df['Historical_Daily_Average'] = 0.0
    working_df['Contribution_%'] = 0.0
    working_df['Allocated_Monthly_Target'] = 0.0
    working_df['Allocated_Daily_Target'] = 0.0
    
    # Fill in values for eligible shops (dynamic count)
    for idx in shops_only.index:
        working_df.loc[idx, 'Historical_Total_Sales'] = shops_only.loc[idx, 'Historical_Total_Sales']
        working_df.loc[idx, 'Historical_Daily_Average'] = shops_only.loc[idx, 'Historical_Daily_Average']
        working_df.loc[idx, 'Contribution_%'] = shops_only.loc[idx, 'Contribution_%']
        working_df.loc[idx, 'Allocated_Monthly_Target'] = shops_only.loc[idx, 'Allocated_Monthly_Target']
        working_df.loc[idx, 'Allocated_Daily_Target'] = shops_only.loc[idx, 'Allocated_Daily_Target']
    
    # ========== STEP 14: Set DIP PLANT to 0 ==========
    working_df.loc[dip_plant_idx, 'Historical_Total_Sales'] = 0.0
    working_df.loc[dip_plant_idx, 'Historical_Daily_Average'] = 0.0
    working_df.loc[dip_plant_idx, 'Contribution_%'] = 0.0
    working_df.loc[dip_plant_idx, 'Allocated_Monthly_Target'] = 0.0
    working_df.loc[dip_plant_idx, 'Allocated_Daily_Target'] = 0.0
    
    # ========== STEP 15: Prepare Metadata ==========
    metadata = {
        'target_month': target_dt.strftime('%b %Y'),
        'target_days': target_days,
        'target_is_leap': target_is_leap,
        'historical_months': [m['month'] for m in month_details],
        'total_historical_days': total_hist_days,
        'eligible_shops_count': eligible_shops_count,
        'company_total_sales': shops_only['Historical_Total_Sales'].sum(),
        'company_daily_average': round(company_daily_average, 2),
        'entered_target': new_target,
        'final_allocated': round(final_total_shops, 2),
        'rounding_adjustment': round(allocation_difference, 2),
        'dip_plant_note': 'DIP PLANT allocation = 0 (excluded per business rule)'
    }
    
    validation_result = {
        'success': True,
        'validation_passed': validation_passed,
        'error': None,
        'warning': f"Rounding adjustment: ₨ {abs(allocation_difference):.2f}" if abs(allocation_difference) > 0.01 else None
    }
    
    return working_df, metadata, validation_result


def create_output_dataframe(df, working_df, outlet_col, month_cols, target_col, metadata):
    """
    Create final output dataframe with enhanced columns.
    
    Output columns:
    - Outlet Name
    - Historical Total Sales
    - Historical Daily Average
    - Contribution %
    - Allocated Monthly Target
    - Allocated Daily Target
    - All historical months
    - Target column with allocations
    """
    output_df = df.copy()
    
    # Reorder columns: Outlet, Historical Sales/Daily/Contribution, then months, then allocations
    outlet_col_idx = output_df.columns.tolist().index(outlet_col)
    
    # Build new column order
    new_columns = [outlet_col]
    
    # Add calculation columns after outlet name
    calc_cols = [
        ('Historical_Total_Sales', 'Historical Total'),
        ('Historical_Daily_Average', 'Daily Average'),
        ('Contribution_%', 'Contribution %'),
    ]
    
    # Insert calculation columns
    for calc_col, display_name in calc_cols:
        output_df.insert(len(new_columns), display_name, np.nan)
        new_columns.append(display_name)
    
    # Add month columns
    for col in month_cols:
        if col not in new_columns:
            new_columns.append(col)
    
    # Add target allocation columns
    output_df.insert(len(new_columns), 'Allocated_Monthly_Target', np.nan)
    output_df.insert(len(new_columns) + 1, 'Allocated_Daily_Target', np.nan)
    
    # Fill in the calculated values
    outlet_mask = ~output_df[outlet_col].apply(is_total_row)
    
    for idx, wdf_idx in enumerate(working_df.index):
        output_idx = wdf_idx
        
        # Fill calculation columns
        output_df.loc[output_idx, 'Historical Total'] = working_df.loc[wdf_idx, 'Historical_Total_Sales']
        output_df.loc[output_idx, 'Daily Average'] = working_df.loc[wdf_idx, 'Historical_Daily_Average']
        output_df.loc[output_idx, 'Contribution %'] = working_df.loc[wdf_idx, 'Contribution_%']
        output_df.loc[output_idx, 'Allocated_Monthly_Target'] = working_df.loc[wdf_idx, 'Allocated_Monthly_Target']
        output_df.loc[output_idx, 'Allocated_Daily_Target'] = working_df.loc[wdf_idx, 'Allocated_Daily_Target']
    
    # Update target column with allocations
    if target_col and target_col in output_df.columns:
        for idx, wdf_idx in enumerate(working_df.index):
            output_df.loc[wdf_idx, target_col] = working_df.loc[wdf_idx, 'Allocated_Monthly_Target']
    
    # Update TOTAL row
    total_row_idx = None
    for idx, val in enumerate(output_df[outlet_col]):
        if is_total_row(val):
            total_row_idx = idx
            break
    
    if total_row_idx is not None:
        for col in month_cols:
            output_df.loc[total_row_idx, col] = output_df.loc[outlet_mask, col].sum()
        # Add totals for allocations
        output_df.loc[total_row_idx, 'Allocated_Monthly_Target'] = working_df['Allocated_Monthly_Target'].sum()
        output_df.loc[total_row_idx, 'Allocated_Daily_Target'] = working_df['Allocated_Daily_Target'].sum()
    
    return output_df


def export_to_excel(df):
    """Export dataframe to Excel bytes with error handling."""
    try:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Allocations', index=False)
            
            # Format the worksheet
            workbook = writer.book
            worksheet = writer.sheets['Allocations']
            
            # Format currency columns
            currency_format = workbook.add_format({'num_format': '#,##0.00'})
            percent_format = workbook.add_format({'num_format': '0.00"%"'})
            
            for col_num, col_name in enumerate(df.columns, 1):
                if 'Contribution' in col_name or 'Allocated' in col_name or 'Target' in col_name:
                    fmt = currency_format if 'Target' in col_name or 'Allocated' in col_name else percent_format
                    worksheet.set_column(col_num - 1, col_num - 1, 15, fmt)
                else:
                    worksheet.set_column(col_num - 1, col_num - 1, 20)
        
        output.seek(0)
        return output
    
    except Exception as e:
        raise Exception(f"Failed to generate Excel file: {str(e)}")


# ============================================================================
# STREAMLIT APP INTERFACE
# ============================================================================

# Sidebar for file upload
st.sidebar.header("📁 Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload Excel file with sales data",
    type=['xlsx', 'xls', 'csv'],
    help="File should have outlet names in first column and monthly sales data"
)

if uploaded_file is not None:
    try:
        # ====================================================================
        # STEP 1: FILE LOAD WITH ERROR HANDLING
        # ====================================================================
        
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            elif uploaded_file.name.endswith(('.xlsx', '.xls')):
                df = pd.read_excel(uploaded_file)
            else:
                st.error(f"❌ Unsupported file type: {uploaded_file.name}")
                st.stop()
            
            # Validate file is not empty
            if df.empty:
                st.error("❌ File is empty. Please upload a file with data.")
                st.stop()
            
            # Validate minimum rows
            if len(df) < 3:
                st.error("❌ File has too few rows. Need at least: 1 header + 1 DIP PLANT + 1 shop + 1 TOTAL row")
                st.stop()
            
            st.sidebar.success("✅ File loaded successfully!")
        
        except pd.errors.EmptyDataError:
            st.error("❌ File appears corrupted or empty. Please check the file and try again.")
            st.stop()
        except FileNotFoundError:
            st.error("❌ File not found. Please upload the file again.")
            st.stop()
        except Exception as e:
            st.error(f"❌ Failed to load file: {str(e)}")
            st.stop()
        
        # ====================================================================
        # STEP 2: COLUMN CLASSIFICATION
        # ====================================================================
        
        outlet_col, month_cols, target_col, validation_errors = classify_columns(df)
        
        # ====================================================================
        # STEP 3: PRIMARY EXCEL STRUCTURE VALIDATION
        # ====================================================================
        
        is_valid_structure, structure_errors = validate_excel_structure(df, outlet_col)
        if not is_valid_structure:
            st.error("❌ File structure is invalid:")
            for error in structure_errors:
                st.write(f"  {error}")
            st.stop()
        
        st.sidebar.success("✅ File structure validated!")
        
        # Display file info
        st.sidebar.markdown("---")
        st.sidebar.subheader("📋 File Information")
        st.sidebar.write(f"**Outlets:** {len(df[df[outlet_col].apply(lambda x: not is_total_row(x))])}")
        st.sidebar.write(f"**Historical Months:** {len(month_cols)}")
        st.sidebar.write(f"**Outlet Column:** {outlet_col}")
        if target_col:
            st.sidebar.write(f"**Target Column:** {target_col}")
        
        # Display validation errors (if any non-critical issues)
        if validation_errors:
            st.sidebar.warning("Data Validation Notes:")
            for error in validation_errors:
                st.sidebar.write(f"- {error}")
        
        # Display raw data
        st.header("📊 Current Data")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Outlets", len(df[df[outlet_col].apply(lambda x: not is_total_row(x))]))
        with col2:
            st.metric("Historical Months", len(month_cols))
        with col3:
            company_total_all = df[month_cols].sum().sum()
            st.metric("Company Total Sales", f"₨ {company_total_all:,.0f}")
        
        st.dataframe(df, use_container_width=True, height=300)
        
        # Display months and target info
        with st.expander("ℹ️ Column Analysis"):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Historical Months:**")
                for month in month_cols:
                    st.write(f"- {month}")
            with col2:
                if target_col:
                    st.write(f"**Target Column:** {target_col}")
                else:
                    st.write("**Target Column:** Not found (will create new one)")
        
        # ====================================================================
        # TARGET ALLOCATION SECTION
        # ====================================================================
        
        st.markdown("---")
        st.header("🎯 Target Allocation")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            new_target = st.number_input(
                "Enter Monthly Target (PKR)",
                value=3200000.0,
                min_value=1.0,
                step=100000.0,
                help="Enter the target budget for the upcoming month (must be > 0)"
            )
        
        with col2:
            st.write(f"**Target Amount:** ₨ {new_target:,.2f}")
        
        with col3:
            current_outlet_count = len(df[df[outlet_col].apply(lambda x: not is_total_row(x))])
            st.write(f"**Number of Outlets:** {current_outlet_count}")
        
        # Validate target before allowing calculation
        if new_target <= 0:
            st.error("❌ Target must be greater than 0")
        elif new_target is None:
            st.error("❌ Please enter a valid target amount")
        else:
            # Calculate allocations
            if st.button("🔄 Calculate Allocations", key="allocate", type="primary"):
                try:
                    with st.spinner("Calculating allocations..."):
                        working_df, metadata, validation = calculate_allocations(
                            df, outlet_col, month_cols, target_col, new_target
                        )
                    
                    if validation['success']:
                        # Store in session state
                        st.session_state.working_df = working_df
                        st.session_state.metadata = metadata
                        st.session_state.validation = validation
                        st.session_state.new_target = new_target
                        
                        # Show success message
                        st.success(
                            f"✅ Calculation successful!\n\n"
                            f"Target allocated to {metadata['eligible_shops_count']} shops "
                            f"(excluding DIP PLANT)"
                        )
                    else:
                        st.error(f"❌ Calculation failed: {validation['error']}")
                
                except Exception as e:
                    st.error(
                        f"❌ Unexpected error during calculation:\n"
                        f"{str(e)}\n\n"
                        f"Please check your data and try again."
                    )
        
        # Display allocation results if calculated
        if 'working_df' in st.session_state:
            working_df = st.session_state.working_df
            metadata = st.session_state.metadata
            validation = st.session_state.validation
            new_target = st.session_state.new_target
            
            st.markdown("---")
            st.header("✨ Allocation Results")
            
            # Validation status
            if validation['validation_passed']:
                st.success(f"✅ Validation Passed! Total allocation = ₨ {metadata['final_allocated']:,.2f}")
            else:
                if abs(metadata['rounding_adjustment']) > 0.01:
                    st.warning(f"⚠️ Rounding adjustment applied: ₨ {abs(metadata['rounding_adjustment']):.2f}")
                else:
                    st.success(f"✅ Allocation validated!")
            
            # Display DIP PLANT exclusion status
            st.info(
                f"🚫 **DIP PLANT EXCLUDED**\n\n"
                f"Allocation calculated for **{metadata['eligible_shops_count']} shops only** (excluding DIP PLANT)\n"
                f"DIP PLANT allocation = ₨ 0.00"
            )
            
            # ====================================================================
            # SUMMARY METRICS SECTION
            # ====================================================================
            
            st.markdown("---")
            st.subheader("📊 Summary Metrics")
            
            summary_col1, summary_col2, summary_col3, summary_col4 = st.columns(4)
            
            with summary_col1:
                st.metric(
                    "Target Entered",
                    f"₨ {metadata['entered_target']:,.0f}"
                )
            
            with summary_col2:
                delta_text = "✓ Match" if abs(metadata['entered_target'] - metadata['final_allocated']) < 0.01 else "⚠️ Mismatch"
                st.metric(
                    "Total Allocated",
                    f"₨ {metadata['final_allocated']:,.2f}",
                    delta=delta_text
                )
            
            with summary_col3:
                st.metric(
                    "Eligible Shops",
                    metadata['eligible_shops_count'],
                    delta="(excl. DIP PLANT)"
                )
            
            with summary_col4:
                if metadata['eligible_shops_count'] > 0:
                    avg_allocation = metadata['final_allocated'] / metadata['eligible_shops_count']
                    st.metric(
                        "Avg. Per Shop",
                        f"₨ {avg_allocation:,.0f}"
                    )
                else:
                    st.metric("Avg. Per Shop", "N/A")
            
            # Data integrity check
            if abs(metadata['entered_target'] - metadata['final_allocated']) < 0.01:
                st.info("✅ Data integrity verified: Total allocated = Target entered")
            else:
                st.warning(
                    f"⚠️ Minor rounding adjustment: "
                    f"₨ {abs(metadata['entered_target'] - metadata['final_allocated']):.2f}"
                )
            
            # Display metadata
            st.markdown("---")
            st.markdown("### 📊 Calculation Metadata")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Target Month", metadata['target_month'])
            with col2:
                leap_status = "✓ Leap" if metadata['target_is_leap'] else "Regular"
                st.metric("Days in Target", f"{metadata['target_days']} ({leap_status})")
            with col3:
                st.metric("Historical Days", f"{metadata['total_historical_days']} days")
            with col4:
                st.metric("Company Daily Avg", f"₨ {metadata['company_daily_average']:,.0f}")
            
            # Display detailed results table
            st.subheader("📈 Outlet-wise Allocation (Day-Aware)")
            
            display_df = working_df[[
                outlet_col, 
                'Historical_Total_Sales',
                'Historical_Daily_Average',
                'Contribution_%', 
                'Allocated_Monthly_Target',
                'Allocated_Daily_Target'
            ]].copy()
            
            display_df.columns = [
                'Outlet Name',
                'Historical Total',
                'Daily Average',
                'Contribution %',
                'Monthly Target',
                'Daily Target'
            ]
            
            # Format for display
            st.dataframe(
                display_df,
                use_container_width=True,
                column_config={
                    "Historical Total": st.column_config.NumberColumn(format="₨ %,.2f"),
                    "Daily Average": st.column_config.NumberColumn(format="₨ %,.2f"),
                    "Monthly Target": st.column_config.NumberColumn(format="₨ %,.2f"),
                    "Daily Target": st.column_config.NumberColumn(format="₨ %,.2f"),
                    "Contribution %": st.column_config.NumberColumn(format="%.2f%%"),
                }
            )
            
            # Export section
            st.markdown("---")
            st.subheader("💾 Export Updated File")
            
            try:
                output_df = create_output_dataframe(
                    df, working_df, outlet_col, month_cols, target_col, metadata
                )
                
                # Prepare download
                excel_bytes = export_to_excel(output_df)
                
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"Target_Allocation_{timestamp}.xlsx"
                
                st.download_button(
                    label="📥 Download Updated Excel",
                    data=excel_bytes,
                    file_name=filename,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    key="download_excel"
                )
                st.success(f"✅ File ready for download: {filename}")
            
            except Exception as e:
                st.error(f"❌ Failed to generate download file: {str(e)}")
            
            st.info(
                "📌 **Next Steps:**\n\n"
                "1. Download the updated Excel file\n"
                "2. When the month ends, rename the 'Target' column to the month name\n"
                "3. Add a new column for the next month's target\n"
                "4. Upload the file again - the system will automatically detect the new structure!"
            )
    
    except Exception as e:
        st.error(f"❌ Unexpected error: {str(e)}")
        st.write("Please ensure your Excel file has the correct format and try again.")

else:
    # Show instructions when no file is uploaded
    st.info("👈 **Upload an Excel file to get started!**")
    
    with st.expander("📖 File Format Guide"):
        st.markdown("""
        ### Expected Excel Structure:
        
        | OUTLET NAME | July 2025 | Aug 2025 | Sep 2025 | Oct 2025 | ... | Feb 2026 Target |
        |---|---|---|---|---|---|---|
        | Shop 1 | 1,500,000 | 1,600,000 | 1,550,000 | 1,700,000 | ... | |
        | Shop 2 | 2,000,000 | 2,100,000 | 2,050,000 | 2,200,000 | ... | |
        | Shop 3 | 1,200,000 | 1,300,000 | 1,250,000 | 1,400,000 | ... | |
        | ... | | | | | ... | |
        | TOTAL | 4,700,000 | 5,000,000 | 4,850,000 | 5,300,000 | ... | |
        
        ### Requirements:
        - ✅ First column must be **OUTLET NAME**
        - ✅ Monthly columns should follow format: **Month YYYY** (e.g., "July 2025")
        - ✅ Last row should be **TOTAL** (will be ignored in calculations)
        - ✅ Target column should contain **"Target"** in the name
        - ✅ All sales values should be numeric
        
        ### How It Works:
        1. Upload your Excel file
        2. System automatically classifies columns
        3. Enter the target budget for the upcoming month
        4. System calculates each outlet's contribution %
        5. Allocates target proportionally to each outlet
        6. Download updated file with allocations
        7. When month ends, rename target column to month name
        8. Add new target column for next month
        9. Upload again - no code changes needed!
        """)
    
    with st.expander("🔧 Technical Details"):
        st.markdown("""
        ### Calculation Process:
        
        1. **Calculate Historical Total:** Sum of all actual sales for each outlet across all months
        2. **Company Total:** Sum of all outlet historical totals
        3. **Contribution %:** (Outlet Historical Total / Company Total) × 100
        4. **Allocated Target:** (Contribution % / 100) × New Target
        5. **Validation:** Sum of all allocated targets ≈ New target (within 0.01 tolerance)
        6. **Rounding Adjustment:** If discrepancy exists, distributed proportionally
        
        ### Ignored Elements:
        - ✗ TOTAL row
        - ✗ Any column containing "Target"
        - ✗ Non-numeric values
        """)


# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>"
    "🎯 Rolling Monthly Target Allocation System v1.0 | Production Ready"
    "</div>",
    unsafe_allow_html=True
)
