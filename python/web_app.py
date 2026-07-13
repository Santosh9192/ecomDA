"""
=============================================================================
E-Commerce Sales Analytics - Flask Web Application
=============================================================================
Description: A web application wrapper that serves the analytics dashboard,
             provides REST API endpoints, and hosts the interactive dashboard.
Usage: python python/web_app.py
       Then open http://localhost:5000 in your browser
=============================================================================
"""

import pandas as pd
import numpy as np
import os
import sys
from datetime import datetime, timedelta

from flask import Flask, jsonify, request, send_file

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# Import shared utilities
try:
    from python.analytics_utils import (
        load_data, get_filtered_data, calculate_numeric_kpis, to_native,
        get_filter_options, COLOR_PALETTE
    )
except ImportError:
    from analytics_utils import (
        load_data, get_filtered_data, calculate_numeric_kpis, to_native,
        get_filter_options, COLOR_PALETTE
    )

app = Flask(__name__)

# Path to the static HTML report
REPORT_PATH = os.path.join(PROJECT_ROOT, 'reports', 'dashboard_report.html')


# =============================================================================
# HELPERS
# =============================================================================

def get_report_html():
    """Read and return the static HTML report content."""
    if os.path.exists(REPORT_PATH):
        with open(REPORT_PATH, 'r', encoding='utf-8') as f:
            return f.read()
    return None


NAV_STYLES = '''
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: #0E1117; color: #E6EDF3;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;
            min-height: 100vh;
        }
        .navbar {
            background: #0D1117; padding: 14px 24px;
            border-bottom: 1px solid #30363D;
            display: flex; justify-content: space-between; align-items: center;
            flex-wrap: wrap; gap: 10px;
        }
        .navbar .logo { color: #2E86AB; font-size: 20px; font-weight: 700; text-decoration: none; display: flex; align-items: center; gap: 8px; }
        .navbar .nav-links { display: flex; gap: 8px; align-items: center; }
        .navbar .nav-links a {
            color: #8B949E; text-decoration: none; font-size: 13px;
            padding: 6px 12px; border-radius: 6px; transition: all 0.2s;
        }
        .navbar .nav-links a:hover { color: #E6EDF3; background: #21262D; }
        .navbar .nav-links a.active { color: #2E86AB; background: #1C2128; }
        footer {
            text-align: center; padding: 20px; color: #8B949E;
            border-top: 1px solid #30363D; margin-top: 40px; font-size: 12px;
        }
        .container { max-width: 1400px; margin: 0 auto; padding: 20px; }
    </style>
'''

NAVBAR = '''
    <nav class="navbar">
        <a href="/" class="logo">🛒 E-Commerce Analytics</a>
        <div class="nav-links">
            <a href="/" class="ACTIVE_HOME">Home</a>
            <a href="/dashboard" class="ACTIVE_DASH">Dashboard</a>
            <a href="/report" class="ACTIVE_REPORT">Report</a>
            <a href="/dash" class="ACTIVE_DASH2">Interactive</a>
            <a href="/api/kpis" class="ACTIVE_API">API</a>
            <a href="/api/docs" class="ACTIVE_DOCS">API Docs</a>
        </div>
    </nav>
'''

FOOTER = '''
    <footer>
        E-Commerce Sales Analytics Platform &bull; Built with Flask &bull; ''' + datetime.now().strftime('%Y-%m-%d') + '''
    </footer>
'''


# =============================================================================
# ROUTES
# =============================================================================

@app.route('/')
def index():
    """Landing page with project overview and navigation."""
    df = load_data()
    kpis = calculate_numeric_kpis(df) if not df.empty else {}
    
    nav = NAVBAR.replace('ACTIVE_HOME', 'active').replace('ACTIVE_DASH', '').replace('ACTIVE_REPORT', '').replace('ACTIVE_DASH2', '').replace('ACTIVE_API', '').replace('ACTIVE_DOCS', '')
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>E-Commerce Sales Analytics</title>
        {NAV_STYLES}
        <style>
            .hero {{
                text-align: center; padding: 60px 20px 40px;
                background: linear-gradient(180deg, #0D1117 0%, #0E1117 100%);
            }}
            .hero h1 {{ font-size: 42px; color: #2E86AB; margin-bottom: 12px; }}
            .hero p {{ font-size: 18px; color: #8B949E; max-width: 700px; margin: 0 auto; line-height: 1.6; }}
            .stats-grid {{
                display: flex; flex-wrap: wrap; gap: 16px; justify-content: center;
                padding: 20px; max-width: 1200px; margin: 0 auto;
            }}
            .stat-card {{
                background: #161B22; border: 1px solid #30363D;
                border-radius: 10px; padding: 20px 24px;
                flex: 1; min-width: 180px; max-width: 220px;
                transition: transform 0.2s, box-shadow 0.2s;
            }}
            .stat-card:hover {{ transform: translateY(-4px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); }}
            .stat-card .label {{ color: #8B949E; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; }}
            .stat-card .value {{ font-size: 26px; font-weight: 700; margin-top: 8px; font-family: monospace; }}
            .feature-grid {{
                display: flex; flex-wrap: wrap; gap: 20px; justify-content: center;
                padding: 20px; max-width: 1200px; margin: 0 auto;
            }}
            .feature-card {{
                background: #161B22; border: 1px solid #30363D;
                border-radius: 10px; padding: 24px;
                flex: 1; min-width: 280px; max-width: 350px;
                transition: transform 0.2s;
            }}
            .feature-card:hover {{ transform: translateY(-2px); }}
            .feature-card .icon {{ font-size: 32px; margin-bottom: 12px; }}
            .feature-card h3 {{ color: #E6EDF3; font-size: 18px; margin-bottom: 8px; }}
            .feature-card p {{ color: #8B949E; font-size: 13px; line-height: 1.5; }}
            .feature-card a {{
                display: inline-block; margin-top: 12px; color: #2E86AB;
                text-decoration: none; font-weight: 600; font-size: 13px;
            }}
            .feature-card a:hover {{ color: #44BBA4; }}
            .section-title {{
                text-align: center; padding: 30px 20px 10px;
                font-size: 28px; color: #E6EDF3;
            }}
            .section-subtitle {{
                text-align: center; color: #8B949E; font-size: 15px;
                margin-bottom: 20px;
            }}
            @media (max-width: 768px) {{
                .hero h1 {{ font-size: 28px; }}
                .stat-card {{ min-width: 140px; }}
            }}
        </style>
    </head>
    <body>
        {nav}

        <div class="hero">
            <h1>E-Commerce Sales Analytics</h1>
            <p>Transforming raw e-commerce transaction data into actionable business insights through interactive dashboards, RESTful APIs, and automated reporting.</p>
        </div>

        <h2 class="section-title">📊 Key Metrics</h2>
        <p class="section-subtitle">Real-time performance indicators from {len(df):,} transactions</p>
        <div class="stats-grid">
            {''.join(
                f'<div class="stat-card" style="border-left: 4px solid {["#2E86AB", "#44BBA4", "#F18F01", "#A23B72", "#2E86AB", "#C73E1D", "#44BBA4", "#F18F01", "#A23B72"][i % 9]};">'
                f'<div class="label">{k.replace("_", " ").title()}</div>'
                f'<div class="value" style="color: {["#2E86AB", "#44BBA4", "#F18F01", "#A23B72", "#2E86AB", "#C73E1D", "#44BBA4", "#F18F01", "#A23B72"][i % 9]};">'
                f'{"$" + f"{v:,.2f}" if k in ["total_sales","total_profit","avg_order_value","avg_profit_per_order"] else (f"{v:,.0f}" if k in ["total_orders","total_customers","total_items_sold"] else (f"{v}%" if k in ["profit_margin","return_rate","repeat_purchase_rate"] else str(v)))}'
                f'</div></div>'
                for i, (k, v) in enumerate(kpis.items())
            )}
        </div>

        <h2 class="section-title">🚀 Explore</h2>
        <p class="section-subtitle">Navigate through the analytics platform</p>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="icon">📈</div>
                <h3>Interactive Dashboard</h3>
                <p>Explore 20+ visualizations across 6 tabs with real-time filtering by year, category, region, segment, and shipping mode.</p>
                <a href="/dashboard">Open Dashboard →</a>
            </div>
            <div class="feature-card">
                <div class="icon">📊</div>
                <h3>Full Analytics Report</h3>
                <p>View a comprehensive static report with KPI cards, charts, and key business insights all on one page.</p>
                <a href="/report">View Report →</a>
            </div>
            <div class="feature-card">
                <div class="icon">🎮</div>
                <h3>Interactive (Dash)</h3>
                <p>Launch the full Plotly/Dash interactive dashboard with filters, tabs, drill-downs, and real-time data exploration.</p>
                <a href="/dash">Launch Interactive →</a>
            </div>
            <div class="feature-card">
                <div class="icon">🔌</div>
                <h3>REST API</h3>
                <p>Access analytics data programmatically via JSON endpoints. Perfect for integrating with other applications and services.</p>
                <a href="/api/docs">View API Docs →</a>
            </div>
            <div class="feature-card">
                <div class="icon">📋</div>
                <h3>Reports & Downloads</h3>
                <p>Access generated reports including Excel files, CSV exports, and downloadable data from the analytics pipeline.</p>
                <a href="/api/reports">Access Reports →</a>
            </div>
        </div>

        {FOOTER}
    </body>
    </html>
    '''


@app.route('/dashboard')
def dashboard():
    """Serve the full analytics report with all charts embedded directly in the Flask app."""
    report_html = get_report_html()
    
    nav = NAVBAR.replace('ACTIVE_HOME', '').replace('ACTIVE_DASH', 'active').replace('ACTIVE_REPORT', '').replace('ACTIVE_DASH2', '').replace('ACTIVE_API', '').replace('ACTIVE_DOCS', '')
    
    if report_html:
        # Inject navbar and footer into the report by modifying the HTML
        report_html = report_html.replace(
            '<body>',
            f'<body>{nav}'
        ).replace(
            '</footer>',
            f'</footer>{FOOTER}'
        )
        # Remove the report's own header since we have the navbar
        report_html = report_html.replace(
            '<div class="header">',
            '<div class="header" style="padding-top: 30px;">'
        )
        return report_html
    else:
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dashboard - E-Commerce Analytics</title>
            {NAV_STYLES}
            <style>
                .no-report {{
                    text-align: center; padding: 80px 20px;
                }}
                .no-report h2 {{ color: #2E86AB; font-size: 28px; margin-bottom: 16px; }}
                .no-report p {{ color: #8B949E; font-size: 16px; line-height: 1.6; margin-bottom: 8px; }}
                .no-report code {{ background: #21262D; padding: 3px 8px; border-radius: 4px; color: #E6EDF3; }}
                .btn {{
                    display: inline-block; margin-top: 20px; background: #2E86AB; color: white;
                    text-decoration: none; padding: 12px 28px; border-radius: 6px;
                    font-size: 15px; font-weight: 600; transition: background 0.2s;
                }}
                .btn:hover {{ background: #44BBA4; }}
            </style>
        </head>
        <body>
            {nav}
            <div class="no-report">
                <h2>📊 Report Not Available</h2>
                <p>The static report hasn't been generated yet. Generate it by running:</p>
                <p><code>python python/dashboard.py</code></p>
                <p>Or launch the interactive Dash dashboard:</p>
                <a href="/dash" class="btn">🚀 Launch Interactive Dashboard</a>
            </div>
            {FOOTER}
        </body>
        </html>
        '''


@app.route('/report')
def report():
    """Serve the static HTML analytics report."""
    df = load_data()
    report_html = get_report_html()
    
    nav = NAVBAR.replace('ACTIVE_HOME', '').replace('ACTIVE_DASH', '').replace('ACTIVE_REPORT', 'active').replace('ACTIVE_DASH2', '').replace('ACTIVE_API', '').replace('ACTIVE_DOCS', '')
    
    if report_html:
        report_html = report_html.replace(
            '<body>',
            f'<body>{nav}'
        ).replace(
            '</footer>',
            f'</footer>{FOOTER}'
        )
        report_html = report_html.replace(
            '<div class="header">',
            '<div class="header" style="padding-top: 30px;">'
        )
        return report_html
    else:
        return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Report - E-Commerce Analytics</title>
            {NAV_STYLES}
            <style>
                .no-report {{ text-align: center; padding: 80px 20px; }}
                .no-report h2 {{ color: #2E86AB; font-size: 28px; margin-bottom: 16px; }}
                .no-report p {{ color: #8B949E; font-size: 16px; }}
                .no-report code {{ background: #21262D; padding: 3px 8px; border-radius: 4px; color: #E6EDF3; }}
                .btn {{
                    display: inline-block; margin-top: 20px; background: #2E86AB; color: white;
                    text-decoration: none; padding: 12px 28px; border-radius: 6px;
                    font-size: 15px; font-weight: 600; transition: background 0.2s;
                }}
                .btn:hover {{ background: #44BBA4; }}
            </style>
        </head>
        <body>
            {nav}
            <div class="no-report">
                <h2>📊 Report Not Available</h2>
                <p>Generate it with: <code>python python/dashboard.py</code></p>
                <a href="/dash" class="btn">🚀 Launch Interactive Dashboard Instead</a>
            </div>
            {FOOTER}
        </body>
        </html>
        '''


@app.route('/dash')
def dash_iframe():
    """Embed the interactive Dash dashboard in an iframe."""
    df = load_data()
    kpis = calculate_numeric_kpis(df) if not df.empty else {}
    
    nav = NAVBAR.replace('ACTIVE_HOME', '').replace('ACTIVE_DASH', '').replace('ACTIVE_REPORT', '').replace('ACTIVE_DASH2', 'active').replace('ACTIVE_API', '').replace('ACTIVE_DOCS', '')
    
    quick_stats = ''
    if kpis:
        quick_stats = f'''
        <div class="quick-stats">
            <div class="quick-stat"><div class="label">Total Sales</div><div class="value" style="color:#2E86AB">${kpis.get("total_sales",0):,.0f}</div></div>
            <div class="quick-stat"><div class="label">Total Profit</div><div class="value" style="color:#44BBA4">${kpis.get("total_profit",0):,.0f}</div></div>
            <div class="quick-stat"><div class="label">Profit Margin</div><div class="value" style="color:#F18F01">{kpis.get("profit_margin",0):.1f}%</div></div>
            <div class="quick-stat"><div class="label">Orders</div><div class="value" style="color:#A23B72">{kpis.get("total_orders",0):,}</div></div>
            <div class="quick-stat"><div class="label">Customers</div><div class="value" style="color:#2E86AB">{kpis.get("total_customers",0):,}</div></div>
            <div class="quick-stat"><div class="label">Avg Order</div><div class="value" style="color:#44BBA4">${kpis.get("avg_order_value",0):,.0f}</div></div>
        </div>
        '''
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Interactive Dashboard - E-Commerce Analytics</title>
        {NAV_STYLES}
        <style>
            .quick-stats {{
                display: flex; flex-wrap: wrap; gap: 10px; margin: 16px auto;
                max-width: 1400px; padding: 0 20px;
            }}
            .quick-stat {{
                background: #161B22; border: 1px solid #30363D;
                border-radius: 8px; padding: 10px 14px; flex: 1; min-width: 100px;
                text-align: center;
            }}
            .quick-stat .label {{ color: #8B949E; font-size: 10px; text-transform: uppercase; letter-spacing: 0.5px; }}
            .quick-stat .value {{ color: #E6EDF3; font-size: 16px; font-weight: 700; margin-top: 3px; }}
            .dash-container {{
                max-width: 1600px; margin: 0 auto; padding: 0 20px 20px;
            }}
            .dash-info {{
                background: #161B22; border: 1px solid #30363D; border-radius: 8px;
                padding: 12px 16px; margin: 0 auto 16px; max-width: 1400px;
                display: flex; justify-content: space-between; align-items: center;
                flex-wrap: wrap; gap: 8px;
            }}
            .dash-info p {{ color: #8B949E; font-size: 13px; }}
            .dash-info p code {{ background: #21262D; padding: 2px 6px; border-radius: 3px; color: #E6EDF3; font-size: 12px; }}
            .dash-info .status {{
                display: flex; align-items: center; gap: 8px;
            }}
            .dash-info .status-dot {{
                width: 10px; height: 10px; border-radius: 50%; display: inline-block;
            }}
            .status-dot.online {{ background: #44BBA4; box-shadow: 0 0 6px #44BBA4; }}
            .status-dot.offline {{ background: #C73E1D; box-shadow: 0 0 6px #C73E1D; }}
            iframe {{
                width: 100%; height: calc(100vh - 180px); border: none;
                border-radius: 8px; background: #0E1117;
            }}
            .dash-fallback {{
                text-align: center; padding: 60px 20px;
            }}
            .dash-fallback h2 {{ color: #2E86AB; margin-bottom: 12px; }}
            .dash-fallback p {{ color: #8B949E; margin-bottom: 8px; line-height: 1.6; }}
            .dash-fallback code {{ background: #21262D; padding: 2px 8px; border-radius: 4px; font-size: 14px; color: #E6EDF3; }}
            .btn {{
                display: inline-block; margin-top: 16px; background: #2E86AB; color: white;
                text-decoration: none; padding: 10px 24px; border-radius: 6px;
                font-size: 14px; font-weight: 600; transition: background 0.2s;
            }}
            .btn:hover {{ background: #44BBA4; }}
        </style>
    </head>
    <body>
        {nav}
        
        {quick_stats}
        
        <div class="dash-info">
            <div class="status">
                <span class="status-dot online"></span>
                <p>Dash Interactive Dashboard — running on <code>localhost:8050</code></p>
            </div>
            <p>Filter by year, category, region, segment, and shipping mode in the embedded dashboard</p>
        </div>
        
        <div class="dash-container">
            <iframe src="http://localhost:8050" title="Dash Interactive Dashboard"></iframe>
        </div>
        
        {FOOTER}
    </body>
    </html>
    '''


@app.route('/api/docs')
def api_docs():
    """API documentation page."""
    nav = NAVBAR.replace('ACTIVE_HOME', '').replace('ACTIVE_DASH', '').replace('ACTIVE_REPORT', '').replace('ACTIVE_DASH2', '').replace('ACTIVE_API', '').replace('ACTIVE_DOCS', 'active')
    
    return f'''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>API Docs - E-Commerce Analytics</title>
        {NAV_STYLES}
        <style>
            h1 {{ color: #2E86AB; font-size: 32px; margin-bottom: 8px; }}
            .subtitle {{ color: #8B949E; font-size: 16px; margin-bottom: 30px; }}
            .endpoint {{ background: #161B22; border: 1px solid #30363D; border-radius: 8px; margin-bottom: 16px; overflow: hidden; }}
            .endpoint-header {{ display: flex; align-items: center; padding: 14px 18px; border-bottom: 1px solid #30363D; gap: 12px; }}
            .method {{ font-size: 11px; font-weight: 700; padding: 3px 8px; border-radius: 4px; text-transform: uppercase; letter-spacing: 0.5px; }}
            .method.get {{ background: #1C3A28; color: #44BBA4; }}
            .endpoint-url {{ color: #E6EDF3; font-family: monospace; font-size: 15px; font-weight: 600; }}
            .endpoint-desc {{ padding: 14px 18px; }}
            .endpoint-desc p {{ color: #8B949E; font-size: 13px; margin-bottom: 8px; }}
            .endpoint-desc code {{ background: #21262D; padding: 2px 6px; border-radius: 3px; font-size: 12px; color: #E6EDF3; }}
            .response-sample {{ background: #0D1117; padding: 12px 16px; border-radius: 6px; margin-top: 8px; font-family: monospace; font-size: 12px; color: #8B949E; overflow-x: auto; white-space: pre; }}
            h2 {{ color: #E6EDF3; font-size: 22px; margin: 30px 0 16px; }}
        </style>
    </head>
    <body>
        {nav}
        <div class="container">
            <h1>🔌 API Documentation</h1>
            <p class="subtitle">RESTful endpoints for accessing e-commerce analytics data programmatically.</p>
            
            <h2>📊 Metrics Endpoints</h2>
            
            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/kpis</span>
                </div>
                <div class="endpoint-desc">
                    <p>Get all key business KPIs including total sales, profit, margins, customer metrics, and top performers.</p>
                    <p>Optional query parameters: <code>year</code>, <code>category</code>, <code>region</code>, <code>segment</code></p>
                    <div class="response-sample">{{
    "total_sales": 7530312.05,
    "total_profit": 2678439.65,
    "profit_margin": 35.57,
    "total_orders": 15000,
    "total_customers": 2000,
    "avg_order_value": 502.02
}}</div>
                </div>
            </div>

            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/sales/overview</span>
                </div>
                <div class="endpoint-desc">
                    <p>Get monthly sales and profit data for trend analysis.</p>
                    <p>Optional query parameters: <code>year</code>, <code>category</code>, <code>region</code></p>
                </div>
            </div>
            
            <h2>📦 Product Endpoints</h2>

            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/products/top</span>
                </div>
                <div class="endpoint-desc">
                    <p>Get top N products by sales revenue. Optional query parameter: <code>limit</code> (default: 10)</p>
                </div>
            </div>

            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/products/categories</span>
                </div>
                <div class="endpoint-desc">
                    <p>Get sales breakdown by category and sub-category.</p>
                </div>
            </div>
            
            <h2>👥 Customer Endpoints</h2>

            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/customers/top</span>
                </div>
                <div class="endpoint-desc">
                    <p>Get top customers by total spend. Optional query parameter: <code>limit</code> (default: 10)</p>
                </div>
            </div>

            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/customers/segments</span>
                </div>
                <div class="endpoint-desc">
                    <p>Get customer segment analysis with sales and profit metrics.</p>
                </div>
            </div>
            
            <h2>🌍 Regional Endpoints</h2>

            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/regions</span>
                </div>
                <div class="endpoint-desc">
                    <p>Get regional performance data including sales by state and region.</p>
                </div>
            </div>

            <div class="endpoint">
                <div class="endpoint-header">
                    <span class="method get">GET</span>
                    <span class="endpoint-url">/api/shipping</span>
                </div>
                <div class="endpoint-desc">
                    <p>Get shipping mode analysis with costs and order volumes.</p>
                </div>
            </div>
        </div>
        {FOOTER}
    </body>
    </html>
    '''


# =============================================================================
# API ROUTES
# =============================================================================

@app.route('/api/kpis')
def api_kpis():
    """Get all KPIs."""
    year = request.args.get('year')
    category = request.args.get('category')
    region = request.args.get('region')
    segment = request.args.get('segment')
    
    df = get_filtered_data(year, category, region, segment)
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    kpis = calculate_numeric_kpis(df)
    return jsonify(kpis)


@app.route('/api/sales/overview')
def api_sales_overview():
    """Get monthly sales overview."""
    year = request.args.get('year')
    category = request.args.get('category')
    region = request.args.get('region')
    
    df = get_filtered_data(year, category, region)
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    monthly = df.groupby(df['Order Date'].dt.to_period('M')).agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index()
    monthly['month'] = monthly['Order Date'].astype(str)
    
    result = []
    for _, row in monthly.iterrows():
        result.append({
            'month': str(row['month']),
            'sales': round(float(row['Sales']), 2),
            'profit': round(float(row['Profit']), 2),
            'orders': int(row['Orders']),
        })
    
    return jsonify(result)


@app.route('/api/products/top')
def api_top_products():
    """Get top products by sales."""
    limit = request.args.get('limit', 10, type=int)
    df = get_filtered_data()
    
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    top = df.groupby(['Product Name', 'Category', 'Sub-Category']).agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'),
        Quantity=('Quantity', 'sum'), Orders=('Order ID', 'nunique')
    ).reset_index().sort_values('Sales', ascending=False).head(limit)
    
    result = []
    for _, row in top.iterrows():
        result.append({
            'product_name': str(row['Product Name']),
            'category': str(row['Category']),
            'subcategory': str(row['Sub-Category']),
            'sales': round(float(row['Sales']), 2),
            'profit': round(float(row['Profit']), 2),
            'quantity': int(row['Quantity']),
            'orders': int(row['Orders']),
            'margin': round(float(row['Profit'] / row['Sales'] * 100), 2) if row['Sales'] > 0 else 0,
        })
    
    return jsonify(result)


@app.route('/api/products/categories')
def api_categories():
    """Get category breakdown."""
    df = get_filtered_data()
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    cats = df.groupby(['Category', 'Sub-Category']).agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'), Quantity=('Quantity', 'sum')
    ).reset_index()
    
    result = []
    for _, row in cats.iterrows():
        result.append({
            'category': str(row['Category']),
            'subcategory': str(row['Sub-Category']),
            'sales': round(float(row['Sales']), 2),
            'profit': round(float(row['Profit']), 2),
            'orders': int(row['Orders']),
            'quantity': int(row['Quantity']),
        })
    
    return jsonify(sorted(result, key=lambda x: x['sales'], reverse=True))


@app.route('/api/customers/top')
def api_top_customers():
    """Get top customers."""
    limit = request.args.get('limit', 10, type=int)
    df = get_filtered_data()
    
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    top = df.groupby(['Customer Name', 'Segment', 'Region']).agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique')
    ).reset_index().sort_values('Sales', ascending=False).head(limit)
    
    result = []
    for _, row in top.iterrows():
        result.append({
            'customer_name': str(row['Customer Name']),
            'segment': str(row['Segment']),
            'region': str(row['Region']),
            'sales': round(float(row['Sales']), 2),
            'profit': round(float(row['Profit']), 2),
            'orders': int(row['Orders']),
        })
    
    return jsonify(result)


@app.route('/api/customers/segments')
def api_customer_segments():
    """Get segment analysis."""
    df = get_filtered_data()
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    segments = df.groupby('Segment').agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'), Customers=('Customer ID', 'nunique')
    ).reset_index()
    
    result = []
    for _, row in segments.iterrows():
        result.append({
            'segment': str(row['Segment']),
            'sales': round(float(row['Sales']), 2),
            'profit': round(float(row['Profit']), 2),
            'orders': int(row['Orders']),
            'customers': int(row['Customers']),
            'avg_order_value': round(float(row['Sales'] / row['Orders']), 2) if row['Orders'] > 0 else 0,
        })
    
    return jsonify(result)


@app.route('/api/regions')
def api_regions():
    """Get regional performance."""
    df = get_filtered_data()
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    regions = df.groupby(['Region', 'State']).agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'), Customers=('Customer ID', 'nunique')
    ).reset_index()
    
    result = []
    for _, row in regions.iterrows():
        result.append({
            'region': str(row['Region']),
            'state': str(row['State']),
            'sales': round(float(row['Sales']), 2),
            'profit': round(float(row['Profit']), 2),
            'orders': int(row['Orders']),
            'customers': int(row['Customers']),
        })
    
    return jsonify(sorted(result, key=lambda x: x['sales'], reverse=True))


@app.route('/api/shipping')
def api_shipping():
    """Get shipping analysis."""
    df = get_filtered_data()
    if df.empty:
        return jsonify({'error': 'No data found'}), 404
    
    shipping = df.groupby('Shipping Mode').agg(
        Sales=('Sales', 'sum'), Profit=('Profit', 'sum'),
        Orders=('Order ID', 'nunique'),
        Avg_Shipping_Cost=('Shipping Cost', 'mean')
    ).reset_index()
    
    result = []
    for _, row in shipping.iterrows():
        result.append({
            'shipping_mode': str(row['Shipping Mode']),
            'sales': round(float(row['Sales']), 2),
            'profit': round(float(row['Profit']), 2),
            'orders': int(row['Orders']),
            'avg_shipping_cost': round(float(row['Avg_Shipping_Cost']), 2),
        })
    
    return jsonify(result)


@app.route('/api/reports')
def api_reports():
    """List available generated reports."""
    reports_dir = os.path.join(PROJECT_ROOT, 'reports')
    excel_dir = os.path.join(PROJECT_ROOT, 'excel', 'reports')
    
    available = {'csv': [], 'excel': [], 'other': []}
    
    for f in os.listdir(reports_dir):
        if f.endswith('.csv'):
            available['csv'].append({
                'name': f,
                'path': f'/download/reports/{f}'
            })
        elif f.endswith('.html'):
            available['other'].append({
                'name': f,
                'path': f'/download/reports/{f}'
            })
    
    if os.path.exists(excel_dir):
        for f in os.listdir(excel_dir):
            if f.endswith('.xlsx'):
                available['excel'].append({
                    'name': f,
                    'path': f'/download/excel/{f}'
                })
    
    return jsonify(available)


@app.route('/download/reports/<filename>')
def download_report(filename):
    """Download a generated report file."""
    filepath = os.path.join(PROJECT_ROOT, 'reports', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404


@app.route('/download/excel/<filename>')
def download_excel(filename):
    """Download an Excel report file."""
    filepath = os.path.join(PROJECT_ROOT, 'excel', 'reports', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404


# =============================================================================
# ERROR HANDLERS
# =============================================================================
@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500


# =============================================================================
# MAIN
# =============================================================================
def main():
    """Main entry point for the Flask web application."""
    print("=" * 60)
    print("E-COMMERCE WEB APPLICATION")
    print("=" * 60)
    
    df = load_data()
    if df.empty:
        print("\n[WARN] No data found. Run the data generation pipeline first:")
        print("  1. python data/raw/generate_dataset.py")
        print("  2. python python/clean_data.py")
    else:
        print(f"\n  [OK] Data loaded: {len(df):,} records")
    
    report_exists = os.path.exists(REPORT_PATH)
    print(f"  [{'OK' if report_exists else 'WARN'}] {'Static report found' if report_exists else 'Static report not found — run python python/dashboard.py to generate'}")
    
    print("\nStarting web application...")
    print("  URL: http://localhost:5000")
    print("  Dashboard: http://localhost:5000/dashboard")
    print("  Report: http://localhost:5000/report")
    print("  Interactive Dash: http://localhost:5000/dash")
    print("  API Docs: http://localhost:5000/api/docs")
    print("  API KPIs: http://localhost:5000/api/kpis")
    print("  Press Ctrl+C to stop\n")
    
    # Try port 5000, fallback to 5001 if busy
    port = 5000
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', port))
    sock.close()
    if result == 0:
        port = 5001
        print(f"  Port 5000 in use, using port {port}")
    app.run(debug=False, host='0.0.0.0', port=port)


if __name__ == '__main__':
    main()
