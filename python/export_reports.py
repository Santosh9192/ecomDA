"""
=============================================================================
E-Commerce Sales Analytics - Report Generation & Export
=============================================================================
Description: Export analysis results to Excel, CSV, and PDF formats
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
from typing import Dict, List, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================
RAW_DATA_PATH = os.path.join('data', 'raw')
CLEANED_DATA_PATH = os.path.join('data', 'cleaned')
EXCEL_OUTPUT_PATH = os.path.join('excel', 'reports')
REPORTS_PATH = os.path.join('reports')
PDF_REPORTS_PATH = os.path.join('reports', 'pdf')

# Excel writer configuration
EXCEL_WRITER_OPTIONS = {
    'engine': 'xlsxwriter',
    'options': {'strings_to_numbers': True}
}

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# =============================================================================
# DATA LOADER
# =============================================================================
def load_cleaned_data() -> Dict[str, pd.DataFrame]:
    """
    Load all cleaned datasets.
    
    Returns:
        Dictionary of DataFrames
    """
    logger.info("Loading cleaned data...")
    
    dataframes = {}
    files = {
        'orders': 'orders_cleaned.csv',
        'customers': 'customers_cleaned.csv',
        'regions': 'regions_cleaned.csv',
        'categories': 'categories_cleaned.csv'
    }
    
    for name, filename in files.items():
        path = os.path.join(CLEANED_DATA_PATH, filename)
        if os.path.exists(path):
            dataframes[name] = pd.read_csv(path)
            logger.info(f"  Loaded {name}: {len(dataframes[name]):,} records")
        else:
            # Try raw
            raw_path = os.path.join(RAW_DATA_PATH, filename.replace('_cleaned', ''))
            if os.path.exists(raw_path):
                dataframes[name] = pd.read_csv(raw_path)
                logger.info(f"  Loaded {name} (raw): {len(dataframes[name]):,} records")
    
    return dataframes


# =============================================================================
# REPORT GENERATORS
# =============================================================================
def generate_monthly_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate monthly sales report."""
    logger.info("Generating monthly report...")
    
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    report = df.groupby(df['Order Date'].dt.to_period('M')).agg(
        Order_Count=('Order ID', 'nunique'),
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Order_Value=('Sales', 'mean'),
        Total_Quantity=('Quantity', 'sum'),
        Avg_Discount=('Discount', 'mean'),
        Customer_Count=('Customer ID', 'nunique')
    ).reset_index()
    
    report['Order Date'] = report['Order Date'].astype(str)
    report['Total_Sales'] = report['Total_Sales'].round(2)
    report['Total_Profit'] = report['Total_Profit'].round(2)
    report['Avg_Order_Value'] = report['Avg_Order_Value'].round(2)
    report['Avg_Discount'] = report['Avg_Discount'].round(4)
    report['Profit_Margin_Pct'] = (
        (report['Total_Profit'] / report['Total_Sales']) * 100
    ).round(2)
    
    logger.info(f"  Generated {len(report)} monthly records")
    return report


def generate_quarterly_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate quarterly sales report."""
    logger.info("Generating quarterly report...")
    
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Quarter'] = df['Order Date'].dt.quarter
    df['Year'] = df['Order Date'].dt.year
    
    report = df.groupby(['Year', 'Quarter']).agg(
        Order_Count=('Order ID', 'nunique'),
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Order_Value=('Sales', 'mean'),
        Total_Quantity=('Quantity', 'sum'),
        Customer_Count=('Customer ID', 'nunique')
    ).reset_index()
    
    report['Total_Sales'] = report['Total_Sales'].round(2)
    report['Total_Profit'] = report['Total_Profit'].round(2)
    report['Avg_Order_Value'] = report['Avg_Order_Value'].round(2)
    report['Quarter_Label'] = 'Q' + report['Quarter'].astype(str) + '-' + report['Year'].astype(str)
    
    logger.info(f"  Generated {len(report)} quarterly records")
    return report


def generate_yearly_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate yearly sales report."""
    logger.info("Generating yearly report...")
    
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    
    report = df.groupby(df['Order Date'].dt.year).agg(
        Order_Count=('Order ID', 'nunique'),
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Order_Value=('Sales', 'mean'),
        Total_Quantity=('Quantity', 'sum'),
        Customer_Count=('Customer ID', 'nunique'),
        New_Customers=('Customer ID', lambda x: x.nunique())
    ).reset_index()
    
    report.columns = ['Year', 'Order_Count', 'Total_Sales', 'Total_Profit',
                      'Avg_Order_Value', 'Total_Quantity', 'Customer_Count', 'New_Customers']
    report['Total_Sales'] = report['Total_Sales'].round(2)
    report['Total_Profit'] = report['Total_Profit'].round(2)
    report['Avg_Order_Value'] = report['Avg_Order_Value'].round(2)
    
    logger.info(f"  Generated {len(report)} yearly records")
    return report


def generate_sales_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate detailed sales report."""
    logger.info("Generating sales report...")
    
    report = df.groupby(['Category', 'Sub-Category', 'Product Name']).agg(
        Order_Count=('Order ID', 'nunique'),
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Sale=('Sales', 'mean'),
        Total_Quantity=('Quantity', 'sum'),
        Avg_Discount=('Discount', 'mean')
    ).reset_index()
    
    report['Total_Sales'] = report['Total_Sales'].round(2)
    report['Total_Profit'] = report['Total_Profit'].round(2)
    report['Avg_Sale'] = report['Avg_Sale'].round(2)
    report['Avg_Discount'] = report['Avg_Discount'].round(4)
    report['Profit_Margin_Pct'] = (
        (report['Total_Profit'] / report['Total_Sales']) * 100
    ).round(2)
    
    report = report.sort_values('Total_Sales', ascending=False)
    
    logger.info(f"  Generated {len(report)} sales records")
    return report


def generate_customer_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate customer analysis report."""
    logger.info("Generating customer report...")
    
    report = df.groupby(['Customer ID', 'Customer Name', 'Segment', 'Region']).agg(
        Order_Count=('Order ID', 'nunique'),
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Order_Value=('Sales', 'mean'),
        Total_Quantity=('Quantity', 'sum')
    ).reset_index()
    
    report['Total_Sales'] = report['Total_Sales'].round(2)
    report['Total_Profit'] = report['Total_Profit'].round(2)
    report['Avg_Order_Value'] = report['Avg_Order_Value'].round(2)
    report['Customer_LTV'] = report['Total_Sales'].round(2)
    
    report = report.sort_values('Total_Sales', ascending=False)
    
    logger.info(f"  Generated {len(report)} customer records")
    return report


def generate_regional_report(df: pd.DataFrame) -> pd.DataFrame:
    """Generate regional performance report."""
    logger.info("Generating regional report...")
    
    report = df.groupby(['Region', 'State', 'City']).agg(
        Order_Count=('Order ID', 'nunique'),
        Customer_Count=('Customer ID', 'nunique'),
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Avg_Order_Value=('Sales', 'mean'),
        Total_Quantity=('Quantity', 'sum')
    ).reset_index()
    
    report['Total_Sales'] = report['Total_Sales'].round(2)
    report['Total_Profit'] = report['Total_Profit'].round(2)
    report['Avg_Order_Value'] = report['Avg_Order_Value'].round(2)
    
    report = report.sort_values('Total_Sales', ascending=False)
    
    logger.info(f"  Generated {len(report)} regional records")
    return report


# =============================================================================
# EXCEL REPORT GENERATION
# =============================================================================
def generate_excel_reports(orders_df: pd.DataFrame, 
                           export_dir: str = EXCEL_OUTPUT_PATH) -> str:
    """
    Generate comprehensive Excel report with multiple sheets.
    
    Args:
        orders_df: Orders DataFrame
        export_dir: Output directory
        
    Returns:
        Path to the generated Excel file
    """
    logger.info("\n" + "=" * 50)
    logger.info("GENERATING EXCEL REPORTS")
    logger.info("=" * 50)
    
    os.makedirs(export_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    excel_path = os.path.join(export_dir, f'Ecommerce_Reports_{timestamp}.xlsx')
    
    # Generate all reports
    reports = {
        'Monthly Report': generate_monthly_report(orders_df),
        'Quarterly Report': generate_quarterly_report(orders_df),
        'Yearly Report': generate_yearly_report(orders_df),
        'Sales Report': generate_sales_report(orders_df),
        'Customer Report': generate_customer_report(orders_df),
        'Regional Report': generate_regional_report(orders_df)
    }
    
    # Write to Excel with formatting
    with pd.ExcelWriter(excel_path, engine='xlsxwriter') as writer:
        workbook = writer.book
        
        # Create formats
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#2E86AB',
            'font_color': 'white',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'font_size': 11
        })
        
        currency_format = workbook.add_format({
            'num_format': '$#,##0.00',
            'border': 1
        })
        
        percentage_format = workbook.add_format({
            'num_format': '0.00%',
            'border': 1
        })
        
        int_format = workbook.add_format({
            'num_format': '#,##0',
            'border': 1
        })
        
        title_format = workbook.add_format({
            'bold': True,
            'font_size': 16,
            'font_color': '#2E86AB',
            'bottom': 2,
            'bottom_color': '#2E86AB'
        })
        
        # Write each report as a separate sheet
        for sheet_name, report_df in reports.items():
            # Truncate sheet name to 31 chars (Excel limit)
            safe_sheet_name = sheet_name[:31]
            
            # Write title
            report_df.to_excel(writer, sheet_name=safe_sheet_name, 
                              index=False, startrow=2)
            
            worksheet = writer.sheets[safe_sheet_name]
            
            # Write title
            worksheet.merge_range(0, 0, 0, len(report_df.columns) - 1,
                                 f'E-Commerce {sheet_name}', title_format)
            
            # Write date
            date_format = workbook.add_format({'italic': True, 'font_size': 10})
            worksheet.write(1, 0, f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 
                          date_format)
            
            # Format headers
            for col_idx, col_name in enumerate(report_df.columns):
                worksheet.write(2, col_idx, col_name.replace('_', ' ').title(), 
                              header_format)
            
            # Format data columns
            for col_idx, col_name in enumerate(report_df.columns):
                if any(x in col_name.lower() for x in ['sales', 'profit', 'value', 'revenue', 'ltv']):
                    worksheet.set_column(col_idx, col_idx, 15, currency_format)
                elif any(x in col_name.lower() for x in ['margin', 'discount', 'rate']):
                    worksheet.set_column(col_idx, col_idx, 12, percentage_format)
                elif any(x in col_name.lower() for x in ['count', 'quantity', 'number']):
                    worksheet.set_column(col_idx, col_idx, 12, int_format)
                else:
                    worksheet.set_column(col_idx, col_idx, 15)
            
            # Set column widths
            worksheet.set_column(0, 0, 18)
            
            # Add autofilter
            worksheet.autofilter(2, 0, 2 + len(report_df), len(report_df.columns) - 1)
        
        # Add a summary sheet with KPIs
        kpi_data = {
            'KPI': ['Total Sales', 'Total Profit', 'Profit Margin', 'Total Orders',
                   'Total Customers', 'Avg Order Value', 'Avg Discount', 'Total Quantity'],
            'Value': [
                f'${orders_df["Sales"].sum():,.2f}',
                f'${orders_df["Profit"].sum():,.2f}',
                f'{(orders_df["Profit"].sum() / orders_df["Sales"].sum() * 100):.2f}%',
                f'{orders_df["Order ID"].nunique():,}',
                f'{orders_df["Customer ID"].nunique():,}',
                f'${orders_df["Sales"].sum() / orders_df["Order ID"].nunique():,.2f}',
                f'{orders_df["Discount"].mean() * 100:.2f}%',
                f'{int(orders_df["Quantity"].sum()):,}'
            ]
        }
        kpi_df = pd.DataFrame(kpi_data)
        kpi_df.to_excel(writer, sheet_name='Dashboard Summary', index=False, startrow=1)
        
        kpi_worksheet = writer.sheets['Dashboard Summary']
        kpi_worksheet.merge_range(0, 0, 0, 1, 'E-Commerce KPI Dashboard Summary', title_format)
        for col_idx, col_name in enumerate(kpi_df.columns):
            kpi_worksheet.write(1, col_idx, col_name, header_format)
    
    logger.info(f"Excel report saved: {excel_path}")
    return excel_path


# =============================================================================
# CSV EXPORT
# =============================================================================
def export_csv_reports(orders_df: pd.DataFrame, 
                       export_dir: str = REPORTS_PATH) -> List[str]:
    """
    Export reports to CSV format.
    
    Args:
        orders_df: Orders DataFrame
        export_dir: Output directory
        
    Returns:
        List of generated file paths
    """
    logger.info("\n" + "=" * 50)
    logger.info("EXPORTING CSV REPORTS")
    logger.info("=" * 50)
    
    os.makedirs(export_dir, exist_ok=True)
    generated_files = []
    
    reports = {
        'monthly_report': generate_monthly_report(orders_df),
        'quarterly_report': generate_quarterly_report(orders_df),
        'yearly_report': generate_yearly_report(orders_df),
        'sales_report': generate_sales_report(orders_df),
        'customer_report': generate_customer_report(orders_df),
        'regional_report': generate_regional_report(orders_df)
    }
    
    for report_name, report_df in reports.items():
        filepath = os.path.join(export_dir, f'{report_name}.csv')
        report_df.to_csv(filepath, index=False)
        generated_files.append(filepath)
        logger.info(f"  Exported: {filepath}")
    
    return generated_files


# =============================================================================
# SUMMARY STATISTICS EXPORT
# =============================================================================
def export_summary_statistics(orders_df: pd.DataFrame,
                              export_dir: str = PDF_REPORTS_PATH) -> str:
    """
    Generate summary statistics text report.
    
    Args:
        orders_df: Orders DataFrame
        export_dir: Output directory
        
    Returns:
        Path to the summary file
    """
    logger.info("\n" + "=" * 50)
    logger.info("GENERATING SUMMARY STATISTICS")
    logger.info("=" * 50)
    
    os.makedirs(export_dir, exist_ok=True)
    
    lines = []
    lines.append("=" * 70)
    lines.append("E-COMMERCE SALES ANALYTICS - SUMMARY REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"Data Period: {orders_df['Order Date'].min()} to {orders_df['Order Date'].max()}")
    lines.append("=" * 70)
    
    lines.append("\n1. EXECUTIVE SUMMARY")
    lines.append("-" * 40)
    lines.append(f"  Total Sales:          ${orders_df['Sales'].sum():>12,.2f}")
    lines.append(f"  Total Profit:         ${orders_df['Profit'].sum():>12,.2f}")
    lines.append(f"  Profit Margin:        {(orders_df['Profit'].sum() / orders_df['Sales'].sum() * 100):>11.2f}%")
    lines.append(f"  Total Orders:         {orders_df['Order ID'].nunique():>15,}")
    lines.append(f"  Total Customers:      {orders_df['Customer ID'].nunique():>15,}")
    lines.append(f"  Total Items Sold:     {int(orders_df['Quantity'].sum()):>15,}")
    
    lines.append("\n2. CUSTOMER METRICS")
    lines.append("-" * 40)
    lines.append(f"  Avg Order Value:      ${orders_df['Sales'].sum() / orders_df['Order ID'].nunique():>11,.2f}")
    lines.append(f"  Avg Orders/Customer:  {orders_df.groupby('Customer ID')['Order ID'].nunique().mean():>11.2f}")
    lines.append(f"  Avg Revenue/Customer: ${orders_df.groupby('Customer ID')['Sales'].sum().mean():>11,.2f}")
    
    lines.append("\n3. PRODUCT METRICS")
    lines.append("-" * 40)
    top_cat = orders_df.groupby('Category')['Sales'].sum().idxmax()
    top_prod = orders_df.groupby('Product Name')['Sales'].sum().idxmax()
    lines.append(f"  Top Category:         {top_cat}")
    lines.append(f"  Top Product:          {top_prod}")
    
    lines.append("\n4. REGIONAL METRICS")
    lines.append("-" * 40)
    top_region = orders_df.groupby('Region')['Sales'].sum().idxmax()
    lines.append(f"  Top Region:           {top_region}")
    
    lines.append("\n5. OPERATIONAL METRICS")
    lines.append("-" * 40)
    lines.append(f"  Avg Discount:         {orders_df['Discount'].mean() * 100:.2f}%")
    lines.append(f"  Avg Shipping Cost:    ${orders_df['Shipping Cost'].mean():.2f}")
    
    if 'Return Status' in orders_df.columns:
        return_rate = (orders_df['Return Status'] == 'Returned').mean() * 100
        lines.append(f"  Return Rate:          {return_rate:.2f}%")
    
    lines.append("\n" + "=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)
    
    summary_text = '\n'.join(lines)
    
    filepath = os.path.join(export_dir, 'summary_report.txt')
    with open(filepath, 'w') as f:
        f.write(summary_text)
    
    logger.info(f"Summary report saved: {filepath}")
    return filepath


# =============================================================================
# ALL-IN-ONE EXPORT
# =============================================================================
def export_all_reports(orders_df: pd.DataFrame) -> Dict[str, str]:
    """
    Export all reports in all formats.
    
    Args:
        orders_df: Orders DataFrame
        
    Returns:
        Dictionary of report types to file paths
    """
    logger.info("\n" + "=" * 60)
    logger.info("EXPORTING ALL REPORTS")
    logger.info("=" * 60)
    
    results = {}
    
    # Excel reports
    excel_path = generate_excel_reports(orders_df)
    results['excel'] = excel_path
    
    # CSV reports
    csv_files = export_csv_reports(orders_df)
    results['csv'] = csv_files
    
    # Summary statistics
    summary_path = export_summary_statistics(orders_df)
    results['summary'] = summary_path
    
    return results


# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    """Main entry point for report generation."""
    logger.info("=" * 60)
    logger.info("REPORT GENERATION ENGINE STARTED")
    logger.info("=" * 60)
    
    # Load data
    data = load_cleaned_data()
    
    if 'orders' not in data:
        logger.error("Orders data not found. Aborting.")
        return
    
    orders_df = data['orders']
    
    # Ensure date is datetime
    if 'Order Date' in orders_df.columns:
        orders_df['Order Date'] = pd.to_datetime(orders_df['Order Date'])
    
    # Generate all reports
    results = export_all_reports(orders_df)
    
    # Print summary
    print("\n" + "=" * 60)
    print("REPORT GENERATION COMPLETE")
    print("=" * 60)
    
    for report_type, paths in results.items():
        if isinstance(paths, list):
            print(f"\n  {report_type.upper()}:")
            for path in paths:
                print(f"    - {path}")
        else:
            print(f"\n  {report_type.upper()}: {paths}")
    
    return results


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    main()
