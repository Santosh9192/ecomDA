"""
=============================================================================
E-Commerce Sales Analytics - Data Cleaning Pipeline
=============================================================================
Description: Clean, transform, and preprocess raw e-commerce data
Author: Business Analytics Team
Version: 1.0
Python: 3.8+
=============================================================================
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime
import logging
from typing import Dict, List

# =============================================================================
# CONFIGURATION
# =============================================================================
RAW_DATA_PATH = os.path.join('data', 'raw')
CLEANED_DATA_PATH = os.path.join('data', 'cleaned')
CUSTOMER_FILE = 'customers.csv'
ORDERS_FILE = 'ecommerce_orders.csv'
REGIONS_FILE = 'regions.csv'
CATEGORIES_FILE = 'categories.csv'

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


# =============================================================================
# DATA LOADER
# =============================================================================
def load_raw_data(data_dir: str = RAW_DATA_PATH) -> Dict[str, pd.DataFrame]:
    """Load all raw CSV data files into a dictionary of DataFrames."""
    logger.info(f"Loading raw data from {data_dir}...")

    data_files = {
        'customers': os.path.join(data_dir, CUSTOMER_FILE),
        'orders': os.path.join(data_dir, ORDERS_FILE),
        'regions': os.path.join(data_dir, REGIONS_FILE),
        'categories': os.path.join(data_dir, CATEGORIES_FILE)
    }

    dataframes = {}
    for name, filepath in data_files.items():
        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            dataframes[name] = df
            logger.info(f"  Loaded {name}: {len(df):,} records from {filepath}")
        else:
            logger.warning(f"  File not found: {filepath}")
            dataframes[name] = pd.DataFrame()

    return dataframes


# =============================================================================
# MISSING VALUE HANDLING
# =============================================================================
def handle_missing_values(df: pd.DataFrame, df_name: str) -> pd.DataFrame:
    """
    Detect and handle missing values in the dataset.

    Strategy:
    - Drop columns with >50% missing values
    - Fill numeric columns with median
    - Fill categorical columns with mode
    - Drop rows with critical missing values (Order ID, Customer ID, etc.)
    """
    logger.info(f"\n{'='*50}")
    logger.info(f"Handling missing values for: {df_name}")
    logger.info(f"{'='*50}")

    df_clean = df.copy()

    # Report initial missing values
    initial_missing = df_clean.isnull().sum()
    if initial_missing.sum() > 0:
        logger.info(f"Initial missing values: {initial_missing.sum()}")
        missing_details = initial_missing[initial_missing > 0]
        for col, count in missing_details.items():
            logger.info(f"  {col}: {count} missing ({count/len(df_clean)*100:.2f}%)")
    else:
        logger.info("No missing values found.")
        return df_clean

    # Drop columns with >50% missing values
    threshold = len(df_clean) * 0.5
    cols_to_drop = df_clean.columns[df_clean.isnull().sum() > threshold].tolist()
    if cols_to_drop:
        logger.info(f"Dropping columns with >50% missing: {cols_to_drop}")
        df_clean.drop(columns=cols_to_drop, inplace=True)

    # Critical columns that must not have missing values
    critical_cols = {
        'customers': ['Customer ID', 'Customer Name'],
        'orders': ['Order ID', 'Order Date', 'Customer ID'],
        'regions': ['Region', 'State'],
        'categories': ['Category', 'Sub-Category']
    }

    critical = critical_cols.get(df_name, [])
    for col in critical:
        if col in df_clean.columns and df_clean[col].isnull().any():
            null_count = df_clean[col].isnull().sum()
            logger.warning(f"Dropping {null_count} rows with missing critical column: {col}")
            df_clean.dropna(subset=[col], inplace=True)

    # Fill remaining numeric columns with median
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df_clean[col].isnull().any():
            median_val = df_clean[col].median()
            df_clean[col] = df_clean[col].fillna(median_val)
            logger.info(f"  Filled {col} missing values with median: {median_val:.2f}")

    # Fill categorical columns with mode
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    for col in categorical_cols:
        if df_clean[col].isnull().any():
            mode_val = df_clean[col].mode()[0]
            df_clean[col] = df_clean[col].fillna(mode_val)
            logger.info(f"  Filled {col} missing values with mode: {mode_val}")

    logger.info(f"Missing values after cleaning: {df_clean.isnull().sum().sum()}")
    return df_clean


# =============================================================================
# DUPLICATE DETECTION & REMOVAL
# =============================================================================
def remove_duplicates(df: pd.DataFrame, df_name: str,
                     subset: List[str] = None) -> pd.DataFrame:
    """Detect and remove duplicate records."""
    logger.info(f"\n{'='*50}")
    logger.info(f"Checking duplicates for: {df_name}")
    logger.info(f"{'='*50}")

    df_clean = df.copy()

    exact_dupes = df_clean.duplicated(keep='first').sum()
    if exact_dupes > 0:
        logger.info(f"Found {exact_dupes} exact duplicate rows")
        df_clean.drop_duplicates(keep='first', inplace=True)
    else:
        logger.info("No exact duplicates found.")

    if subset:
        subset_dupes = df_clean.duplicated(subset=subset, keep='first').sum()
        if subset_dupes > 0:
            logger.info(f"Found {subset_dupes} duplicates based on {subset}")
            df_clean.drop_duplicates(subset=subset, keep='first', inplace=True)

    logger.info(f"Records after deduplication: {len(df_clean):,}")
    return df_clean


# =============================================================================
# OUTLIER DETECTION & HANDLING
# =============================================================================
def detect_and_handle_outliers(df: pd.DataFrame, columns: List[str] = None,
                               method: str = 'iqr', threshold: float = 1.5) -> pd.DataFrame:
    """Detect and handle outliers using IQR or Z-score method."""
    logger.info(f"\n{'='*50}")
    logger.info(f"Outlier Detection ({method.upper()}, threshold={threshold})")
    logger.info(f"{'='*50}")

    df_clean = df.copy()

    if columns is None:
        columns = df_clean.select_dtypes(include=[np.number]).columns.tolist()

    columns = [col for col in columns
               if not any(x in col.lower() for x in ['id', 'index', 'year', 'month'])]

    for col in columns:
        if df_clean[col].nunique() < 5:
            continue

        if method == 'iqr':
            Q1 = df_clean[col].quantile(0.25)
            Q3 = df_clean[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR

            outliers = df_clean[(df_clean[col] < lower_bound) |
                               (df_clean[col] > upper_bound)][col]

            if len(outliers) > 0:
                logger.info(f"  {col}: {len(outliers)} outliers detected "
                           f"(bounds: {lower_bound:.2f}, {upper_bound:.2f})")
                df_clean[col] = df_clean[col].clip(lower_bound, upper_bound)
                logger.info(f"    Capped at [{lower_bound:.2f}, {upper_bound:.2f}]")

        elif method == 'zscore':
            z_scores = np.abs((df_clean[col] - df_clean[col].mean()) /
                             df_clean[col].std())
            outliers_count = (z_scores > threshold).sum()

            if outliers_count > 0:
                logger.info(f"  {col}: {outliers_count} outliers detected (Z>{threshold})")
                mean = df_clean[col].mean()
                std = df_clean[col].std()
                df_clean[col] = df_clean[col].clip(mean - threshold * std,
                                                   mean + threshold * std)

    return df_clean


# =============================================================================
# FEATURE ENGINEERING
# =============================================================================
def engineer_features(orders_df: pd.DataFrame) -> pd.DataFrame:
    """Create new features from existing data for deeper analysis."""
    logger.info(f"\n{'='*50}")
    logger.info("Feature Engineering")
    logger.info(f"{'='*50}")

    df = orders_df.copy()

    date_cols = ['Order Date', 'Ship Date']
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    if 'Order Date' in df.columns:
        df['Order Year'] = df['Order Date'].dt.year
        df['Order Month'] = df['Order Date'].dt.month
        df['Order Quarter'] = df['Order Date'].dt.quarter
        df['Order Weekday'] = df['Order Date'].dt.weekday
        df['Order Month Name'] = df['Order Date'].dt.strftime('%B')
        df['Order Quarter Label'] = 'Q' + df['Order Quarter'].astype(str) + \
                                     '-' + df['Order Year'].astype(str)

        df['Is Weekend'] = df['Order Weekday'].isin([5, 6]).astype(int)

        df['Season'] = df['Order Month'].apply(
            lambda x: 'Holiday' if x in [11, 12]
            else 'Spring' if x in [3, 4, 5]
            else 'Summer' if x in [6, 7, 8]
            else 'Fall'
        )

        logger.info("  [OK] Time-based features created (Year, Month, Quarter, etc.)")

    if 'Order Date' in df.columns and 'Ship Date' in df.columns:
        df['Delivery Days'] = (df['Ship Date'] - df['Order Date']).dt.days
        df['Delivery Days'] = df['Delivery Days'].clip(0, 30)
        df['Is Delayed'] = (df['Delivery Days'] > 7).astype(int)
        logger.info("  [OK] Delivery features created")

    if 'Sales' in df.columns and 'Profit' in df.columns:
        df['Profit Margin %'] = np.where(
            df['Sales'] > 0,
            (df['Profit'] / df['Sales'] * 100).round(2),
            0
        )

        if 'Discount' in df.columns:
            df['Discount Amount'] = (df['Sales'] * df['Discount']).round(2)
            logger.info("  [OK] Discount amount calculated")

        df['Profit Category'] = pd.cut(
            df['Profit Margin %'],
            bins=[-float('inf'), 0, 10, 20, float('inf')],
            labels=['Loss', 'Low Margin', 'Medium Margin', 'High Margin']
        )

        logger.info("  [OK] Financial features created (Margin, Categories)")

    if 'Sales' in df.columns:
        df['Sales Bucket'] = pd.cut(
            df['Sales'],
            bins=[0, 50, 100, 250, 500, 1000, float('inf')],
            labels=['Under $50', '$50-$100', '$101-$250', '$251-$500',
                   '$501-$1000', 'Over $1000']
        )
        logger.info("  [OK] Price bucketing completed")

    if 'Return Status' in df.columns:
        df['Is Returned'] = (df['Return Status'] == 'Returned').astype(int)
        logger.info("  [OK] Return indicators created")

    if 'Registration Date' in df.columns:
        df['Registration Date'] = pd.to_datetime(df['Registration Date'], errors='coerce')
        ref_date = df['Order Date'].max() if 'Order Date' in df.columns else datetime.now()
        df['Customer Tenure Days'] = (ref_date - df['Registration Date']).dt.days
        logger.info("  [OK] Customer tenure calculated")

    logger.info(f"Total features after engineering: {df.shape[1]}")
    return df


# =============================================================================
# DATA TYPE STANDARDIZATION
# =============================================================================
def standardize_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """Standardize data types across the dataset for consistency."""
    df_clean = df.copy()

    str_cols = df_clean.select_dtypes(include=['object', 'str']).columns
    for col in str_cols:
        if df_clean[col].dtype in ['object', 'str']:
            df_clean[col] = df_clean[col].astype(str).str.strip()

    numeric_patterns = ['Sales', 'Profit', 'Discount', 'Quantity', 'Price', 'Cost']
    for col in df_clean.columns:
        if any(pattern in col for pattern in numeric_patterns):
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')

    bool_cols = [col for col in df_clean.columns if col.startswith('Is ')]
    for col in bool_cols:
        df_clean[col] = df_clean[col].astype(int)

    return df_clean


# =============================================================================
# DATA QUALITY REPORT GENERATION
# =============================================================================
def generate_quality_report(df: pd.DataFrame, df_name: str,
                            output_dir: str = CLEANED_DATA_PATH) -> Dict:
    """Generate a comprehensive data quality report."""
    report = {
        'dataset': df_name,
        'total_records': len(df),
        'total_columns': len(df.columns),
        'memory_usage_mb': round(df.memory_usage(deep=True).sum() / 1024 / 1024, 2),
        'column_details': [],
        'completeness_score': round(100 - (df.isnull().sum().sum() /
                                      (df.shape[0] * df.shape[1]) * 100), 2)
    }

    for col in df.columns:
        col_info = {
            'name': col,
            'dtype': str(df[col].dtype),
            'non_null_count': int(df[col].notna().sum()),
            'null_count': int(df[col].isna().sum()),
            'null_percent': round(float(df[col].isna().sum() / len(df) * 100), 2),
            'unique_count': int(df[col].nunique())
        }

        if df[col].dtype in ['int64', 'float64', 'Int64', 'Float64']:
            col_info.update({
                'min': float(df[col].min()) if df[col].notna().any() else None,
                'max': float(df[col].max()) if df[col].notna().any() else None,
                'mean': float(df[col].mean()) if df[col].notna().any() else None,
                'median': float(df[col].median()) if df[col].notna().any() else None,
                'std': float(df[col].std()) if df[col].notna().any() else None
            })

        report['column_details'].append(col_info)

    report_df = pd.DataFrame(report['column_details'])
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f'{df_name}_quality_report.csv')
    report_df.to_csv(report_path, index=False)
    logger.info(f"Quality report saved to: {report_path}")

    return report


# =============================================================================
# MAIN CLEANING PIPELINE
# =============================================================================
def run_cleaning_pipeline(input_dir: str = RAW_DATA_PATH,
                          output_dir: str = CLEANED_DATA_PATH) -> Dict[str, pd.DataFrame]:
    """Execute the complete data cleaning pipeline."""
    start_time = datetime.now()
    logger.info("=" * 60)
    logger.info("DATA CLEANING PIPELINE STARTED")
    logger.info(f"Input: {input_dir}")
    logger.info(f"Output: {output_dir}")
    logger.info("=" * 60)

    logger.info("\n[Step 1/6] Loading raw data...")
    raw_data = load_raw_data(input_dir)

    cleaned_data = {}

    for name, df in raw_data.items():
        if len(df) == 0:
            logger.warning(f"Skipping {name}: empty dataset")
            continue

        logger.info(f"\n{'#'*50}")
        logger.info(f"Processing: {name.upper()}")
        logger.info(f"{'#'*50}")

        logger.info(f"\n[Step 2/6] Handling missing values...")
        df = handle_missing_values(df, name)

        logger.info(f"\n[Step 3/6] Removing duplicates...")
        if name == 'orders':
            df = remove_duplicates(df, name, subset=['Order ID'])
        elif name == 'customers':
            df = remove_duplicates(df, name, subset=['Customer ID'])
        else:
            df = remove_duplicates(df, name)

        if name == 'orders':
            logger.info(f"\n[Step 4/6] Detecting and handling outliers...")
            numeric_cols = ['Sales', 'Profit', 'Quantity', 'Shipping Cost']
            df = detect_and_handle_outliers(df, numeric_cols, method='iqr')

        if name == 'orders':
            logger.info(f"\n[Step 5/6] Engineering features...")
            df = engineer_features(df)

        logger.info(f"\n[Step 6/6] Standardizing data types...")
        df = standardize_dtypes(df)

        generate_quality_report(df, name, output_dir)

        os.makedirs(output_dir, exist_ok=True)
        output_file = os.path.join(output_dir, f'{name}_cleaned.csv')
        df.to_csv(output_file, index=False)
        logger.info(f"\nSaved cleaned {name} to: {output_file}")

        cleaned_data[name] = df

    duration = (datetime.now() - start_time).total_seconds()
    logger.info("\n" + "=" * 60)
    logger.info("DATA CLEANING PIPELINE COMPLETED")
    logger.info(f"Duration: {duration:.2f} seconds")
    logger.info("=" * 60)

    for name, df in cleaned_data.items():
        logger.info(f"  {name}: {len(df):,} records, {len(df.columns)} columns")

    return cleaned_data


# =============================================================================
# MAIN EXECUTION
# =============================================================================
if __name__ == '__main__':
    """Main entry point for the data cleaning pipeline."""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)

    cleaned_dfs = run_cleaning_pipeline()

    print("\n" + "=" * 60)
    print("DATA CLEANING COMPLETE")
    print("=" * 60)
    for name, df in cleaned_dfs.items():
        print(f"  [OK] {name}: {len(df):,} records -> data/cleaned/{name}_cleaned.csv")
