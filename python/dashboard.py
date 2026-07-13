"""
=============================================================================
E-Commerce Sales Analytics - Enhanced Interactive Dashboard (Plotly/Dash)
=============================================================================
Description: A comprehensive interactive dashboard with multiple tabs,
             advanced filters, and rich visualizations. Runs in the browser.
Usage: python python/dashboard.py
       Then open http://localhost:8050 in your browser
=============================================================================
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime
from typing import Dict, List, Tuple

# Add project root and import shared utilities
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
try:
    from python.analytics_utils import load_data, calculate_kpis, COLOR_PALETTE, get_filter_options
except ImportError:
    # Fallback if running from different context
    from analytics_utils import load_data, calculate_kpis, COLOR_PALETTE, get_filter_options

SCREENSHOTS_PATH = os.path.join(PROJECT_ROOT, 'reports', 'screenshots')

CSS = {
    'bg': '#0E1117',
    'card': '#161B22',
    'card_border': '#30363D',
    'accent': '#2E86AB',
    'accent2': '#44BBA4',
    'text': '#E6EDF3',
    'muted': '#8B949E',
    'header_bg': '#0D1117',
}

# Try to import dash
try:
    import dash
    from dash import dcc, html, callback, Input, Output, State, dash_table
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.figure_factory as ff
    import plotly.io as pio
    DASH_AVAILABLE = True
except ImportError:
    DASH_AVAILABLE = False
    print("Dash not installed. Install with: pip install dash plotly")


# =============================================================================
# CHART GENERATION FUNCTIONS
# =============================================================================

def create_monthly_trend(df):
    """Monthly Sales & Profit trend with dual axes."""
    monthly = df.groupby(df['Order Date'].dt.to_period('M')).agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum')
    ).reset_index()
    monthly['Order Date'] = monthly['Order Date'].astype(str)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly['Order Date'], y=monthly['Sales'],
                         name='Sales', marker_color=COLOR_PALETTE['primary'],
                         hovertemplate='%{y:$,.0f}<extra>Sales</extra>'))
    fig.add_trace(go.Scatter(x=monthly['Order Date'], y=monthly['Profit'],
                              name='Profit', yaxis='y2',
                              line=dict(color=COLOR_PALETTE['accent'], width=3),
                              mode='lines+markers',
                              hovertemplate='%{y:$,.0f}<extra>Profit</extra>'))
    fig.update_layout(
        title=dict(text='Monthly Sales & Profit Trend', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        hovermode='x unified',
        xaxis_tickangle=-45,
        yaxis=dict(title='Sales ($)', side='left', gridcolor='#2D333B'),
        yaxis2=dict(title='Profit ($)', overlaying='y', side='right', gridcolor='#2D333B'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(l=60, r=60, t=50, b=80),
    )
    return fig


def create_sales_by_category(df):
    """Category sales distribution pie chart."""
    cat_sales = df.groupby('Category')['Sales'].sum().reset_index()
    total = cat_sales['Sales'].sum()
    cat_sales['Percentage'] = (cat_sales['Sales'] / total * 100).round(1)
    cat_sales['Label'] = cat_sales.apply(
        lambda r: f"{r['Category']}<br>${r['Sales']:,.0f}<br>({r['Percentage']}%)", axis=1
    )
    
    fig = px.pie(
        cat_sales, values='Sales', names='Category',
        title='Sales Distribution by Category',
        color_discrete_sequence=[COLOR_PALETTE['primary'], COLOR_PALETTE['secondary'], COLOR_PALETTE['accent']],
        hole=0.45,
        custom_data=['Percentage']
    )
    fig.update_traces(
        textinfo='label+percent',
        textposition='outside',
        hovertemplate='<b>%{label}</b><br>Sales: $%{value:,.0f}<br>Share: %{customdata[0]:.1f}%<extra></extra>'
    )
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        title=dict(font=dict(size=18, color=CSS['text'])),
        showlegend=True,
        legend=dict(orientation='h', yanchor='bottom', y=-0.2),
        margin=dict(t=50, b=80),
    )
    return fig


def create_regional_bar(df):
    """Regional sales and profit comparison."""
    regional = df.groupby('Region').agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum')
    ).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Sales', x=regional['Region'], y=regional['Sales'],
                         marker_color=COLOR_PALETTE['primary'],
                         hovertemplate='Sales: $%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Bar(name='Profit', x=regional['Region'], y=regional['Profit'],
                         marker_color=COLOR_PALETTE['success'],
                         hovertemplate='Profit: $%{y:,.0f}<extra></extra>'))
    fig.update_layout(
        title=dict(text='Regional Performance', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        barmode='group',
        yaxis=dict(title='Amount ($)', gridcolor='#2D333B'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=40),
    )
    return fig


def create_top_products(df, n=10):
    """Top N products by sales."""
    top = df.groupby('Product Name')['Sales'].sum().nlargest(n).reset_index()
    fig = px.bar(
        top, x='Sales', y='Product Name', orientation='h',
        title=f'Top {n} Products by Revenue',
        color='Sales', color_continuous_scale='blues',
        text_auto='$.2s'
    )
    fig.update_traces(hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.0f}<extra></extra>')
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        yaxis=dict(categoryorder='total ascending', gridcolor='#2D333B'),
        xaxis=dict(gridcolor='#2D333B'),
        title=dict(font=dict(size=18, color=CSS['text'])),
        coloraxis_showscale=False,
        margin=dict(t=50, b=40, l=250),
    )
    return fig


def create_segment_analysis(df):
    """Customer segment analysis with multiple metrics."""
    seg = df.groupby('Segment').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Customers=('Customer ID', 'nunique')
    ).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Sales ($K)', x=seg['Segment'], y=seg['Sales']/1000,
                         marker_color=COLOR_PALETTE['primary'],
                         hovertemplate='Sales: $%{y:,.1f}K<extra></extra>'))
    fig.add_trace(go.Bar(name='Profit ($K)', x=seg['Segment'], y=seg['Profit']/1000,
                         marker_color=COLOR_PALETTE['secondary'],
                         hovertemplate='Profit: $%{y:,.1f}K<extra></extra>'))
    fig.add_trace(go.Bar(name='Orders (/100)', x=seg['Segment'], y=seg['Orders']/100,
                         marker_color=COLOR_PALETTE['success'],
                         hovertemplate='Orders: %{y:.0f}00<extra></extra>'))
    fig.update_layout(
        title=dict(text='Customer Segment Analysis', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        barmode='group',
        yaxis=dict(title='Amount', gridcolor='#2D333B'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=40),
    )
    return fig


def create_discount_analysis(df):
    """Discount impact analysis."""
    df['Discount Range'] = pd.cut(
        df['Discount'],
        bins=[-0.01, 0, 0.05, 0.10, 0.20, 1.0],
        labels=['0%', '1-5%', '6-10%', '11-20%', '21%+']
    )
    disc = df.groupby('Discount Range', observed=True).agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Sales', x=disc['Discount Range'], y=disc['Sales'],
                         marker_color=COLOR_PALETTE['primary'],
                         hovertemplate='Sales: $%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Bar(name='Profit', x=disc['Discount Range'], y=disc['Profit'],
                         marker_color=COLOR_PALETTE['danger'],
                         hovertemplate='Profit: $%{y:,.0f}<extra></extra>'))
    fig.update_layout(
        title=dict(text='Discount Impact on Sales & Profit', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        barmode='group',
        xaxis=dict(title='Discount Range', gridcolor='#2D333B'),
        yaxis=dict(title='Amount ($)', gridcolor='#2D333B'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=40),
    )
    return fig


def create_monthly_growth(df):
    """Month-over-month growth rate chart."""
    monthly_sales = df.set_index('Order Date').resample('ME')['Sales'].sum()
    growth_rate = monthly_sales.pct_change() * 100
    
    fig = go.Figure()
    colors = [COLOR_PALETTE['success'] if g >= 0 else COLOR_PALETTE['danger'] for g in growth_rate]
    fig.add_trace(go.Bar(x=growth_rate.index, y=growth_rate.values, marker_color=colors,
                         name='Growth Rate',
                         hovertemplate='%{y:.1f}%<extra>MoM Growth</extra>'))
    fig.add_trace(go.Scatter(x=growth_rate.index, y=[0]*len(growth_rate),
                             mode='lines', line=dict(color='white', width=1, dash='dash'),
                             showlegend=False, hoverinfo='skip'))
    fig.update_layout(
        title=dict(text='Month-over-Month Sales Growth', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        yaxis=dict(title='Growth Rate (%)', gridcolor='#2D333B'),
        xaxis=dict(gridcolor='#2D333B'),
        hovermode='x unified',
        margin=dict(t=50, b=40),
    )
    return fig


def create_sales_map(df):
    """Sales by state choropleth map."""
    state_sales = df.groupby('State')['Sales'].sum().reset_index()
    fig = px.choropleth(
        state_sales, locations='State', locationmode='USA-states',
        color='Sales', scope='usa',
        title='Sales by State',
        color_continuous_scale='blues',
        range_color=(0, state_sales['Sales'].max())
    )
    fig.update_traces(hovertemplate='<b>%{location}</b><br>Sales: $%{z:,.0f}<extra></extra>')
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        geo=dict(bgcolor='rgba(0,0,0,0)', lakecolor='#161B22', landcolor='#21262D',
                 subunitcolor='#30363D', countrycolor='#30363D'),
        title=dict(font=dict(size=18, color=CSS['text'])),
        coloraxis=dict(colorbar=dict(title='Sales', tickprefix='$')),
        margin=dict(t=50, b=40, l=0, r=0),
    )
    return fig


def create_profit_waterfall(df):
    """Profit waterfall by category showing contributing factors."""
    cat_profit = df.groupby('Category')['Profit'].sum().reset_index()
    cat_profit = cat_profit.sort_values('Profit', ascending=False)
    
    total_profit = cat_profit['Profit'].sum()
    categories = cat_profit['Category'].tolist()
    profits = cat_profit['Profit'].tolist()
    
    # Build waterfall
    measures = ['relative'] * len(categories)
    
    fig = go.Figure(go.Waterfall(
        name="Profit", orientation="v",
        measure=measures,
        x=categories,
        y=profits,
        text=[f"${p:,.0f}" for p in profits],
        textposition="outside",
        connector={"line": {"color": "#636363", "dash": "solid", "width": 1}},
        decreasing={"marker": {"color": COLOR_PALETTE['danger']}},
        increasing={"marker": {"color": COLOR_PALETTE['success']}},
        totals={"marker": {"color": COLOR_PALETTE['primary']}},
    ))
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="white", opacity=0.3)
    fig.update_layout(
        title=dict(text='Profit Breakdown by Category', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        yaxis=dict(title='Profit ($)', gridcolor='#2D333B'),
        xaxis=dict(gridcolor='#2D333B'),
        margin=dict(t=50, b=40),
        showlegend=False,
    )
    return fig


def create_shipping_analysis(df):
    """Shipping mode analysis."""
    shipping = df.groupby('Shipping Mode').agg(
        Sales=('Sales', 'sum'),
        Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Avg_Shipping=('Shipping Cost', 'mean')
    ).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Total Sales', x=shipping['Shipping Mode'], y=shipping['Sales'],
                         marker_color=COLOR_PALETTE['primary'],
                         hovertemplate='Sales: $%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Bar(name='Total Profit', x=shipping['Shipping Mode'], y=shipping['Profit'],
                         marker_color=COLOR_PALETTE['success'],
                         hovertemplate='Profit: $%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Scatter(name='Avg Shipping Cost', x=shipping['Shipping Mode'], y=shipping['Avg_Shipping'],
                              yaxis='y2', mode='lines+markers',
                              line=dict(color=COLOR_PALETTE['accent'], width=3, dash='dot'),
                              marker=dict(size=10),
                              hovertemplate='Avg Cost: $%{y:.2f}<extra></extra>'))
    fig.update_layout(
        title=dict(text='Shipping Mode Performance', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        barmode='group',
        yaxis=dict(title='Amount ($)', side='left', gridcolor='#2D333B'),
        yaxis2=dict(title='Avg Shipping Cost ($)', overlaying='y', side='right', gridcolor='#2D333B'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=80),
    )
    return fig


def create_profit_margin_scatter(df):
    """Profit margin analysis with scatter plot."""
    df_sample = df.sample(min(1000, len(df)), random_state=42)
    df_sample['Profit_Margin'] = np.where(
        df_sample['Sales'] > 0,
        (df_sample['Profit'] / df_sample['Sales']) * 100,
        0
    )
    
    fig = px.scatter(
        df_sample, x='Discount', y='Profit_Margin',
        color='Category', size='Sales',
        hover_data={'Sales': ':$,.0f', 'Profit': ':$,.0f', 'Discount': ':.0%'},
        title='Discount vs Profit Margin',
        color_discrete_sequence=[COLOR_PALETTE['primary'], COLOR_PALETTE['secondary'], COLOR_PALETTE['accent']],
        size_max=20,
    )
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="white", opacity=0.3)
    fig.update_traces(hovertemplate='<b>%{data.name}</b><br>Discount: %{x:.0%}<br>Margin: %{y:.1f}%<br>Sales: $%{customdata[0]:,.0f}<extra></extra>')
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        xaxis=dict(title='Discount Rate', tickformat='.0%', gridcolor='#2D333B'),
        yaxis=dict(title='Profit Margin (%)', gridcolor='#2D333B'),
        title=dict(font=dict(size=18, color=CSS['text'])),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=40),
    )
    return fig


def create_seasonal_heatmap(df):
    """Seasonal heatmap of sales by month and year."""
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['MonthName'] = df['Order Date'].dt.strftime('%b')
    
    heatmap_data = df.pivot_table(
        values='Sales', index='MonthName', columns='Year',
        aggfunc='sum', fill_value=0
    )
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    heatmap_data = heatmap_data.reindex(month_order) if any(m in heatmap_data.index for m in month_order) else heatmap_data
    
    fig = px.imshow(
        heatmap_data.values,
        x=heatmap_data.columns.astype(str),
        y=heatmap_data.index,
        text_auto='.3s',
        aspect='auto',
        color_continuous_scale='blues',
        title='Monthly Sales Heatmap (by Year)',
        labels=dict(x='Year', y='Month', color='Sales')
    )
    fig.update_traces(hovertemplate='<b>%{y} %{x}</b><br>Sales: $%{z:,.0f}<extra></extra>')
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        xaxis=dict(gridcolor='#2D333B'),
        yaxis=dict(gridcolor='#2D333B'),
        title=dict(font=dict(size=18, color=CSS['text'])),
        coloraxis=dict(colorbar=dict(title='Sales', tickprefix='$')),
        margin=dict(t=50, b=40),
    )
    return fig


def create_payment_analysis(df):
    """Payment mode distribution."""
    payment = df.groupby('Payment Mode').agg(
        Sales=('Sales', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index().sort_values('Sales', ascending=False)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Sales ($K)', x=payment['Payment Mode'], y=payment['Sales']/1000,
                         marker_color=COLOR_PALETTE['colors'][:len(payment)],
                         hovertemplate='Sales: $%{y:,.1f}K<extra></extra>'))
    fig.add_trace(go.Scatter(name='Orders', x=payment['Payment Mode'], y=payment['Orders'],
                              yaxis='y2', mode='lines+markers',
                              line=dict(color=COLOR_PALETTE['accent'], width=3),
                              marker=dict(size=10),
                              hovertemplate='Orders: %{y:,}<extra></extra>'))
    fig.update_layout(
        title=dict(text='Payment Mode Analysis', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        yaxis=dict(title='Sales ($K)', side='left', gridcolor='#2D333B'),
        yaxis2=dict(title='Order Count', overlaying='y', side='right', gridcolor='#2D333B'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=80),
    )
    return fig


def create_top_customers(df, n=10):
    """Top customers by sales."""
    top = df.groupby(['Customer Name', 'Segment', 'City', 'State']).agg(
        Sales=('Sales', 'sum'),
        Orders=('Order ID', 'nunique'),
        AvgOrder=('Sales', 'mean')
    ).reset_index().sort_values('Sales', ascending=False).head(n)
    
    fig = px.bar(
        top, x='Sales', y='Customer Name', orientation='h',
        title=f'Top {n} Customers by Revenue',
        color='Sales', color_continuous_scale='blues',
        hover_data={'Segment': True, 'City': True, 'State': True, 'Orders': True, 'AvgOrder': ':$,.0f'},
        text_auto='$.2s'
    )
    fig.update_traces(hovertemplate=(
        '<b>%{y}</b><br>'
        'Sales: $%{x:,.0f}<br>'
        'Segment: %{customdata[0]}<br>'
        'Location: %{customdata[1]}, %{customdata[2]}<br>'
        'Orders: %{customdata[3]}<br>'
        'Avg Order: $%{customdata[4]:,.0f}<extra></extra>'
    ))
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        yaxis=dict(categoryorder='total ascending'),
        xaxis=dict(title='Total Sales ($)', gridcolor='#2D333B'),
        title=dict(font=dict(size=18, color=CSS['text'])),
        coloraxis_showscale=False,
        margin=dict(t=50, b=40, l=200),
    )
    return fig


def create_subcategory_sales(df):
    """Sales by sub-category."""
    subcat = df.groupby(['Category', 'Sub-Category'])['Sales'].sum().reset_index()
    subcat = subcat.sort_values('Sales', ascending=True)
    
    fig = px.bar(
        subcat, x='Sales', y='Sub-Category', color='Category', orientation='h',
        title='Sales by Sub-Category',
        color_discrete_sequence=[COLOR_PALETTE['primary'], COLOR_PALETTE['secondary'], COLOR_PALETTE['accent']],
        text_auto='$.2s'
    )
    fig.update_traces(hovertemplate='<b>%{y}</b><br>Sales: $%{x:,.0f}<br>Category: %{data.name}<extra></extra>')
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        yaxis=dict(categoryorder='total ascending'),
        xaxis=dict(title='Sales ($)', gridcolor='#2D333B'),
        title=dict(font=dict(size=18, color=CSS['text'])),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=40, l=200),
    )
    return fig


def create_delivery_analysis(df):
    """Delivery days analysis."""
    if 'Delivery Days' not in df.columns:
        fig = go.Figure()
        fig.update_layout(title='Delivery data not available', template='plotly_dark')
        return fig
    
    fig = go.Figure()
    fig.add_trace(go.Histogram(
        x=df['Delivery Days'], nbinsx=20,
        marker_color=COLOR_PALETTE['primary'],
        hovertemplate='Delivery Days: %{x}<br>Count: %{y}<extra></extra>'
    ))
    fig.add_vline(x=df['Delivery Days'].median(), line_dash='dash',
                   line_color=COLOR_PALETTE['accent'],
                   annotation_text=f"Median: {df['Delivery Days'].median():.0f} days",
                   annotation_position='top right')
    fig.update_layout(
        title=dict(text='Delivery Time Distribution', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        xaxis=dict(title='Delivery Days', gridcolor='#2D333B'),
        yaxis=dict(title='Number of Orders', gridcolor='#2D333B'),
        margin=dict(t=50, b=40),
    )
    return fig


def create_weekday_analysis(df):
    """Sales by day of week."""
    df['Weekday'] = df['Order Date'].dt.day_name()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    weekday_sales = df.groupby('Weekday').agg(
        Sales=('Sales', 'sum'), Orders=('Order ID', 'nunique')
    ).reset_index()
    weekday_sales['Weekday'] = pd.Categorical(weekday_sales['Weekday'], categories=weekday_order, ordered=True)
    weekday_sales = weekday_sales.sort_values('Weekday')
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Sales ($K)', x=weekday_sales['Weekday'], y=weekday_sales['Sales']/1000,
                         marker_color=COLOR_PALETTE['primary'],
                         hovertemplate='Sales: $%{y:,.1f}K<extra></extra>'))
    fig.add_trace(go.Scatter(name='Orders', x=weekday_sales['Weekday'], y=weekday_sales['Orders'],
                              yaxis='y2', mode='lines+markers',
                              line=dict(color=COLOR_PALETTE['accent'], width=3),
                              marker=dict(size=10),
                              hovertemplate='Orders: %{y:,}<extra></extra>'))
    fig.update_layout(
        title=dict(text='Sales by Day of Week', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        yaxis=dict(title='Sales ($K)', side='left', gridcolor='#2D333B'),
        yaxis2=dict(title='Order Count', overlaying='y', side='right', gridcolor='#2D333B'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=40),
    )
    return fig


def create_return_analysis(df):
    """Return rate by category."""
    return_stats = df.groupby('Category').agg(
        Total_Orders=('Order ID', 'nunique'),
        Returned=('Return Status', lambda x: (x == 'Returned').sum())
    ).reset_index()
    return_stats['Return_Rate'] = (return_stats['Returned'] / return_stats['Total_Orders'] * 100).round(1)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Return Rate (%)', x=return_stats['Category'], y=return_stats['Return_Rate'],
                         marker_color=[COLOR_PALETTE['danger'], COLOR_PALETTE['accent'], COLOR_PALETTE['primary']],
                         hovertemplate='Return Rate: %{y:.1f}%<extra></extra>'))
    fig.add_trace(go.Scatter(name='Returned Orders', x=return_stats['Category'], y=return_stats['Returned'],
                              yaxis='y2', mode='lines+markers',
                              line=dict(color=COLOR_PALETTE['success'], width=3),
                              marker=dict(size=10),
                              hovertemplate='Returned: %{y:,}<extra></extra>'))
    fig.update_layout(
        title=dict(text='Return Rate by Category', font=dict(size=18, color=CSS['text'])),
        template='plotly_dark',
        paper_bgcolor=CSS['card'],
        plot_bgcolor=CSS['card'],
        yaxis=dict(title='Return Rate (%)', side='left', gridcolor='#2D333B', ticksuffix='%'),
        yaxis2=dict(title='Returned Orders', overlaying='y', side='right', gridcolor='#2D333B'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=40),
    )
    return fig


# =============================================================================
# DASHBOARD APP
# =============================================================================

def create_app_layout(df):
    """Create the comprehensive Dash application layout."""
    kpis = calculate_kpis(df)
    
    # Get filter options
    years = sorted(df['Order Date'].dt.year.dropna().unique())
    categories = sorted(df['Category'].unique())
    regions = sorted(df['Region'].unique())
    segments = sorted(df['Segment'].unique())
    shipping_modes = sorted(df['Shipping Mode'].unique())
    
    # Build the app
    app = dash.Dash(__name__, title='E-Commerce Sales Analytics Dashboard',
                    assets_ignore='.*',
                    update_title='Loading...',
                    suppress_callback_exceptions=True)
    
    # =============================================================================
    # COMPONENT HELPERS
    # =============================================================================
    def kpi_card(title, value, color=COLOR_PALETTE['primary'], icon=''):
        """Styled KPI metric card."""
        return html.Div([
            html.Div([
                html.Span(icon, style={'fontSize': '20px', 'marginRight': '8px'}) if icon else None,
                html.Span(title, style={'fontSize': '12px', 'color': CSS['muted'], 'textTransform': 'uppercase',
                                         'letterSpacing': '0.5px'})
            ], style={'display': 'flex', 'alignItems': 'center', 'marginBottom': '8px'}),
            html.Div(value, style={
                'fontSize': '28px', 'fontWeight': '700', 'color': color,
                'fontFamily': 'SF Mono, Monaco, Consolas, monospace'
            })
        ], style={
            'backgroundColor': CSS['card'], 'padding': '16px 20px', 'borderRadius': '10px',
            'border': f'1px solid {CSS["card_border"]}',
            'borderLeft': f'4px solid {color}',
            'flex': '1', 'minWidth': '160px', 'margin': '6px',
            'transition': 'transform 0.2s, box-shadow 0.2s',
        })
    
    def section_header(title, subtitle=''):
        """Section header with optional subtitle."""
        return html.Div([
            html.H3(title, style={'color': CSS['text'], 'margin': '0', 'fontSize': '22px',
                                   'fontWeight': '600'}),
            html.P(subtitle, style={'color': CSS['muted'], 'margin': '4px 0 0 0', 'fontSize': '14px'})
        ], style={'marginBottom': '20px', 'borderBottom': f'1px solid {CSS["card_border"]}',
                   'paddingBottom': '12px'})
    
    def chart_container(fig, graph_id=None):
        """Wrap a chart in a styled container."""
        children = [dcc.Graph(id=graph_id, figure=fig)] if graph_id else [dcc.Graph(figure=fig)]
        return html.Div(
            children,
            style={
                'backgroundColor': CSS['card'], 'borderRadius': '10px',
                'border': f'1px solid {CSS["card_border"]}',
                'padding': '12px', 'margin': '8px', 'flex': '1', 'minWidth': '400px',
                'transition': 'transform 0.2s, box-shadow 0.2s',
            }
        )
    
    # =============================================================================
    # FILTER BAR
    # =============================================================================
    filter_bar = html.Div([
        html.Div([
            html.Label('Year:', style={'color': CSS['muted'], 'fontSize': '11px', 'fontWeight': '600',
                                        'textTransform': 'uppercase', 'letterSpacing': '0.5px',
                                        'marginBottom': '4px', 'display': 'block'}),
            dcc.Dropdown(
                id='year-filter',
                options=[{'label': 'All Years', 'value': 'All'}] +
                         [{'label': str(y), 'value': y} for y in years],
                value='All', clearable=False,
                style={'color': '#0D1117', 'fontSize': '14px', 'borderRadius': '6px'},
            )
        ], style={'width': '13%', 'minWidth': '120px'}),
        html.Div([
            html.Label('Category:', style={'color': CSS['muted'], 'fontSize': '11px', 'fontWeight': '600',
                                            'textTransform': 'uppercase', 'letterSpacing': '0.5px',
                                            'marginBottom': '4px', 'display': 'block'}),
            dcc.Dropdown(
                id='category-filter',
                options=[{'label': 'All Categories', 'value': 'All'}] +
                         [{'label': c, 'value': c} for c in categories],
                value='All', clearable=False,
                style={'color': '#0D1117', 'fontSize': '14px', 'borderRadius': '6px'},
            )
        ], style={'width': '15%', 'minWidth': '140px'}),
        html.Div([
            html.Label('Region:', style={'color': CSS['muted'], 'fontSize': '11px', 'fontWeight': '600',
                                          'textTransform': 'uppercase', 'letterSpacing': '0.5px',
                                          'marginBottom': '4px', 'display': 'block'}),
            dcc.Dropdown(
                id='region-filter',
                options=[{'label': 'All Regions', 'value': 'All'}] +
                         [{'label': r, 'value': r} for r in regions],
                value='All', clearable=False,
                style={'color': '#0D1117', 'fontSize': '14px', 'borderRadius': '6px'},
            )
        ], style={'width': '13%', 'minWidth': '120px'}),
        html.Div([
            html.Label('Segment:', style={'color': CSS['muted'], 'fontSize': '11px', 'fontWeight': '600',
                                           'textTransform': 'uppercase', 'letterSpacing': '0.5px',
                                           'marginBottom': '4px', 'display': 'block'}),
            dcc.Dropdown(
                id='segment-filter',
                options=[{'label': 'All Segments', 'value': 'All'}] +
                         [{'label': s, 'value': s} for s in segments],
                value='All', clearable=False,
                style={'color': '#0D1117', 'fontSize': '14px', 'borderRadius': '6px'},
            )
        ], style={'width': '15%', 'minWidth': '140px'}),
        html.Div([
            html.Label('Shipping:', style={'color': CSS['muted'], 'fontSize': '11px', 'fontWeight': '600',
                                            'textTransform': 'uppercase', 'letterSpacing': '0.5px',
                                            'marginBottom': '4px', 'display': 'block'}),
            dcc.Dropdown(
                id='shipping-filter',
                options=[{'label': 'All Modes', 'value': 'All'}] +
                         [{'label': s, 'value': s} for s in shipping_modes],
                value='All', clearable=False,
                style={'color': '#0D1117', 'fontSize': '14px', 'borderRadius': '6px'},
            )
        ], style={'width': '15%', 'minWidth': '140px'}),
    ], style={
        'display': 'flex', 'flexWrap': 'wrap', 'gap': '12px', 'alignItems': 'flex-end',
        'backgroundColor': CSS['card'], 'padding': '16px 20px', 'borderRadius': '10px',
        'border': f'1px solid {CSS["card_border"]}',
        'margin': '0 8px 20px 8px'
    })
    
    # =============================================================================
    # TABS
    # =============================================================================
    tabs = dcc.Tabs(id='tabs', value='tab-overview', children=[
        dcc.Tab(label='📊 Overview', value='tab-overview'),
        dcc.Tab(label='💰 Sales', value='tab-sales'),
        dcc.Tab(label='📦 Products', value='tab-products'),
        dcc.Tab(label='👥 Customers', value='tab-customers'),
        dcc.Tab(label='🌍 Regional', value='tab-regional'),
        dcc.Tab(label='📈 Forecasting', value='tab-forecast'),
    ], style={
        'margin': '0 8px 20px 8px',
        'fontSize': '15px',
    })
    
    # =============================================================================
    # APP LAYOUT
    # =============================================================================
    app.layout = html.Div(style={
        'backgroundColor': CSS['bg'], 'minHeight': '100vh',
        'fontFamily': '-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif',
        'padding': '0', 'margin': '0',
    }, children=[
        # Header
        html.Header(style={
            'backgroundColor': CSS['header_bg'], 'padding': '20px 30px',
            'borderBottom': f'1px solid {CSS["card_border"]}',
            'display': 'flex', 'justifyContent': 'space-between', 'alignItems': 'center',
            'flexWrap': 'wrap', 'gap': '10px'
        }, children=[
            html.Div([
                html.H1('🛒 E-Commerce Sales Analytics',
                        style={'color': COLOR_PALETTE['primary'], 'margin': '0', 'fontSize': '28px',
                               'fontWeight': '700'}),
                html.P('Interactive Business Intelligence Dashboard',
                        style={'color': CSS['muted'], 'margin': '4px 0 0 0', 'fontSize': '14px',
                               'letterSpacing': '0.3px'}),
            ]),
            html.Div([
                html.Span(f'{datetime.now().strftime("%B %d, %Y")}',
                          style={'color': CSS['muted'], 'fontSize': '13px', 'marginRight': '20px'}),
                html.Span(f'{len(df):,} Orders • {df["Customer ID"].nunique():,} Customers',
                          style={'color': CSS['muted'], 'fontSize': '13px'}),
            ])
        ]),
        
        # Main Content
        html.Main(style={
            'maxWidth': '1600px', 'margin': '0 auto', 'padding': '20px'
        }, children=[
            # Filters
            filter_bar,
            
            # Tabs
            tabs,
            
            # Tab Content
            html.Div(id='tab-content'),
        ]),
        
        # Footer
        html.Footer(style={
            'backgroundColor': CSS['header_bg'], 'padding': '15px 30px',
            'borderTop': f'1px solid {CSS["card_border"]}',
            'textAlign': 'center', 'color': CSS['muted'], 'fontSize': '12px'
        }, children=[
            html.Span('E-Commerce Sales Analytics Dashboard • '),
            html.Span(f'Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'),
            html.Br(),
            html.Span('Built with Dash & Plotly • Data: 15,000+ e-commerce transactions'),
        ]),
    ])
    
    # =============================================================================
    # CALLBACKS
    # =============================================================================
    
    @callback(
        Output('tab-content', 'children'),
        [Input('tabs', 'value'),
         Input('year-filter', 'value'),
         Input('category-filter', 'value'),
         Input('region-filter', 'value'),
         Input('segment-filter', 'value'),
         Input('shipping-filter', 'value')]
    )
    def render_tab(tab, year, category, region, segment, shipping):
        """Render content based on selected tab and filters."""
        filtered_df = df.copy()
        
        # Apply filters
        if year and year != 'All':
            filtered_df = filtered_df[filtered_df['Order Date'].dt.year == year]
        if category and category != 'All':
            filtered_df = filtered_df[filtered_df['Category'] == category]
        if region and region != 'All':
            filtered_df = filtered_df[filtered_df['Region'] == region]
        if segment and segment != 'All':
            filtered_df = filtered_df[filtered_df['Segment'] == segment]
        if shipping and shipping != 'All':
            filtered_df = filtered_df[filtered_df['Shipping Mode'] == shipping]
        
        if len(filtered_df) == 0:
            return html.Div('No data matches the selected filters.',
                           style={'color': CSS['muted'], 'textAlign': 'center', 'padding': '40px'})
        
        tab_kpis = calculate_kpis(filtered_df)
        
        if tab == 'tab-overview':
            return render_overview_tab(filtered_df, tab_kpis)
        elif tab == 'tab-sales':
            return render_sales_tab(filtered_df, tab_kpis)
        elif tab == 'tab-products':
            return render_products_tab(filtered_df)
        elif tab == 'tab-customers':
            return render_customers_tab(filtered_df)
        elif tab == 'tab-regional':
            return render_regional_tab(filtered_df)
        elif tab == 'tab-forecast':
            return render_forecast_tab(filtered_df, tab_kpis)
        return html.Div()
    
    return app


# =============================================================================
# TAB RENDERERS
# =============================================================================

def render_overview_tab(df, kpis):
    """Overview tab with key metrics and high-level charts."""
    kpi_cards = html.Div([
        html.Div([
            html.Span(k, style={'color': CSS['muted'], 'fontSize': '11px', 'textTransform': 'uppercase',
                                 'letterSpacing': '0.5px'}),
            html.Div(v, style={'fontSize': '24px', 'fontWeight': '700', 'color': CSS['text'],
                               'marginTop': '4px'})
        ], style={
            'backgroundColor': CSS['card'], 'padding': '14px 18px', 'borderRadius': '8px',
            'border': f'1px solid {CSS["card_border"]}',
            'borderLeft': f'4px solid {[COLOR_PALETTE["primary"], COLOR_PALETTE["success"], COLOR_PALETTE["accent"], COLOR_PALETTE["secondary"], COLOR_PALETTE["primary"], COLOR_PALETTE["danger"]][i % 6]}',
            'flex': '1', 'minWidth': '140px', 'margin': '5px'
        }) for i, (k, v) in enumerate(kpis.items())
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'margin': '0 8px 20px 8px'})
    
    return html.Div([
        section_header('Executive Summary', 'High-level business performance at a glance'),
        kpi_cards,
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_monthly_trend(df), 'monthly-trend'),
            chart_container(create_sales_by_category(df), 'category-pie'),
        ]),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_regional_bar(df), 'regional-bar'),
            chart_container(create_seasonal_heatmap(df), 'seasonal-heatmap'),
        ]),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_monthly_growth(df), 'monthly-growth'),
            chart_container(create_profit_waterfall(df), 'profit-waterfall'),
        ]),
        # Summary Stats
        html.Div([
            section_header('Key Business Insights'),
            html.Div([
                html.Div([
                    html.Div([
                        html.Span('📈', style={'fontSize': '24px'}),
                        html.Div([
                            html.Strong('Revenue Leaders', style={'color': CSS['text'], 'display': 'block'}),
                            html.Span(f"Top Category: {kpis.get('Top Category', 'N/A')}", style={'color': CSS['muted'], 'fontSize': '13px'}),
                            html.Span(f"Top Region: {kpis.get('Top Region', 'N/A')}", style={'color': CSS['muted'], 'fontSize': '13px'}),
                        ], style={'marginLeft': '12px'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'padding': '12px',
                              'borderBottom': f'1px solid {CSS["card_border"]}'}),
                    html.Div([
                        html.Span('💰', style={'fontSize': '24px'}),
                        html.Div([
                            html.Strong('Profitability', style={'color': CSS['text'], 'display': 'block'}),
                            html.Span(f"Profit Margin: {kpis.get('Profit Margin', 'N/A')}", style={'color': CSS['muted'], 'fontSize': '13px'}),
                            html.Span(f"Avg Order Value: {kpis.get('Avg Order Value', 'N/A')}", style={'color': CSS['muted'], 'fontSize': '13px'}),
                        ], style={'marginLeft': '12px'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'padding': '12px',
                              'borderBottom': f'1px solid {CSS["card_border"]}'}),
                    html.Div([
                        html.Span('🔄', style={'fontSize': '24px'}),
                        html.Div([
                            html.Strong('Customer Metrics', style={'color': CSS['text'], 'display': 'block'}),
                            html.Span(f"Avg Orders/Customer: {kpis.get('Avg Orders/Customer', 'N/A')}", style={'color': CSS['muted'], 'fontSize': '13px'}),
                            html.Span(f"Return Rate: {kpis.get('Return Rate', 'N/A')}", style={'color': CSS['muted'], 'fontSize': '13px'}),
                        ], style={'marginLeft': '12px'})
                    ], style={'display': 'flex', 'alignItems': 'center', 'padding': '12px'})
                ], style={'flex': '1', 'backgroundColor': CSS['card'], 'borderRadius': '10px',
                          'border': f'1px solid {CSS["card_border"]}', 'padding': '10px'})
            ], style={'margin': '0 8px'})
        ], style={'margin': '0 0 20px 0'}),
    ])


def render_sales_tab(df, kpis):
    """Sales analysis tab."""
    return html.Div([
        section_header('Sales Analysis', 'Detailed breakdown of sales performance'),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_monthly_trend(df), 'sales-monthly'),
            chart_container(create_monthly_growth(df), 'sales-growth'),
        ]),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_discount_analysis(df), 'sales-discount'),
            chart_container(create_profit_margin_scatter(df), 'sales-margin-scatter'),
        ]),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_seasonal_heatmap(df), 'sales-heatmap'),
            chart_container(create_weekday_analysis(df), 'sales-weekday'),
        ]),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_payment_analysis(df), 'sales-payment'),
            chart_container(create_shipping_analysis(df), 'sales-shipping'),
        ]),
    ])


def render_products_tab(df):
    """Product analysis tab."""
    return html.Div([
        section_header('Product Analysis', 'Product portfolio performance and category insights'),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_top_products(df, 15), 'prod-top'),
            chart_container(create_subcategory_sales(df), 'prod-subcat'),
        ]),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_sales_by_category(df), 'prod-category'),
            chart_container(create_profit_waterfall(df), 'prod-profit'),
        ]),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_return_analysis(df), 'prod-returns'),
            chart_container(create_profit_margin_scatter(df), 'prod-margin-scatter'),
        ]),
    ])


def render_customers_tab(df):
    """Customer analysis tab."""
    return html.Div([
        section_header('Customer Analysis', 'Customer behavior, segmentation, and value analysis'),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_segment_analysis(df), 'cust-segment'),
            chart_container(create_top_customers(df, 15), 'cust-top'),
        ]),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_weekday_analysis(df), 'cust-weekday'),
            chart_container(create_delivery_analysis(df), 'cust-delivery'),
        ]),
        # Customer Data Table
        html.Div([
            section_header('Customer Data Explorer'),
            html.Div([
                dash_table.DataTable(
                    id='customer-table',
                    columns=[{'name': c, 'id': c, 'selectable': True} for c in
                             ['Customer Name', 'Segment', 'Region', 'State', 'City', 'Sales', 'Profit', 'Quantity']],
                    data=df.groupby(['Customer Name', 'Segment', 'Region', 'State', 'City']).agg(
                        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'), Quantity=('Quantity', 'sum')
                    ).reset_index().sort_values('Sales', ascending=False).head(50).to_dict('records'),
                    page_size=15,
                    style_table={'overflowX': 'auto'},
                    style_header={
                        'backgroundColor': '#21262D', 'color': CSS['text'],
                        'fontWeight': '600', 'textTransform': 'uppercase', 'fontSize': '11px',
                        'letterSpacing': '0.5px', 'border': 'none'
                    },
                    style_cell={
                        'backgroundColor': CSS['card'], 'color': CSS['text'],
                        'border': f'1px solid {CSS["card_border"]}', 'padding': '10px 15px',
                        'fontFamily': 'SF Mono, Monaco, monospace', 'fontSize': '13px'
                    },
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': '#1C2128'},
                        {'if': {'column_id': 'Sales'}, 'color': COLOR_PALETTE['primary']},
                        {'if': {'column_id': 'Profit'}, 'color': COLOR_PALETTE['success']},
                    ],
                    sort_action='native',
                    filter_action='native',
                    export_format='csv',
                    export_headers='display',
                )
            ], style={
                'backgroundColor': CSS['card'], 'borderRadius': '10px',
                'border': f'1px solid {CSS["card_border"]}', 'padding': '10px', 'margin': '0 8px'
            })
        ]),
    ])


def render_regional_tab(df):
    """Regional analysis tab."""
    return html.Div([
        section_header('Regional Analysis', 'Geographic performance and market insights'),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_sales_map(df), 'reg-map'),
            chart_container(create_regional_bar(df), 'reg-bar'),
        ]),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(create_seasonal_heatmap(df), 'reg-heatmap'),
            chart_container(create_shipping_analysis(df), 'reg-shipping'),
        ]),
    ])


def render_forecast_tab(df, kpis):
    """Forecasting & trends tab."""
    monthly = df.set_index('Order Date').resample('ME').agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum')
    ).reset_index()
    
    # Simple moving average
    monthly['Sales_MA3'] = monthly['Sales'].rolling(3).mean()
    monthly['Sales_MA6'] = monthly['Sales'].rolling(6).mean()
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly['Order Date'], y=monthly['Sales'],
                         name='Actual Sales', marker_color=COLOR_PALETTE['primary'],
                         opacity=0.6,
                         hovertemplate='%{x|%b %Y}<br>Sales: $%{y:,.0f}<extra>Actual</extra>'))
    fig.add_trace(go.Scatter(x=monthly['Order Date'], y=monthly['Sales_MA3'],
                              name='3-Month Moving Avg',
                              line=dict(color=COLOR_PALETTE['accent'], width=3),
                              hovertemplate='%{x|%b %Y}<br>MA(3): $%{y:,.0f}<extra></extra>'))
    fig.add_trace(go.Scatter(x=monthly['Order Date'], y=monthly['Sales_MA6'],
                              name='6-Month Moving Avg',
                              line=dict(color=COLOR_PALETTE['success'], width=3, dash='dot'),
                              hovertemplate='%{x|%b %Y}<br>MA(6): $%{y:,.0f}<extra></extra>'))
    fig.update_layout(
        title='Sales Trends with Moving Averages',
        template='plotly_dark',
        paper_bgcolor=CSS['card'], plot_bgcolor=CSS['card'],
        xaxis=dict(gridcolor='#2D333B'),
        yaxis=dict(title='Sales ($)', gridcolor='#2D333B'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=40),
    )
    
    # Year-over-Year comparison
    df['Year'] = df['Order Date'].dt.year
    df['Month'] = df['Order Date'].dt.month
    df['MonthName'] = df['Order Date'].dt.strftime('%b')
    yoy = df.groupby(['Year', 'MonthName', 'Month'])['Sales'].sum().reset_index()
    yoy = yoy.sort_values(['Year', 'Month'])
    
    years = sorted(yoy['Year'].unique())
    fig_yoy = go.Figure()
    colors = [COLOR_PALETTE['primary'], COLOR_PALETTE['secondary'],
              COLOR_PALETTE['accent'], COLOR_PALETTE['success']]
    for i, yr in enumerate(years):
        yr_data = yoy[yoy['Year'] == yr]
        fig_yoy.add_trace(go.Scatter(
            x=yr_data['MonthName'], y=yr_data['Sales'],
            mode='lines+markers', name=str(yr),
            line=dict(width=3, color=colors[i % len(colors)]),
            hovertemplate=f'{yr}<br>%{{x}}<br>Sales: $%{{y:,.0f}}<extra></extra>'
        ))
    fig_yoy.update_layout(
        title='Year-over-Year Sales Comparison',
        template='plotly_dark',
        paper_bgcolor=CSS['card'], plot_bgcolor=CSS['card'],
        xaxis=dict(gridcolor='#2D333B'),
        yaxis=dict(title='Sales ($)', gridcolor='#2D333B'),
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=40),
    )
    
    # Growth metrics
    yearly = df.groupby('Year').agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'), Customers=('Customer ID', 'nunique')
    ).reset_index()
    yearly['Sales_Growth'] = yearly['Sales'].pct_change() * 100
    yearly['Profit_Growth'] = yearly['Profit'].pct_change() * 100
    
    fig_growth = go.Figure()
    fig_growth.add_trace(go.Bar(name='Sales Growth %', x=yearly['Year'].astype(str),
                                y=yearly['Sales_Growth'],
                                marker_color=COLOR_PALETTE['primary'],
                                hovertemplate='%{y:.1f}%<extra>Sales Growth</extra>'))
    fig_growth.add_trace(go.Bar(name='Profit Growth %', x=yearly['Year'].astype(str),
                                y=yearly['Profit_Growth'],
                                marker_color=COLOR_PALETTE['success'],
                                hovertemplate='%{y:.1f}%<extra>Profit Growth</extra>'))
    fig_growth.update_layout(
        title='Year-over-Year Growth Rates',
        template='plotly_dark',
        paper_bgcolor=CSS['card'], plot_bgcolor=CSS['card'],
        yaxis=dict(title='Growth Rate (%)', gridcolor='#2D333B', ticksuffix='%'),
        barmode='group',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1),
        margin=dict(t=50, b=40),
    )
    
    return html.Div([
        section_header('Forecasting & Trends', 'Sales trends, moving averages, and year-over-year comparisons'),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(fig, 'forecast-trend'),
            chart_container(fig_yoy, 'forecast-yoy'),
        ]),
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            chart_container(fig_growth, 'forecast-growth'),
            chart_container(create_monthly_growth(df), 'forecast-mom'),
        ]),
        # Yearly Summary Table
        html.Div([
            section_header('Yearly Performance Summary'),
            html.Div([
                dash_table.DataTable(
                    columns=[{'name': c.replace('_', ' ').title(), 'id': c} for c in yearly.columns],
                    data=yearly.round(2).to_dict('records'),
                    style_table={'overflowX': 'auto'},
                    style_header={
                        'backgroundColor': '#21262D', 'color': CSS['text'],
                        'fontWeight': '600', 'fontSize': '12px', 'border': 'none'
                    },
                    style_cell={
                        'backgroundColor': CSS['card'], 'color': CSS['text'],
                        'border': f'1px solid {CSS["card_border"]}', 'padding': '10px 15px',
                        'fontFamily': 'SF Mono, Monaco, monospace', 'fontSize': '13px'
                    },
                    style_data_conditional=[
                        {'if': {'row_index': 'odd'}, 'backgroundColor': '#1C2128'},
                    ],
                )
            ], style={
                'backgroundColor': CSS['card'], 'borderRadius': '10px',
                'border': f'1px solid {CSS["card_border"]}', 'padding': '10px', 'margin': '0 8px'
            })
        ]),
    ])


# =============================================================================
# STATIC HTML REPORT GENERATION
# =============================================================================
def generate_html_report(df):
    """Generate a comprehensive static HTML report with all charts embedded."""
    charts = [
        ('Monthly Sales & Profit Trend', create_monthly_trend),
        ('Sales by Category', create_sales_by_category),
        ('Regional Performance', create_regional_bar),
        ('Top 15 Products', lambda d: create_top_products(d, 15)),
        ('Customer Segment Analysis', create_segment_analysis),
        ('Discount Impact', create_discount_analysis),
        ('Monthly Growth Rate', create_monthly_growth),
        ('Seasonal Heatmap', create_seasonal_heatmap),
        ('Payment Analysis', create_payment_analysis),
    ]
    
    charts_html = ""
    for title, chart_func in charts:
        try:
            fig = chart_func(df)
            fig.update_layout(
                paper_bgcolor='#0E1117', plot_bgcolor='#0E1117',
                font=dict(color='#E6EDF3'),
                title=dict(text=title, font=dict(color='#E6EDF3'))
            )
            charts_html += f'<div style="margin: 24px 0;">{fig.to_html(full_html=False, include_plotlyjs=False)}</div>\n'
        except Exception as e:
            charts_html += f'<div style="color: #C73E1D; margin: 20px;">Error rendering {title}: {e}</div>\n'
    
    kpis = calculate_kpis(df)
    kpi_rows = ''.join(
        f'<tr><td style="padding:10px 16px;border:1px solid #30363D;color:#8B949E">{k}</td>'
        f'<td style="padding:10px 16px;border:1px solid #30363D;font-weight:700;color:#2E86AB;font-family:monospace">{v}</td></tr>'
        for k, v in kpis.items()
    )
    
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-Commerce Sales Analytics Report</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            background: #0E1117; color: #E6EDF3;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            padding: 0; margin: 0;
        }}
        .header {{
            background: #0D1117; padding: 30px 40px;
            border-bottom: 1px solid #30363D;
            text-align: center;
        }}
        .header h1 {{ color: #2E86AB; font-size: 32px; font-weight: 700; margin-bottom: 8px; }}
        .header p {{ color: #8B949E; font-size: 16px; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 20px; }}
        .kpi-grid {{
            display: flex; flex-wrap: wrap; gap: 12px;
            justify-content: center; margin: 24px 0;
        }}
        .kpi-card {{
            background: #161B22; border: 1px solid #30363D;
            border-radius: 8px; padding: 16px 24px;
            min-width: 150px; flex: 1; text-align: center;
        }}
        .kpi-card .label {{ color: #8B949E; font-size: 11px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .kpi-card .value {{ font-size: 22px; font-weight: 700; color: #E6EDF3; margin-top: 6px; font-family: monospace; }}
        table {{ border-collapse: collapse; width: 100%; max-width: 800px; margin: 20px auto; }}
        th {{ background: #2E86AB; color: white; padding: 12px 16px; font-size: 13px; text-transform: uppercase; }}
        .section {{ margin: 32px 0; }}
        .section h2 {{ color: #44BBA4; font-size: 24px; border-bottom: 1px solid #30363D; padding-bottom: 10px; margin-bottom: 20px; }}
        .chart-container {{ margin: 20px 0; }}
        footer {{ text-align: center; color: #8B949E; padding: 20px; border-top: 1px solid #30363D; margin-top: 40px; font-size: 12px; }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 24px; }}
            .kpi-card {{ min-width: 120px; }}
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🛒 E-Commerce Sales Analytics Report</h1>
        <p>Comprehensive Business Intelligence Report</p>
        <p style="color:#8B949E;font-size:13px;margin-top:8px">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
    </div>
    <div class="container">
        <div class="section">
            <h2>📊 Key Performance Indicators</h2>
            <div class="kpi-grid">
                {''.join(f'<div class="kpi-card" style="border-left:4px solid {[COLOR_PALETTE["primary"], COLOR_PALETTE["success"], COLOR_PALETTE["accent"], COLOR_PALETTE["secondary"], COLOR_PALETTE["primary"], COLOR_PALETTE["danger"]][i % 6]}"><div class="label">{k}</div><div class="value">{v}</div></div>' for i, (k, v) in enumerate(kpis.items()))}
            </div>
        </div>
        <div class="section">
            <h2>📈 Charts & Visualizations</h2>
            {charts_html}
        </div>
    </div>
    <footer>
        E-Commerce Sales Analytics Dashboard &bull; Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} &bull; Data: 15,000+ transactions
    </footer>
</body>
</html>'''
    
    report_path = os.path.join(PROJECT_ROOT, 'reports', 'dashboard_report.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"\n[OK] HTML report saved to: {report_path}")
    return report_path


# =============================================================================
# MAIN
# =============================================================================
def main():
    print("=" * 60)
    print("E-COMMERCE INTERACTIVE DASHBOARD")
    print("=" * 60)
    
    print("\nLoading data...")
    df = load_data()
    print(f"  [OK] Loaded {len(df):,} records with {len(df.columns)} columns")
    
    print("\nGenerating static HTML report...")
    try:
        generate_html_report(df)
    except Exception as e:
        print(f"  [WARN] Could not generate HTML report: {e}")
    
    if DASH_AVAILABLE:
        print("\nStarting interactive dashboard...")
        print("  URL: http://localhost:8050")
        print("  Press Ctrl+C to stop\n")
        app = create_app_layout(df)
        app.run(debug=False, host='0.0.0.0', port=8050)
    else:
        print("\n" + "=" * 60)
        print("DASHBOARD READY!")
        print("=" * 60)
        print("\nTo view the interactive dashboard:")
        print("  1. pip install dash plotly")
        print("  2. python python/dashboard.py")
        print("  3. Open http://localhost:8050 in your browser")
        print("\nStatic report generated:")
        print("  - reports/dashboard_report.html (open in browser)")


if __name__ == '__main__':
    main()
