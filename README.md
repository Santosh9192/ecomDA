<div align="center">

# 🛒 E-Commerce Sales Analytics & Business Intelligence Dashboard

**A Comprehensive Business Analytics Portfolio Project**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://python.org)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15%2B-336791?logo=postgresql&logoColor=white)](https://postgresql.org)
[![Power BI](https://img.shields.io/badge/Power_BI-Desktop-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com)
[![Pandas](https://img.shields.io/badge/Pandas-2.0+-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

**Transforming Raw E-Commerce Data into Actionable Business Insights**

[📊 Dashboard Preview](#-power-bi-dashboard) •
[📈 Features](#-key-features) •
[🗄️ SQL Analytics](#%EF%B8%8F-sql-analytics) •
[🐍 Python Pipeline](#-python-pipeline) •
[📁 Project Structure](#-project-structure) •
[🚀 Getting Started](#-getting-started)

---

</div>

## 📋 Project Overview

A complete **Business Intelligence solution** for analyzing e-commerce sales data. This project demonstrates professional-level data analysis skills including **data cleaning, validation, SQL analytics, Python data processing, interactive dashboards, and automated reporting**.

> **What makes this project stand out:**
> - Industry-standard folder structure (GitHub-ready)
> - 15,000+ realistic transactional records
> - 50+ Business SQL queries with CTEs, Window Functions, Views & Stored Procedures
> - Production-grade Python ETL pipeline with PEP8 compliance
> - Professional Power BI dashboard with 8 analytical pages
> - Comprehensive documentation (BRD, FS, Technical Docs, Data Dictionary)

## 🎯 Key Features

### 📊 **Data Analysis & Processing**
| Feature | Description |
|---------|-------------|
| **Data Cleaning** | Automated pipeline handling missing values, duplicates, outliers |
| **Data Validation** | Comprehensive quality checks with 30+ validation rules |
| **Feature Engineering** | 15+ derived features for deeper analysis |
| **Outlier Detection** | IQR and Z-score methods for anomaly detection |

### 🗄️ **SQL Analytics**
| Feature | Description |
|---------|-------------|
| **50+ Queries** | Comprehensive analysis across all business dimensions |
| **Window Functions** | Running totals, moving averages, rankings |
| **CTEs & Joins** | Complex analytical queries with Common Table Expressions |
| **Views** | Pre-built views for common reporting needs |
| **Stored Procedures** | Reusable analysis procedures with parameters |
| **Performance Tuning** | Strategic indexing for query optimization |

### 📈 **Business KPIs**
| KPI | Description |
|-----|-------------|
| Total Sales & Profit | Revenue and profitability metrics |
| Profit Margin | Percentage-based profitability analysis |
| Average Order Value (AOV) | Revenue per transaction |
| Customer Lifetime Value (LTV) | Long-term customer revenue |
| Repeat Purchase Rate | Customer retention measurement |
| Monthly Growth Rate | Period-over-period performance |
| Return Rate | Product quality indicator |

### 🐍 **Python Analytics Pipeline**
- Modular ETL pipeline with 4 specialized scripts
- Automated chart generation (Matplotlib + Seaborn)
- Statistical analysis and business insights extraction
- Excel and CSV report generation with formatting

### 📊 **Power BI Dashboard**
- **8 Interactive Pages**: Executive Summary, Sales, Profit, Customer, Regional, Product, Forecast, KPI
- **20+ Visualizations**: Cards, bar charts, pie/donut charts, treemaps, maps, line charts, scatter plots
- **Interactive Features**: Slicers, bookmarks, drill-through, tooltips, dynamic filters
- **Dark Modern Theme**: Professional corporate design

### 📋 **Automated Reporting**
- **Monthly/Quarterly/Yearly** sales reports
- **Customer, Product, Regional** analysis reports
- **Excel** reports with pivot tables and conditional formatting
- **CSV** exports for further analysis

## 🛠️ Tech Stack

<div align="center">

| Category | Technologies |
|----------|-------------|
| **Languages** | ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white) ![SQL](https://img.shields.io/badge/SQL-CC2927?style=flat&logo=postgresql&logoColor=white) |
| **Data Processing** | ![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white) ![NumPy](https://img.shields.io/badge/NumPy-013243?style=flat&logo=numpy&logoColor=white) |
| **Visualization** | ![Power BI](https://img.shields.io/badge/Power_BI-F2C811?style=flat&logo=powerbi&logoColor=black) ![Matplotlib](https://img.shields.io/badge/Matplotlib-3776AB?style=flat&logo=python&logoColor=white) ![Seaborn](https://img.shields.io/badge/Seaborn-3776AB?style=flat&logo=python&logoColor=white) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat&logo=postgresql&logoColor=white) |
| **Reporting** | ![Excel](https://img.shields.io/badge/Excel-217346?style=flat&logo=microsoft-excel&logoColor=white) |
| **Tools** | ![Git](https://img.shields.io/badge/Git-F05032?style=flat&logo=git&logoColor=white) ![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat&logo=visual-studio-code&logoColor=white) |

</div>

## 📁 Project Structure

```
Ecommerce-Sales-Analytics/
│
├── 📂 data/
│   ├── 📂 raw/              # Source CSV datasets
│   │   ├── ecommerce_orders.csv    # 15,000 order records
│   │   ├── customers.csv           # 2,000 customer records
│   │   ├── regions.csv             # Regional reference data
│   │   ├── categories.csv          # Category reference data
│   │   └── generate_dataset.py     # Synthetic data generator
│   ├── 📂 cleaned/          # Processed & cleaned datasets
│   └── 📂 database/         # Database files
│
├── 📂 sql/
│   ├── schema.sql           # Complete database schema (11 tables)
│   ├── insert.sql           # Data insertion & ETL scripts
│   └── analysis_queries.sql # 50+ Business SQL queries
│
├── 📂 python/
│   ├── clean_data.py        # Data cleaning pipeline
│   ├── validate_data.py     # Data validation engine
│   ├── analysis.py          # Business analysis & charts
│   └── export_reports.py    # Report generation module
│
├── 📂 powerbi/
│   └── Ecommerce Dashboard.pbix  # Power BI dashboard file
│
├── 📂 excel/
│   └── Dashboard.xlsx       # Excel dashboard with pivot tables
│
├── 📂 reports/
│   ├── 📂 pdf/              # PDF reports
│   ├── 📂 screenshots/      # Dashboard screenshots & charts
│   └── business_insights.csv # Extracted business insights
│
├── 📂 presentation/
│   └── Project Presentation.pptx  # Project overview slides
│
├── 📂 documentation/
│   ├── Business_Requirements.md   # BRD document
│   ├── Functional_Specification.md # FS document
│   ├── Technical_Documentation.md  # Technical docs
│   ├── ER_Diagram.md              # Entity Relationship Diagram
│   └── Data_Dictionary.md         # Complete data dictionary
│
├── README.md               # Project overview (this file)
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
└── LICENSE                 # MIT License
```

## 🗄️ SQL Analytics (50+ Queries)

### Query Categories

| Category | Count | Description |
|----------|-------|-------------|
| **Sales Overview** | 10 | Total sales, trends, growth rates, running totals |
| **Product Analysis** | 10 | Top products, categories, margins, returns |
| **Customer Analysis** | 10 | LTV, segments, retention, cohorts |
| **Regional Analysis** | 10 | State/City/Region performance |
| **Discount & Profit** | 10 | Discount impact, profit analysis |
| **Advanced Analytics** | 10 | YoY comparison, moving averages, cross-selling |
| **Business KPIs** | 5 | Key performance indicator queries |
| **Data Quality** | 3 | Validation and audit queries |

### Sample Query: Customer Lifetime Value
```sql
CREATE OR REPLACE VIEW vw_customer_ltv AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.sales) AS total_sales,
    SUM(oi.profit) AS total_profit,
    ROUND(SUM(oi.sales) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS avg_order_value,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS last_order_date
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
LEFT JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name, c.segment;
```

## 🐍 Python Pipeline

### Script Overview

| Script | Description | Key Functions |
|--------|-------------|---------------|
| `clean_data.py` | Automated data cleaning | Missing values, duplicates, outliers, feature engineering |
| `validate_data.py` | Data quality validation | Schema, types, ranges, domains, referential integrity |
| `analysis.py` | Business analysis & charts | KPI calculation, 9 chart types, insight extraction |
| `export_reports.py` | Report generation | Excel, CSV, and text report exports |

### Run the Pipeline

```bash
# Step 1: Generate synthetic data
python data/raw/generate_dataset.py

# Step 2: Clean and process data
python python/clean_data.py

# Step 3: Validate data quality
python python/validate_data.py

# Step 4: Run analysis and generate charts
python python/analysis.py

# Step 5: Export reports
python python/export_reports.py
```

## 📊 Power BI Dashboard

### Dashboard Pages

| Page | Visuals | Key Insights |
|------|---------|--------------|
| **Executive Summary** | KPI Cards, Line Charts, Map | High-level business health overview |
| **Sales Dashboard** | Bar Charts, Treemap, Slicers | Detailed sales performance analysis |
| **Profit Dashboard** | Waterfall, Donut, Scatter | Profitability drivers and trends |
| **Customer Dashboard** | Customer Table, Segments | Customer behavior and segmentation |
| **Regional Dashboard** | Map, State/Region Charts | Geographic performance analysis |
| **Product Dashboard** | Product Charts, Categories | Product portfolio performance |
| **Forecast Dashboard** | Forecast Lines, Confidence | Sales predictions and trends |
| **KPI Dashboard** | Gauges, Trend Indicators | Critical metric monitoring |

### Features
- ✅ **Dark Modern Theme** - Professional corporate styling
- ✅ **Interactive Slicers** - Filter by Date, Region, Category, Segment
- ✅ **Drill-Through Navigation** - Click-through to detailed pages
- ✅ **Custom Tooltips** - Rich hover information
- ✅ **Bookmarks** - Saved view states
- ✅ **Dynamic Measures** - DAX calculated columns and measures

## 💡 Business Insights

### Key Findings (Expected from Analysis)

1. **Revenue Drivers**: Technology products generate highest revenue but Office Supplies have better profit margins
2. **Customer Segments**: Consumer segment contributes the most orders, but Corporate has higher AOV
3. **Regional Performance**: West and East regions outperform Central and South in sales volume
4. **Discount Impact**: High discounts (>20%) negatively impact profitability without proportional volume increase
5. **Seasonal Trends**: Q4 (Holiday season) shows peak sales; summer months show decline
6. **Product Returns**: Return rates vary by product category; Technology has highest return rate
7. **Customer Retention**: Repeat purchase rate correlates with customer segment and order value
8. **Shipping Analysis**: Standard Class is most used; Same Day shipping has highest profit margin

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL 15+ (optional, for database features)
- Power BI Desktop (to view .pbix dashboard)
- Git

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/Ecommerce-Sales-Analytics.git
cd Ecommerce-Sales-Analytics

# 2. Create and activate virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Generate synthetic data
python data/raw/generate_dataset.py

# 5. Run the analysis pipeline
python python/clean_data.py
python python/validate_data.py
python python/analysis.py
python python/export_reports.py

# 6. (Optional) Set up PostgreSQL
# Execute sql/schema.sql in your database
# Then execute sql/insert.sql to load data

# 7. Open Power BI Dashboard
# Open powerbi/Ecommerce Dashboard.pbix with Power BI Desktop
```

## 📈 Resume Description

> **E-Commerce Sales Analytics & BI Dashboard** — Developed a comprehensive Business Intelligence solution analyzing 15,000+ e-commerce transactions. Engineered a normalized PostgreSQL database with 11 tables, implemented 50+ analytical SQL queries using advanced techniques (CTEs, Window Functions, Views, Stored Procedures). Built a production-grade Python ETL pipeline for data cleaning, validation, and feature engineering. Created a professional Power BI dashboard with 8 interactive pages featuring KPI cards, trend analysis, geographic mapping, and sales forecasting. Generated automated Excel/CSV reporting with pivot tables. Delivered comprehensive business documentation including BRD, FS, Technical Documentation, and Data Dictionary.

## 🔮 Future Enhancements

- [ ] **Real-time Dashboard** - Live data refresh with streaming
- [ ] **Machine Learning Models** - Customer churn prediction, product recommendation
- [ ] **Web Application** - Flask/Django web interface for interactive analysis
- [ ] **Automated Email Reports** - Scheduled report distribution
- [ ] **API Integration** - REST API for data access
- [ ] **A/B Testing Module** - Statistical significance testing
- [ ] **Inventory Analytics** - Stock level and supply chain analysis
- [ ] **Sentiment Analysis** - Customer review and feedback analysis

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

<div align="center">

### ⭐ If you find this project useful, please consider giving it a star!

**Built with ❤️ by the Business Analytics Team**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?logo=github)](https://github.com)

</div>
