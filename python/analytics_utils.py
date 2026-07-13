"""
=============================================================================
E-Commerce Sales Analytics - Shared Utility Functions
=============================================================================
Description: Common data loading, KPI calculation, filters, and helper
             functions shared between dashboard.py and web_app.py.
=============================================================================
"""

import pandas as pd
import numpy as np
import os
from typing import Dict, Any, Optional
from functools import lru_cache

# =============================================================================
# PATHS
# =============================================================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'cleaned', 'orders_cleaned.csv')
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ecommerce_orders.csv')


# =============================================================================
# DATA LOADING
# =============================================================================
@lru_cache(maxsize=1)
def load_data() -> pd.DataFrame:
    """
    Load cleaned e-commerce data (cached). Falls back to raw CSV.
    
    Returns:
        DataFrame with order data, or empty DataFrame if no data found.
    """
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    elif os.path.exists(RAW_DATA_PATH):
        df = pd.read_csv(RAW_DATA_PATH)
    else:
        return pd.DataFrame()
    
    for col in ['Order Date', 'Ship Date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df


def get_filtered_data(year=None, category=None, region=None, segment=None, shipping=None) -> pd.DataFrame:
    """
    Load data and apply filters.
    
    Args:
        year: Filter by year (int or 'All')
        category: Filter by product category (str or 'All')
        region: Filter by geographic region (str or 'All')
        segment: Filter by customer segment (str or 'All')
        shipping: Filter by shipping mode (str or 'All')
    
    Returns:
        Filtered DataFrame
    """
    df = load_data()
    if df.empty:
        return df
    
    if year and year != 'All':
        df = df[df['Order Date'].dt.year == int(year)]
    if category and category != 'All':
        df = df[df['Category'] == category]
    if region and region != 'All':
        df = df[df['Region'] == region]
    if segment and segment != 'All':
        df = df[df['Segment'] == segment]
    if shipping and shipping != 'All':
        df = df[df['Shipping Mode'] == shipping]
    
    return df


# =============================================================================
# KPI CALCULATION
# =============================================================================
def calculate_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate all key business KPIs from the dataset.
    
    Args:
        df: Orders DataFrame
    
    Returns:
        Dictionary of KPI names to values
    """
    if df.empty:
        return {}
    
    total_sales = float(df['Sales'].sum())
    total_profit = float(df['Profit'].sum())
    total_orders = int(df['Order ID'].nunique())
    total_customers = int(df['Customer ID'].nunique())
    total_items = int(df['Quantity'].sum())
    profit_margin = round((total_profit / total_sales * 100), 2) if total_sales > 0 else 0
    aov = round(total_sales / total_orders, 2) if total_orders > 0 else 0
    return_rate = round(float((df['Return Status'] == 'Returned').mean() * 100), 2)
    repeat_rate = round(float(
        (df.groupby('Customer ID')['Order ID'].nunique() > 1).mean() * 100
    ), 2) if total_customers > 0 else 0
    
    category_sales = df.groupby('Category')['Sales'].sum()
    region_sales = df.groupby('Region')['Sales'].sum()
    product_sales = df.groupby('Product Name')['Sales'].sum()
    customer_sales = df.groupby('Customer Name')['Sales'].sum()
    
    avg_orders_per_customer = round(float(
        df.groupby('Customer ID')['Order ID'].nunique().mean()
    ), 2)
    avg_revenue_per_customer = round(float(
        df.groupby('Customer ID')['Sales'].sum().mean()
    ), 2)
    avg_items_per_order = round(float(total_items / total_orders), 2) if total_orders > 0 else 0
    
    return {
        'Total Sales': f"${total_sales:,.2f}",
        'Total Profit': f"${total_profit:,.2f}",
        'Profit Margin': f"{profit_margin:.1f}%",
        'Total Orders': f"{total_orders:,}",
        'Total Customers': f"{total_customers:,}",
        'Total Items Sold': f"{total_items:,}",
        'Avg Order Value': f"${aov:,.2f}",
        'Avg Orders/Customer': f"{avg_orders_per_customer:.1f}",
        'Avg Revenue/Customer': f"${avg_revenue_per_customer:,.2f}",
        'Return Rate': f"{return_rate:.1f}%",
        'Repeat Purchase Rate': f"{repeat_rate:.1f}%",
        'Top Category': str(category_sales.idxmax()) if not category_sales.empty else 'N/A',
        'Top Region': str(region_sales.idxmax()) if not region_sales.empty else 'N/A',
        'Top Product': str(product_sales.idxmax()) if not product_sales.empty else 'N/A',
        'Top Customer': str(customer_sales.idxmax()) if not customer_sales.empty else 'N/A',
    }


def calculate_numeric_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate KPIs as numeric values (for API use).
    
    Args:
        df: Orders DataFrame
    
    Returns:
        Dictionary of KPI names to numeric values
    """
    if df.empty:
        return {}
    
    total_sales = float(df['Sales'].sum())
    total_profit = float(df['Profit'].sum())
    total_orders = int(df['Order ID'].nunique())
    total_customers = int(df['Customer ID'].nunique())
    total_items = int(df['Quantity'].sum())
    profit_margin = round((total_profit / total_sales * 100), 2) if total_sales > 0 else 0
    aov = round(total_sales / total_orders, 2) if total_orders > 0 else 0
    return_rate = round(float((df['Return Status'] == 'Returned').mean() * 100), 2)
    avg_discount = round(float(df['Discount'].mean()), 4)
    avg_shipping = round(float(df['Shipping Cost'].mean() if 'Shipping Cost' in df.columns else 0), 2)
    repeat_rate = round(float(
        (df.groupby('Customer ID')['Order ID'].nunique() > 1).mean() * 100
    ), 2) if total_customers > 0 else 0
    
    return {
        'total_sales': round(total_sales, 2),
        'total_profit': round(total_profit, 2),
        'profit_margin': profit_margin,
        'total_orders': total_orders,
        'total_customers': total_customers,
        'total_items_sold': total_items,
        'avg_order_value': aov,
        'avg_profit_per_order': round(total_profit / total_orders, 2) if total_orders > 0 else 0,
        'avg_items_per_order': round(total_items / total_orders, 2) if total_orders > 0 else 0,
        'avg_discount': avg_discount,
        'avg_shipping_cost': avg_shipping,
        'return_rate': return_rate,
        'repeat_purchase_rate': repeat_rate,
        'avg_orders_per_customer': round(float(df.groupby('Customer ID')['Order ID'].nunique().mean()), 2),
        'avg_revenue_per_customer': round(float(df.groupby('Customer ID')['Sales'].sum().mean()), 2),
    }


# =============================================================================
# FILTER OPTIONS
# =============================================================================
def get_filter_options() -> Dict[str, list]:
    """
    Get available filter values for dropdowns.
    
    Returns:
        Dictionary of filter names to lists of values
    """
    df = load_data()
    if df.empty:
        return {'years': [], 'categories': [], 'regions': [], 'segments': [], 'shipping_modes': []}
    
    return {
        'years': sorted(df['Order Date'].dt.year.dropna().unique().tolist()),
        'categories': sorted(df['Category'].unique().tolist()),
        'regions': sorted(df['Region'].unique().tolist()),
        'segments': sorted(df['Segment'].unique().tolist()),
        'shipping_modes': sorted(df['Shipping Mode'].unique().tolist()),
    }


# =============================================================================
# SERIALIZATION
# =============================================================================
def to_native(obj):
    """
    Convert numpy types to native Python types for JSON serialization.
    
    Args:
        obj: Any value that might be a numpy type
    
    Returns:
        Native Python type equivalent
    """
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, np.bool_):
        return bool(obj)
    if isinstance(obj, pd.Timestamp):
        return str(obj)
    if isinstance(obj, pd.Series):
        return obj.tolist()
    return obj


# =============================================================================
# COLOR PALETTE (shared constant)
# =============================================================================
COLOR_PALETTE = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'danger': '#C73E1D',
    'success': '#44BBA4',
    'dark': '#3B1F2B',
    'colors': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#44BBA4',
               '#1B998B', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
}
