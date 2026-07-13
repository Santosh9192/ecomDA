"""
=============================================================================
E-Commerce Sales Analytics - Business Analysis & Insights
=============================================================================
Description: Comprehensive business analysis with visualizations and insights
Author: Business Analytics Team
Version: 1.0
Python: 3.8+
=============================================================================
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import os
import logging
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================
CLEANED_DATA_PATH = os.path.join('data', 'cleaned')
RAW_DATA_PATH = os.path.join('data', 'raw')
OUTPUT_CHARTS_PATH = os.path.join('reports', 'screenshots')
INSIGHTS_PATH = os.path.join('reports', 'business_insights.csv')

# Visualization settings
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette('husl')
PLOT_DPI = 150
COLORS = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#44BBA4']

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


# =============================================================================
# DATA LOADER
# =============================================================================
def load_data() -> pd.DataFrame:
    """
    Load cleaned order data for analysis.
    Falls back to raw data if cleaned is unavailable.
    
    Returns:
        Orders DataFrame
    """
    cleaned_path = os.path.join(CLEANED_DATA_PATH, 'orders_cleaned.csv')
    raw_path = os.path.join(RAW_DATA_PATH, 'ecommerce_orders.csv')
    
    if os.path.exists(cleaned_path):
        df = pd.read_csv(cleaned_path)
        logger.info(f"Loaded cleaned data: {len(df):,} records")
    elif os.path.exists(raw_path):
        df = pd.read_csv(raw_path)
        logger.info(f"Loaded raw data: {len(df):,} records")
    else:
        raise FileNotFoundError("No order data found")
    
    # Ensure date columns are datetime
    for col in ['Order Date', 'Ship Date']:
        if col in df.columns and not pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df


# =============================================================================
# BUSINESS METRICS CALCULATIONS
# =============================================================================
def calculate_kpis(df: pd.DataFrame) -> Dict:
    """
    Calculate key business KPIs from the dataset.
    
    Returns:
        Dictionary of calculated KPIs
    """
    kpis = {}
    
    # Total metrics
    kpis['total_sales'] = round(df['Sales'].sum(), 2)
    kpis['total_profit'] = round(df['Profit'].sum(), 2)
    kpis['total_orders'] = df['Order ID'].nunique()
    kpis['total_customers'] = df['Customer ID'].nunique()
    kpis['total_items_sold'] = int(df['Quantity'].sum())
    
    # Average metrics
    kpis['avg_order_value'] = round(
        df['Sales'].sum() / df['Order ID'].nunique(), 2
    )
    kpis['avg_profit_per_order'] = round(
        df['Profit'].sum() / df['Order ID'].nunique(), 2
    )
    kpis['avg_quantity_per_order'] = round(
        df['Quantity'].sum() / df['Order ID'].nunique(), 2
    )
    
    # Profitability
    kpis['profit_margin_pct'] = round(
        (df['Profit'].sum() / df['Sales'].sum()) * 100, 2
    )
    kpis['avg_discount'] = round(df['Discount'].mean(), 4)
    
    # Customer metrics
    avg_orders_per_customer = df.groupby('Customer ID')['Order ID'].nunique().mean()
    kpis['avg_orders_per_customer'] = round(avg_orders_per_customer, 2)
    
    # Revenue per customer
    revenue_per_customer = df.groupby('Customer ID')['Sales'].sum().mean()
    kpis['avg_revenue_per_customer'] = round(revenue_per_customer, 2)
    
    # Return rate
    if 'Return Status' in df.columns:
        return_rate = (df['Return Status'] == 'Returned').mean() * 100
        kpis['return_rate_pct'] = round(return_rate, 2)
    
    # Shipping metrics
    if 'Shipping Cost' in df.columns:
        kpis['total_shipping_cost'] = round(df['Shipping Cost'].sum(), 2)
        kpis['avg_shipping_cost'] = round(df['Shipping Cost'].mean(), 2)
    
    # Revenue by category
    category_revenue = df.groupby('Category')['Sales'].sum()
    kpis['top_category'] = category_revenue.idxmax()
    kpis['top_category_revenue'] = round(category_revenue.max(), 2)
    
    # Top product
    product_revenue = df.groupby('Product Name')['Sales'].sum()
    kpis['top_product'] = product_revenue.idxmax()
    kpis['top_product_revenue'] = round(product_revenue.max(), 2)
    
    # Regional metrics
    region_revenue = df.groupby('Region')['Sales'].sum()
    kpis['top_region'] = region_revenue.idxmax()
    kpis['top_region_revenue'] = round(region_revenue.max(), 2)
    
    # Top customer
    customer_revenue = df.groupby('Customer Name')['Sales'].sum()
    kpis['top_customer'] = customer_revenue.idxmax()
    kpis['top_customer_revenue'] = round(customer_revenue.max(), 2)
    
    # Repeat purchase rate
    customer_order_counts = df.groupby('Customer ID')['Order ID'].nunique()
    repeat_customers = (customer_order_counts > 1).sum()
    kpis['repeat_purchase_rate_pct'] = round(
        (repeat_customers / len(customer_order_counts)) * 100, 2
    )
    
    return kpis


# =============================================================================
# VISUALIZATION FUNCTIONS
# =============================================================================
def setup_plot(title: str, xlabel: str = '', ylabel: str = '', 
               figsize: Tuple = (12, 6)) -> Tuple:
    """
    Set up a matplotlib plot with consistent styling.
    
    Args:
        title: Plot title
        xlabel: X-axis label
        ylabel: Y-axis label
        figsize: Figure dimensions
        
    Returns:
        Figure and axes objects
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel(xlabel, fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.tick_params(axis='both', labelsize=10)
    return fig, ax


def save_plot(fig, filename: str, subdir: str = '') -> str:
    """
    Save a plot to the charts directory.
    
    Args:
        fig: Matplotlib figure
        filename: Output filename
        subdir: Optional subdirectory
        
    Returns:
        Path to saved file
    """
    output_dir = os.path.join(OUTPUT_CHARTS_PATH, subdir)
    os.makedirs(output_dir, exist_ok=True)
    
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=PLOT_DPI, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.close(fig)
    logger.info(f"Chart saved: {filepath}")
    return filepath


def format_currency(value: float) -> str:
    """Format number as currency string."""
    return f'${value:,.2f}'


def format_percentage(value: float) -> str:
    """Format number as percentage string."""
    return f'{value:.1f}%'


# =============================================================================
# CHART GENERATION
# =============================================================================
def plot_monthly_sales_trend(df: pd.DataFrame) -> str:
    """Generate monthly sales and profit trend chart."""
    logger.info("Generating monthly sales trend chart...")
    
    monthly = df.groupby(df['Order Date'].dt.to_period('M')).agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    monthly['Order Date'] = monthly['Order Date'].astype(str)
    
    fig, ax1 = setup_plot(
        'Monthly Sales & Profit Trend',
        'Month', 'Sales ($)',
        figsize=(14, 6)
    )
    
    ax1.bar(monthly['Order Date'], monthly['Sales'], color=COLORS[0], 
            alpha=0.7, label='Sales', width=0.7)
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, p: f'${x:,.0f}'))
    
    ax2 = ax1.twinx()
    ax2.plot(monthly['Order Date'], monthly['Profit'], color=COLORS[2], 
             marker='o', linewidth=2, label='Profit')
    ax2.set_ylabel('Profit ($)', fontsize=12)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, p: f'${x:,.0f}'))
    
    # Rotate labels
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, ha='right')
    
    # Combined legend
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
    
    fig.tight_layout()
    return save_plot(fig, 'monthly_sales_trend.png')


def plot_sales_by_category(df: pd.DataFrame) -> str:
    """Generate sales by category pie/donut chart."""
    logger.info("Generating category sales chart...")
    
    cat_sales = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    colors = [COLORS[0], COLORS[1], COLORS[2]]
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Pie chart
    wedges, texts, autotexts = ax1.pie(
        cat_sales.values, labels=None, autopct='%1.1f%%',
        colors=colors, startangle=90, explode=(0.05, 0.05, 0.05),
        shadow=True, textprops={'fontsize': 12}
    )
    ax1.set_title('Sales Distribution by Category', fontsize=14, fontweight='bold')
    
    # Donut chart
    wedges2, texts2, autotexts2 = ax2.pie(
        cat_sales.values, labels=None, autopct='%1.1f%%',
        colors=colors, startangle=90, pctdistance=0.85,
        wedgeprops=dict(width=0.4), shadow=True
    )
    ax2.set_title('Sales Share (Donut View)', fontsize=14, fontweight='bold')
    
    # Common legend
    labels = [f'{cat}\n({format_currency(val)})' 
              for cat, val in cat_sales.items()]
    fig.legend(wedges, labels, title='Category', loc='center right',
               fontsize=10)
    
    fig.tight_layout()
    return save_plot(fig, 'sales_by_category.png')


def plot_top_products(df: pd.DataFrame, n: int = 10) -> str:
    """Generate top N products bar chart."""
    logger.info(f"Generating top {n} products chart...")
    
    top_products = df.groupby('Product Name')['Sales'].sum().nlargest(n)
    
    fig, ax = setup_plot(
        f'Top {n} Products by Revenue',
        'Product Name', 'Total Sales ($)',
        figsize=(12, 7)
    )
    
    bars = ax.barh(range(len(top_products)), top_products.values, 
                   color=COLORS[0], edgecolor='white')
    
    # Customize y-axis labels
    ax.set_yticks(range(len(top_products)))
    ax.set_yticklabels(top_products.index, fontsize=10)
    ax.invert_yaxis()
    
    # Add value labels
    for i, (bar, value) in enumerate(zip(bars, top_products.values)):
        ax.text(value, bar.get_y() + bar.get_height()/2,
                f'  ${value:,.0f}', va='center', fontsize=9)
    
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x, p: f'${x:,.0f}'))
    
    fig.tight_layout()
    return save_plot(fig, f'top_{n}_products.png')


def plot_regional_performance(df: pd.DataFrame) -> str:
    """Generate regional sales and profit chart."""
    logger.info("Generating regional performance chart...")
    
    regional = df.groupby('Region').agg({
        'Sales': 'sum',
        'Profit': 'sum'
    }).reset_index()
    
    fig, ax = setup_plot(
        'Regional Sales & Profit Performance',
        'Region', 'Amount ($)',
        figsize=(10, 6)
    )
    
    x = np.arange(len(regional))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, regional['Sales'], width, 
                   label='Sales', color=COLORS[0], alpha=0.8)
    bars2 = ax.bar(x + width/2, regional['Profit'], width, 
                   label='Profit', color=COLORS[1], alpha=0.8)
    
    ax.set_xticks(x)
    ax.set_xticklabels(regional['Region'], fontsize=11)
    ax.legend(fontsize=11)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda x_val, p: f'${x_val:,.0f}'))
    
    # Add value labels
    for bar in bars1:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'${height:,.0f}', ha='center', va='bottom', fontsize=8)
    
    fig.tight_layout()
    return save_plot(fig, 'regional_performance.png')


def plot_customer_segment_analysis(df: pd.DataFrame) -> str:
    """Generate customer segment analysis chart."""
    logger.info("Generating customer segment analysis chart...")
    
    segment_analysis = df.groupby('Segment').agg({
        'Sales': ['sum', 'mean'],
        'Profit': 'sum',
        'Order ID': 'nunique'
    }).round(2)
    
    segment_analysis.columns = ['Total Sales', 'Avg Order Value', 
                                'Total Profit', 'Order Count']
    segment_analysis = segment_analysis.reset_index()
    
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    # Sales by segment
    axes[0, 0].bar(segment_analysis['Segment'], segment_analysis['Total Sales'],
                   color=COLORS[0], alpha=0.8)
    axes[0, 0].set_title('Total Sales by Segment', fontweight='bold')
    axes[0, 0].set_ylabel('Sales ($)')
    axes[0, 0].yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Profit by segment
    axes[0, 1].bar(segment_analysis['Segment'], segment_analysis['Total Profit'],
                   color=COLORS[1], alpha=0.8)
    axes[0, 1].set_title('Total Profit by Segment', fontweight='bold')
    axes[0, 1].set_ylabel('Profit ($)')
    axes[0, 1].yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, p: f'${x:,.0f}'))
    
    # Avg order value
    axes[1, 0].bar(segment_analysis['Segment'], segment_analysis['Avg Order Value'],
                   color=COLORS[2], alpha=0.8)
    axes[1, 0].set_title('Average Order Value by Segment', fontweight='bold')
    axes[1, 0].set_ylabel('Avg Order Value ($)')
    
    # Order count
    axes[1, 1].bar(segment_analysis['Segment'], segment_analysis['Order Count'],
                   color=COLORS[3], alpha=0.8)
    axes[1, 1].set_title('Order Count by Segment', fontweight='bold')
    axes[1, 1].set_ylabel('Number of Orders')
    
    fig.tight_layout()
    return save_plot(fig, 'customer_segment_analysis.png')


def plot_discount_impact(df: pd.DataFrame) -> str:
    """Generate discount impact analysis chart."""
    logger.info("Generating discount impact chart...")
    
    df['Discount Range'] = pd.cut(
        df['Discount'], 
        bins=[-0.01, 0, 0.05, 0.10, 0.15, 0.20, 1.0],
        labels=['0%', '1-5%', '6-10%', '11-15%', '16-20%', '21%+']
    )
    
    discount_impact = df.groupby('Discount Range', observed=True).agg({
        'Sales': 'sum',
        'Profit': 'sum',
        'Quantity': 'sum',
        'Order ID': 'nunique'
    })
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Sales and Profit by discount range
    x = np.arange(len(discount_impact))
    width = 0.35
    
    ax1.bar(x - width/2, discount_impact['Sales'], width, 
            label='Sales', color=COLORS[0], alpha=0.8)
    ax1.bar(x + width/2, discount_impact['Profit'], width, 
            label='Profit', color=COLORS[1], alpha=0.8)
    ax1.set_title('Sales & Profit by Discount Range', fontweight='bold')
    ax1.set_xlabel('Discount Range')
    ax1.set_ylabel('Amount ($)')
    ax1.set_xticks(x)
    ax1.set_xticklabels(discount_impact.index, rotation=45)
    ax1.legend()
    ax1.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x_val, p: f'${x_val:,.0f}'))
    
    # Order count by discount range
    ax2.bar(x, discount_impact['Order ID'], color=COLORS[2], alpha=0.8)
    ax2.set_title('Order Count by Discount Range', fontweight='bold')
    ax2.set_xlabel('Discount Range')
    ax2.set_ylabel('Order Count')
    ax2.set_xticks(x)
    ax2.set_xticklabels(discount_impact.index, rotation=45)
    
    fig.tight_layout()
    return save_plot(fig, 'discount_impact.png')


def plot_profit_margin_analysis(df: pd.DataFrame) -> str:
    """Generate profit margin analysis chart."""
    logger.info("Generating profit margin analysis chart...")
    
    df['Profit Margin'] = np.where(
        df['Sales'] > 0,
        (df['Profit'] / df['Sales']) * 100,
        0
    )
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Profit margin distribution
    ax1.hist(df['Profit Margin'].clip(-50, 50), bins=30, 
             color=COLORS[0], edgecolor='white', alpha=0.7)
    ax1.axvline(df['Profit Margin'].median(), color='red', 
                linestyle='--', linewidth=2, label=f'Median: {df["Profit Margin"].median():.1f}%')
    ax1.set_title('Profit Margin Distribution', fontweight='bold')
    ax1.set_xlabel('Profit Margin (%)')
    ax1.set_ylabel('Frequency')
    ax1.legend()
    
    # Profit margin by category (box plot)
    category_margin_data = [df[df['Category'] == cat]['Profit Margin'].dropna().values 
                           for cat in df['Category'].unique()]
    
    bp = ax2.boxplot(category_margin_data, 
                     patch_artist=True)
    for patch, color in zip(bp['boxes'], COLORS[:3]):
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    ax2.set_title('Profit Margin Distribution by Category', fontweight='bold')
    ax2.set_ylabel('Profit Margin (%)')
    ax2.set_xlabel('Category')
    ax2.set_xticklabels(df['Category'].unique())
    
    fig.tight_layout()
    return save_plot(fig, 'profit_margin_analysis.png')


def plot_shipping_analysis(df: pd.DataFrame) -> str:
    """Generate shipping mode analysis chart."""
    logger.info("Generating shipping analysis chart...")
    
    shipping = df.groupby('Shipping Mode').agg(
        Total_Sales=('Sales', 'sum'),
        Total_Profit=('Profit', 'sum'),
        Order_Count=('Order ID', 'nunique'),
        Avg_Shipping_Cost=('Shipping Cost', 'mean')
    ).round(2)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Sales by shipping mode
    ax1.bar(shipping.index, shipping['Total_Sales'], color=COLORS[0], alpha=0.8)
    ax1.set_title('Sales by Shipping Mode', fontweight='bold')
    ax1.set_xlabel('Shipping Mode')
    ax1.set_ylabel('Total Sales ($)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x_val, p: f'${x_val:,.0f}'))
    
    # Average shipping cost by mode
    ax2.bar(shipping.index, shipping['Avg_Shipping_Cost'], color=COLORS[1], alpha=0.8)
    ax2.set_title('Average Shipping Cost by Mode', fontweight='bold')
    ax2.set_xlabel('Shipping Mode')
    ax2.set_ylabel('Avg Shipping Cost ($)')
    ax2.tick_params(axis='x', rotation=45)
    ax2.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, p: f'${x:,.2f}'))
    
    fig.tight_layout()
    return save_plot(fig, 'shipping_analysis.png')


def plot_monthly_growth_rate(df: pd.DataFrame) -> str:
    """Generate monthly growth rate chart."""
    logger.info("Generating monthly growth rate chart...")
    
    monthly_sales = df.set_index('Order Date').resample('ME')['Sales'].sum()
    growth_rate = monthly_sales.pct_change() * 100
    
    fig, ax = setup_plot(
        'Month-over-Month Sales Growth Rate',
        'Date', 'Growth Rate (%)',
        figsize=(14, 6)
    )
    
    colors = ['green' if g >= 0 else 'red' for g in growth_rate]
    ax.bar(growth_rate.index, growth_rate.values, color=colors, alpha=0.7, width=20)
    ax.axhline(y=0, color='black', linewidth=1)
    ax.yaxis.set_major_formatter(
        mticker.FuncFormatter(lambda x, p: f'{x:.1f}%'))
    
    fig.tight_layout()
    return save_plot(fig, 'monthly_growth_rate.png')


def generate_all_charts(df: pd.DataFrame) -> Dict[str, str]:
    """
    Generate all analysis charts.
    
    Returns:
        Dictionary mapping chart names to file paths
    """
    logger.info("\n" + "=" * 50)
    logger.info("GENERATING ALL CHARTS")
    logger.info("=" * 50)
    
    charts = {}
    
    chart_functions = [
        ('Monthly Sales Trend', plot_monthly_sales_trend),
        ('Category Sales', plot_sales_by_category),
        ('Top Products', plot_top_products),
        ('Regional Performance', plot_regional_performance),
        ('Customer Segment', plot_customer_segment_analysis),
        ('Discount Impact', plot_discount_impact),
        ('Profit Margin', plot_profit_margin_analysis),
        ('Shipping Analysis', plot_shipping_analysis),
        ('Monthly Growth', plot_monthly_growth_rate)
    ]
    
    for name, func in chart_functions:
        try:
            path = func(df)
            charts[name] = path
        except Exception as e:
            logger.error(f"Failed to generate chart '{name}': {e}")
    
    logger.info(f"\nGenerated {len(charts)}/{len(chart_functions)} charts")
    return charts


# =============================================================================
# BUSINESS INSIGHTS EXTRACTION
# =============================================================================
def extract_business_insights(df: pd.DataFrame, kpis: Dict) -> pd.DataFrame:
    """
    Extract actionable business insights from the data.
    
    Returns:
        DataFrame of insights with categories and recommendations
    """
    logger.info("\n" + "=" * 50)
    logger.info("EXTRACTING BUSINESS INSIGHTS")
    logger.info("=" * 50)
    
    insights = []
    
    # Sales insights
    insights.append({
        'Category': 'Sales',
        'Insight': f'Total revenue is {format_currency(kpis["total_sales"])} from {kpis["total_orders"]} orders',
        'Impact': 'High',
        'Recommendation': 'Focus on maintaining revenue growth through customer retention'
    })
    
    # Profitability insights
    insights.append({
        'Category': 'Profitability',
        'Insight': f'Overall profit margin is {format_percentage(kpis["profit_margin_pct"])}',
        'Impact': 'High',
        'Recommendation': 'Review pricing strategy and cost optimization opportunities'
    })
    
    # Category performance
    top_cat = df.groupby('Category')['Sales'].sum().idxmax()
    cat_sales = df.groupby('Category')['Sales'].sum()
    cat_share = (cat_sales[top_cat] / cat_sales.sum()) * 100
    insights.append({
        'Category': 'Product',
        'Insight': f'Top category is {top_cat} with {format_percentage(cat_share)} of total sales',
        'Impact': 'Medium',
        'Recommendation': f'Expand {top_cat} product line and cross-sell to other categories'
    })
    
    # Customer insights
    insights.append({
        'Category': 'Customer',
        'Insight': f'Average order value is {format_currency(kpis["avg_order_value"])} with {format_percentage(kpis["repeat_purchase_rate_pct"])} repeat purchase rate',
        'Impact': 'High',
        'Recommendation': 'Implement loyalty programs to increase repeat purchases and AOV'
    })
    
    # Regional insights
    region_profit = df.groupby('Region')['Profit'].sum()
    best_region = region_profit.idxmax()
    worst_region = region_profit.idxmin()
    insights.append({
        'Category': 'Regional',
        'Insight': f'Best performing region: {best_region}, Worst: {worst_region}',
        'Impact': 'Medium',
        'Recommendation': f'Analyze {worst_region} challenges and replicate {best_region} strategies'
    })
    
    # Discount insights
    avg_disc = kpis['avg_discount'] * 100
    discount_orders = (df['Discount'] > 0).mean() * 100
    insights.append({
        'Category': 'Pricing',
        'Insight': f'Average discount is {avg_disc:.1f}% applied to {discount_orders:.1f}% of orders',
        'Impact': 'Medium',
        'Recommendation': 'Optimize discount strategy to maximize profit without losing sales volume'
    })
    
    # Segment insights
    segment_profit = df.groupby('Segment')['Profit'].sum()
    best_segment = segment_profit.idxmax()
    insights.append({
        'Category': 'Segment',
        'Insight': f'Most profitable segment: {best_segment}',
        'Impact': 'Medium',
        'Recommendation': f'Develop targeted marketing campaigns for {best_segment} segment'
    })
    
    # Shipping insights
    if 'Shipping Cost' in df.columns:
        shipping_cost_pct = (df['Shipping Cost'].sum() / df['Sales'].sum()) * 100
        insights.append({
            'Category': 'Operations',
            'Insight': f'Shipping costs represent {shipping_cost_pct:.1f}% of total revenue',
            'Impact': 'Low',
            'Recommendation': 'Negotiate better shipping rates or optimize shipping modes'
        })
    
    # Return insights
    if 'Return Status' in df.columns:
        return_rate = (df['Return Status'] == 'Returned').mean() * 100
        return_revenue = df[df['Return Status'] == 'Returned']['Sales'].sum()
        insights.append({
            'Category': 'Quality',
            'Insight': f'Return rate is {return_rate:.1f}% affecting {format_currency(return_revenue)} in revenue',
            'Impact': 'Medium',
            'Recommendation': 'Investigate return reasons and improve product quality/descriptions'
        })
    
    insights_df = pd.DataFrame(insights)
    
    # Save insights to CSV
    os.makedirs(os.path.dirname(INSIGHTS_PATH), exist_ok=True)
    insights_df.to_csv(INSIGHTS_PATH, index=False)
    logger.info(f"Insights saved to: {INSIGHTS_PATH}")
    
    return insights_df


# =============================================================================
# MAIN EXECUTION
# =============================================================================
def main():
    """Main analysis execution."""
    logger.info("=" * 60)
    logger.info("BUSINESS ANALYSIS PIPELINE STARTED")
    logger.info("=" * 60)
    
    # Load data
    logger.info("\n[1/4] Loading data...")
    df = load_data()
    
    # Calculate KPIs
    logger.info("\n[2/4] Calculating KPIs...")
    kpis = calculate_kpis(df)
    
    print("\n" + "-" * 50)
    print("KEY BUSINESS KPIs")
    print("-" * 50)
    kpi_display = [
        ('Total Sales', format_currency(kpis['total_sales'])),
        ('Total Profit', format_currency(kpis['total_profit'])),
        ('Profit Margin', format_percentage(kpis['profit_margin_pct'])),
        ('Total Orders', str(kpis['total_orders'])),
        ('Total Customers', str(kpis['total_customers'])),
        ('Avg Order Value', format_currency(kpis['avg_order_value'])),
        ('Avg Orders/Customer', str(kpis['avg_orders_per_customer'])),
        ('Repeat Purchase Rate', format_percentage(kpis['repeat_purchase_rate_pct'])),
        ('Top Category', f"{kpis['top_category']} ({format_currency(kpis['top_category_revenue'])})"),
        ('Top Region', f"{kpis['top_region']} ({format_currency(kpis['top_region_revenue'])})"),
        ('Top Product', f"{kpis['top_product']} ({format_currency(kpis['top_product_revenue'])})"),
        ('Return Rate', format_percentage(kpis.get('return_rate_pct', 0))),
    ]
    
    for name, value in kpi_display:
        print(f"  {name:.<25} {value}")
    
    # Generate charts
    logger.info("\n[3/4] Generating charts...")
    charts = generate_all_charts(df)
    
    # Extract insights
    logger.info("\n[4/4] Extracting insights...")
    insights_df = extract_business_insights(df, kpis)
    
    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print("=" * 60)
    print(f"\nCharts generated: {len(charts)}")
    print(f"Insights extracted: {len(insights_df)}")
    print(f"\nCharts saved to: {OUTPUT_CHARTS_PATH}")
    print(f"Insights saved to: {INSIGHTS_PATH}")
    
    return df, kpis, charts, insights_df


if __name__ == '__main__':
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(project_root)
    main()
