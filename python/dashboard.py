"""
=============================================================================
E-Commerce Sales Analytics - Interactive Dashboard (Plotly)
=============================================================================
Description: A self-contained interactive dashboard that runs in the browser.
             This serves as a working alternative/companion to Power BI.
Usage: python python/dashboard.py
       Then open http://localhost:8050 in your browser
Dependencies: pip install dash plotly pandas numpy
=============================================================================
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

# Try to import dash - if not available, skip
try:
    import dash
    from dash import dcc, html, callback, Input, Output, State
    import plotly.express as px
    import plotly.graph_objects as go
    import plotly.io as pio
    DASH_AVAILABLE = True
except ImportError:
    DASH_AVAILABLE = False
    print("Dash not installed. Install with: pip install dash plotly")
    print("Using static mode instead.")

# =============================================================================
# CONFIGURATION
# =============================================================================
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'cleaned', 'orders_cleaned.csv')
RAW_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw', 'ecommerce_orders.csv')
SCREENSHOTS_PATH = os.path.join(PROJECT_ROOT, 'reports', 'screenshots')

DARK_THEME = {
    'bg': '#1E1E1E',
    'card': '#252526',
    'accent': '#2E86AB',
    'accent2': '#44BBA4',
    'text': '#FFFFFF',
    'muted': '#888888',
    'colors': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D', '#3B1F2B', '#44BBA4']
}

# =============================================================================
# DATA LOADING
# =============================================================================
def load_data():
    """Load the cleaned e-commerce data."""
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
    elif os.path.exists(RAW_DATA_PATH):
        df = pd.read_csv(RAW_DATA_PATH)
    else:
        raise FileNotFoundError("No data found. Run generate_dataset.py first.")
    
    # Ensure dates
    for col in ['Order Date', 'Ship Date']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    return df


def calculate_kpis(df):
    """Calculate key business KPIs."""
    return {
        'Total Sales': f"${df['Sales'].sum():,.2f}",
        'Total Profit': f"${df['Profit'].sum():,.2f}",
        'Profit Margin': f"{(df['Profit'].sum() / df['Sales'].sum() * 100):.1f}%",
        'Total Orders': f"{df['Order ID'].nunique():,}",
        'Total Customers': f"{df['Customer ID'].nunique():,}",
        'Avg Order Value': f"${df['Sales'].sum() / df['Order ID'].nunique():,.2f}",
        'Return Rate': f"{(df['Return Status'] == 'Returned').mean() * 100:.1f}%",
        'Top Category': df.groupby('Category')['Sales'].sum().idxmax(),
        'Top Region': df.groupby('Region')['Sales'].sum().idxmax(),
        'Top Product': df.groupby('Product Name')['Sales'].sum().idxmax()
    }


# =============================================================================
# CHART GENERATION (Plotly)
# =============================================================================
def create_monthly_trend(df):
    """Monthly Sales & Profit trend."""
    monthly = df.groupby(df['Order Date'].dt.to_period('M')).agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum')
    ).reset_index()
    monthly['Order Date'] = monthly['Order Date'].astype(str)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(x=monthly['Order Date'], y=monthly['Sales'], 
                         name='Sales', marker_color='#2E86AB'))
    fig.add_trace(go.Scatter(x=monthly['Order Date'], y=monthly['Profit'],
                              name='Profit', yaxis='y2', line=dict(color='#F18F01', width=3),
                              mode='lines+markers'))
    fig.update_layout(title='Monthly Sales & Profit Trend', template='plotly_dark',
                      hovermode='x unified', xaxis_tickangle=-45,
                      yaxis=dict(title='Sales ($)', side='left'),
                      yaxis2=dict(title='Profit ($)', overlaying='y', side='right'))
    return fig


def create_category_pie(df):
    """Category sales distribution."""
    cat_sales = df.groupby('Category')['Sales'].sum().reset_index()
    fig = px.pie(cat_sales, values='Sales', names='Category', 
                 title='Sales by Category',
                 color_discrete_sequence=['#2E86AB', '#A23B72', '#F18F01'],
                 hole=0.4)
    fig.update_layout(template='plotly_dark', showlegend=True)
    fig.update_traces(textinfo='label+percent', textposition='outside')
    return fig


def create_regional_bar(df):
    """Regional sales comparison."""
    regional = df.groupby('Region').agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum')
    ).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(name='Sales', x=regional['Region'], y=regional['Sales'], 
               marker_color='#2E86AB'),
        go.Bar(name='Profit', x=regional['Region'], y=regional['Profit'], 
               marker_color='#44BBA4')
    ])
    fig.update_layout(title='Regional Performance', template='plotly_dark',
                      barmode='group', yaxis=dict(title='Amount ($)'))
    return fig


def create_top_products(df, n=10):
    """Top N products by sales."""
    top = df.groupby('Product Name')['Sales'].sum().nlargest(n).reset_index()
    fig = px.bar(top, x='Sales', y='Product Name', orientation='h',
                 title=f'Top {n} Products by Sales',
                 color='Sales', color_continuous_scale='blues')
    fig.update_layout(template='plotly_dark', yaxis={'categoryorder': 'total ascending'})
    return fig


def create_segment_analysis(df):
    """Customer segment analysis."""
    seg = df.groupby('Segment').agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(name='Sales', x=seg['Segment'], y=seg['Sales'], marker_color='#2E86AB'),
        go.Bar(name='Profit', x=seg['Segment'], y=seg['Profit'], marker_color='#A23B72'),
        go.Bar(name='Orders (÷100)', x=seg['Segment'], y=seg['Orders']/100, marker_color='#44BBA4')
    ])
    fig.update_layout(title='Customer Segment Analysis', template='plotly_dark',
                      barmode='group')
    return fig


def create_discount_analysis(df):
    """Discount impact analysis."""
    df['Discount Range'] = pd.cut(df['Discount'],
        bins=[-0.01, 0, 0.05, 0.10, 0.20, 1.0],
        labels=['0%', '1-5%', '6-10%', '11-20%', '21%+'])
    
    disc = df.groupby('Discount Range', observed=True).agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum')
    ).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(name='Sales', x=disc['Discount Range'], y=disc['Sales'], 
               marker_color='#2E86AB'),
        go.Bar(name='Profit', x=disc['Discount Range'], y=disc['Profit'], 
               marker_color='#C73E1D')
    ])
    fig.update_layout(title='Discount Impact on Sales & Profit', template='plotly_dark',
                      barmode='group', xaxis_title='Discount Range', yaxis_title='Amount ($)')
    return fig


def create_monthly_growth(df):
    """Month-over-month growth rate."""
    monthly = df.set_index('Order Date').resample('ME')['Sales'].sum()
    growth = monthly.pct_change() * 100
    
    fig = go.Figure()
    colors = ['#44BBA4' if g >= 0 else '#C73E1D' for g in growth]
    fig.add_trace(go.Bar(x=growth.index, y=growth.values, marker_color=colors,
                         name='Growth Rate'))
    fig.add_trace(go.Scatter(x=growth.index, y=[0]*len(growth), 
                             mode='lines', line=dict(color='white', width=1),
                             showlegend=False))
    fig.update_layout(title='Month-over-Month Sales Growth', template='plotly_dark',
                      yaxis=dict(title='Growth Rate (%)'), hovermode='x unified',
                      xaxis_title='Month')
    return fig


def create_sales_map(df):
    """Sales by state."""
    state_sales = df.groupby('State')['Sales'].sum().reset_index()
    fig = px.choropleth(state_sales, locations='State', locationmode='USA-states',
                         color='Sales', scope='usa',
                         title='Sales by State',
                         color_continuous_scale='blues')
    fig.update_layout(template='plotly_dark', geo=dict(bgcolor='rgba(0,0,0,0)'))
    return fig


# =============================================================================
# DASHBOARD APP
# =============================================================================
def create_dashboard(df):
    """Create the interactive Dash application."""
    kpis = calculate_kpis(df)
    
    app = dash.Dash(__name__, title='E-Commerce Sales Analytics')
    
    # KPI card component
    def kpi_card(title, value, color='#2E86AB'):
        return html.Div([
            html.Div(title, style={'fontSize': '12px', 'color': '#888', 'marginBottom': '5px'}),
            html.Div(value, style={'fontSize': '24px', 'fontWeight': 'bold', 'color': color})
        ], style={
            'backgroundColor': '#252526', 'padding': '15px', 'borderRadius': '8px',
            'borderLeft': f'4px solid {color}', 'flex': '1', 'margin': '5px'
        })
    
    # Dashboard filter
    year_options = sorted(df['Order Date'].dt.year.dropna().unique())
    category_options = df['Category'].unique().tolist()
    region_options = df['Region'].unique().tolist()
    
    app.layout = html.Div(style={'backgroundColor': '#1E1E1E', 'minHeight': '100vh', 'padding': '20px', 'fontFamily': 'Segoe UI, sans-serif'}, children=[
        # Header
        html.Div([
            html.H1('E-Commerce Sales Analytics', style={'color': '#2E86AB', 'margin': '0', 'fontSize': '32px'}),
            html.P('Interactive Business Intelligence Dashboard', style={'color': '#888', 'margin': '5px 0'})
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        # Filters
        html.Div([
            html.Div([
                html.Label('Year:', style={'color': '#888', 'fontSize': '12px'}),
                dcc.Dropdown(id='year-filter', options=[{'label': 'All', 'value': 'All'}] + [{'label': str(y), 'value': y} for y in year_options],
                            value='All', clearable=False, style={'color': '#333'})
            ], style={'width': '15%', 'display': 'inline-block', 'margin': '0 10px'}),
            html.Div([
                html.Label('Category:', style={'color': '#888', 'fontSize': '12px'}),
                dcc.Dropdown(id='category-filter', options=[{'label': 'All', 'value': 'All'}] + [{'label': c, 'value': c} for c in category_options],
                            value='All', clearable=False, style={'color': '#333'})
            ], style={'width': '15%', 'display': 'inline-block', 'margin': '0 10px'}),
            html.Div([
                html.Label('Region:', style={'color': '#888', 'fontSize': '12px'}),
                dcc.Dropdown(id='region-filter', options=[{'label': 'All', 'value': 'All'}] + [{'label': r, 'value': r} for r in region_options],
                            value='All', clearable=False, style={'color': '#333'})
            ], style={'width': '15%', 'display': 'inline-block', 'margin': '0 10px'}),
        ], style={'backgroundColor': '#252526', 'padding': '15px', 'borderRadius': '8px', 'marginBottom': '20px'}),
        
        # KPI Cards
        html.Div(id='kpi-cards', style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            kpi_card('Total Sales', kpis['Total Sales'], '#2E86AB'),
            kpi_card('Total Profit', kpis['Total Profit'], '#44BBA4'),
            kpi_card('Profit Margin', kpis['Profit Margin'], '#F18F01'),
            kpi_card('Total Orders', kpis['Total Orders'], '#2E86AB'),
            kpi_card('Avg Order Value', kpis['Avg Order Value'], '#A23B72'),
            kpi_card('Return Rate', kpis['Return Rate'], '#C73E1D'),
        ]),
        
        # Charts Row 1
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            html.Div([dcc.Graph(id='monthly-trend', figure=create_monthly_trend(df))],
                     style={'flex': '2', 'minWidth': '500px', 'backgroundColor': '#252526', 'borderRadius': '8px', 'margin': '5px', 'padding': '10px'}),
            html.Div([dcc.Graph(id='category-pie', figure=create_category_pie(df))],
                     style={'flex': '1', 'minWidth': '300px', 'backgroundColor': '#252526', 'borderRadius': '8px', 'margin': '5px', 'padding': '10px'}),
        ]),
        
        # Charts Row 2
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            html.Div([dcc.Graph(id='regional-bar', figure=create_regional_bar(df))],
                     style={'flex': '1', 'minWidth': '400px', 'backgroundColor': '#252526', 'borderRadius': '8px', 'margin': '5px', 'padding': '10px'}),
            html.Div([dcc.Graph(id='segment-analysis', figure=create_segment_analysis(df))],
                     style={'flex': '1', 'minWidth': '400px', 'backgroundColor': '#252526', 'borderRadius': '8px', 'margin': '5px', 'padding': '10px'}),
        ]),
        
        # Charts Row 3
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            html.Div([dcc.Graph(id='top-products', figure=create_top_products(df))],
                     style={'flex': '1', 'minWidth': '400px', 'backgroundColor': '#252526', 'borderRadius': '8px', 'margin': '5px', 'padding': '10px'}),
            html.Div([dcc.Graph(id='discount-analysis', figure=create_discount_analysis(df))],
                     style={'flex': '1', 'minWidth': '400px', 'backgroundColor': '#252526', 'borderRadius': '8px', 'margin': '5px', 'padding': '10px'}),
        ]),
        
        # Charts Row 4
        html.Div(style={'display': 'flex', 'flexWrap': 'wrap', 'marginBottom': '20px'}, children=[
            html.Div([dcc.Graph(id='monthly-growth', figure=create_monthly_growth(df))],
                     style={'flex': '1', 'minWidth': '400px', 'backgroundColor': '#252526', 'borderRadius': '8px', 'margin': '5px', 'padding': '10px'}),
            html.Div([dcc.Graph(id='sales-map', figure=create_sales_map(df))],
                     style={'flex': '1.5', 'minWidth': '500px', 'backgroundColor': '#252526', 'borderRadius': '8px', 'margin': '5px', 'padding': '10px'}),
        ]),
        
        # Summary Stats
        html.Div([
            html.H3('Business Insights', style={'color': '#2E86AB', 'margin': '0 0 10px 0'}),
            html.Div([
                html.Li(f'Technology leads with {(df[df.Category=="Technology"].Sales.sum()/df.Sales.sum()*100):.0f}% of total sales', 
                       style={'color': '#ccc', 'margin': '5px 0'}),
                html.Li(f'Average order value is ${df.Sales.sum()/df["Order ID"].nunique():.0f} across {df["Customer ID"].nunique():,} customers',
                       style={'color': '#ccc', 'margin': '5px 0'}),
                html.Li(f'Return rate is {(df["Return Status"]=="Returned").mean()*100:.1f}% - worth ${df[df["Return Status"]=="Returned"].Sales.sum():,.0f} in affected revenue',
                       style={'color': '#ccc', 'margin': '5px 0'}),
                html.Li(f'Top product: {df.groupby("Product Name")["Sales"].sum().idxmax()} (${df.groupby("Product Name")["Sales"].sum().max():,.0f})',
                       style={'color': '#ccc', 'margin': '5px 0'}),
            ], style={'listStyle': 'none', 'padding': '0'})
        ], style={'backgroundColor': '#252526', 'padding': '20px', 'borderRadius': '8px', 'margin': '5px'}),
    ])
    
    return app


def save_static_screenshots(df):
    """Save all charts as static PNG images for the reports folder."""
    os.makedirs(SCREENSHOTS_PATH, exist_ok=True)
    
    charts = [
        ('monthly_sales_trend.png', create_monthly_trend),
        ('sales_by_category.png', create_category_pie),
        ('regional_performance.png', create_regional_bar),
        ('top_10_products.png', lambda d: create_top_products(d)),
        ('customer_segment_analysis.png', create_segment_analysis),
        ('discount_impact.png', create_discount_analysis),
        ('monthly_growth_rate.png', create_monthly_growth),
        ('sales_by_state_map.png', create_sales_map),
    ]
    
    for filename, chart_func in charts:
        try:
            fig = chart_func(df)
            fig.update_layout(
                paper_bgcolor='#1E1E1E', plot_bgcolor='#1E1E1E',
                font=dict(color='white')
            )
            fig.write_image(os.path.join(SCREENSHOTS_PATH, filename), width=1200, height=600, scale=2)
            print(f"  Saved: {filename}")
        except Exception as e:
            print(f"  Error saving {filename}: {e}")
    
    print(f"\nScreenshots saved to: {SCREENSHOTS_PATH}")


def generate_html_report(df):
    """Generate a static HTML report with all charts embedded."""
    charts_html = ""
    charts = [
        ('Monthly Sales & Profit Trend', create_monthly_trend),
        ('Sales by Category', create_category_pie),
        ('Regional Performance', create_regional_bar),
        ('Top 10 Products', lambda d: create_top_products(d)),
        ('Customer Segment Analysis', create_segment_analysis),
        ('Discount Impact', create_discount_analysis),
        ('Monthly Growth Rate', create_monthly_growth),
    ]
    
    for title, chart_func in charts:
        fig = chart_func(df)
        fig.update_layout(paper_bgcolor='#1E1E1E', plot_bgcolor='#1E1E1E',
                          font=dict(color='white'), title_text=title)
        charts_html += f'<div style="margin: 20px 0;">{fig.to_html(full_html=False, include_plotlyjs=False)}</div>\n'
    
    kpis = calculate_kpis(df)
    kpi_rows = ''.join(f'<tr><td style="padding:8px;border:1px solid #333">{k}</td><td style="padding:8px;border:1px solid #333;font-weight:bold;color:#2E86AB">{v}</td></tr>' for k, v in kpis.items())
    
    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head><title>E-Commerce Sales Analytics Report</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {{ background: #1E1E1E; color: #fff; font-family: 'Segoe UI', sans-serif; padding: 20px; }}
        h1 {{ color: #2E86AB; text-align: center; }}
        table {{ border-collapse: collapse; width: 100%; max-width: 600px; margin: 20px auto; }}
        th {{ background: #2E86AB; color: white; padding: 10px; }}
        td {{ padding: 8px; border: 1px solid #333; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
    </style>
    </head>
    <body>
    <div class="container">
        <h1>E-Commerce Sales Analytics Report</h1>
        <p style="text-align:center;color:#888">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
        <h2 style="color:#44BBA4;text-align:center">Key Performance Indicators</h2>
        <table><tr><th>KPI</th><th>Value</th></tr>{kpi_rows}</table>
        <hr style="border-color:#333;margin:30px 0">
        {charts_html}
    </div>
    </body>
    </html>
    '''
    
    report_path = os.path.join(PROJECT_ROOT, 'reports', 'dashboard_report.html')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"\nHTML report saved to: {report_path}")
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
    print(f"  Loaded {len(df):,} records")
    
    # Static outputs (always available)
    print("\nGenerating static screenshots...")
    save_static_screenshots(df)
    
    print("\nGenerating HTML report...")
    generate_html_report(df)
    
    # Interactive dashboard (requires Dash)
    if DASH_AVAILABLE:
        print("\nStarting interactive dashboard...")
        print("  URL: http://localhost:8050")
        print("  Press Ctrl+C to stop\n")
        app = create_dashboard(df)
        app.run_server(debug=False, host='0.0.0.0', port=8050)
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
        print("  - reports/screenshots/ (PNG images)")
        print("\nPower BI setup:")
        print("  - powerbi/Ecommerce_Dashboard.pbit (Power BI template)")
        print("  - powerbi/DAX_Measures.txt (DAX formulas)")


if __name__ == '__main__':
    main()
