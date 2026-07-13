# E-Commerce Sales Analytics & Business Intelligence Dashboard

## Functional Specification Document (FSD)

---

### Document Control

| **Document Name** | E-Commerce Sales Analytics FSD |
|---|---|
| **Version** | 1.0 |
| **Date** | January 2024 |
| **Author** | Business Analytics Team |

---

### 1. Introduction

This Functional Specification Document details the system functions, features, and user interfaces for the E-Commerce Sales Analytics & Business Intelligence Dashboard. It builds upon the Business Requirements Document and provides technical specifications for implementation.

---

### 2. System Architecture

#### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        DATA SOURCES                         │
│                (CSV Files / Raw Data)                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    PYTHON ETL PIPELINE                       │
│  clean_data.py → validate_data.py → analysis.py             │
└─────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│   POSTGRESQL DATABASE   │     │     CLEANED CSV FILES       │
│   (Normalized Schema)    │     │     (Data/cleaned/)         │
└─────────────────────────┘     └─────────────────────────────┘
              │                               │
              │                               ▼
              │                    ┌─────────────────────────┐
              │                    │   POWER BI DASHBOARD    │
              │                    │   (8 Pages + Slicers)   │
              │                    └─────────────────────────┘
              │                               │
              ▼                               ▼
┌─────────────────────────┐     ┌─────────────────────────────┐
│     SQL ANALYTICS       │     │      EXCEL REPORTS          │
│   (50+ Queries)         │     │   (Pivot Tables + Charts)   │
└─────────────────────────┘     └─────────────────────────────┘
```

#### 2.2 Technology Stack

| **Component** | **Technology** | **Version** |
|---|---|---|
| Programming Language | Python | 3.8+ |
| Data Processing | Pandas, NumPy | Latest |
| Database | PostgreSQL | 15+ |
| Visualization | Power BI Desktop | Latest |
| Reporting | Excel (xlsxwriter) | - |
| Charts | Matplotlib, Seaborn | Latest |
| Version Control | Git + GitHub | - |
| IDE | VS Code | Latest |

---

### 3. Functional Modules

#### Module 1: Data Ingestion & Cleaning

| **Function** | **Description** | **Input** | **Output** |
|---|---|---|---|
| `load_raw_data()` | Load CSV files from data/raw/ directory | CSV files | Pandas DataFrames |
| `handle_missing_values()` | Detect and impute missing values | DataFrame | Cleaned DataFrame |
| `remove_duplicates()` | Remove duplicate records | DataFrame | Deduplicated DataFrame |
| `detect_and_handle_outliers()` | Detect outliers using IQR/Z-score | DataFrame | Capped DataFrame |
| `engineer_features()` | Create derived features | DataFrame | Enhanced DataFrame |
| `standardize_dtypes()` | Standardize data types | DataFrame | Typed DataFrame |
| `generate_quality_report()` | Generate data quality metrics | DataFrame | Quality report CSV |

**Implementation File:** `python/clean_data.py`

#### Module 2: Data Validation

| **Function** | **Description** |
|---|---|
| `run_all_checks()` | Execute all validation checks |
| `_check_schema()` | Verify expected columns and structure |
| `_check_data_types()` | Validate data type correctness |
| `_check_numeric_ranges()` | Check numeric value boundaries |
| `_check_categorical_domains()` | Validate categorical values |
| `_check_uniqueness()` | Check uniqueness constraints |
| `_check_referential_integrity()` | Cross-dataset relationship checks |
| `_check_business_rules()` | Business logic validation |

**Implementation File:** `python/validate_data.py`

#### Module 3: SQL Database

**Schema Objects:**

| **Object Type** | **Count** | **Details** |
|---|---|---|
| Tables | 11 | Regions, States, Cities, Categories, SubCategories, Customers, Products, Shipping, Payments, Orders, Order_Items, Returns |
| Views | 3 | vw_order_summary, vw_product_performance, vw_customer_ltv |
| Stored Procedures | 2 | sp_get_sales_by_date_range, sp_get_top_customers |
| Triggers | 1 | update_customers_updated_at |
| Indexes | 12+ | Performance indexes on frequently queried columns |

**Implementation File:** `sql/schema.sql`, `sql/insert.sql`

#### Module 4: Business Analysis & KPIs

**KPI Calculations:**

| **KPI** | **Formula** |
|---|---|
| Total Sales | `SUM(Sales)` |
| Total Profit | `SUM(Profit)` |
| Profit Margin | `(SUM(Profit) / SUM(Sales)) * 100` |
| Average Order Value (AOV) | `SUM(Sales) / COUNT(DISTINCT Order_ID)` |
| Customer Lifetime Value | `SUM(Sales_per_Customer)` |
| Repeat Purchase Rate | `(Repeat_Customers / Total_Customers) * 100` |
| Return Rate | `(Returned_Items / Total_Items) * 100` |
| Monthly Growth Rate | `((Current_Month_Sales - Prev_Month_Sales) / Prev_Month_Sales) * 100` |
| Revenue per Customer | `SUM(Sales) / COUNT(DISTINCT Customer_ID)` |
| Orders per Customer | `COUNT(DISTINCT Order_ID) / COUNT(DISTINCT Customer_ID)` |

**Implementation File:** `python/analysis.py`, `sql/analysis_queries.sql`

#### Module 5: Power BI Dashboard Pages

| **Page** | **Visuals** | **Purpose** |
|---|---|---|
| Executive Summary | KPI Cards, Line Charts, Map | High-level business overview |
| Sales Dashboard | Bar Charts, Treemap, Slicers | Detailed sales analysis |
| Profit Dashboard | Waterfall, Donut, Scatter | Profitability analysis |
| Customer Dashboard | Customer Table, Segment Analysis | Customer insights |
| Regional Dashboard | Map, State/Region Charts | Geographic performance |
| Product Dashboard | Product Performance, Category Analysis | Product insights |
| Forecast Dashboard | Forecast Lines, Confidence Bands | Predictive analytics |
| KPI Dashboard | Gauges, Trend Indicators | KPI monitoring |

**Implementation File:** `powerbi/Ecommerce Dashboard.pbix`

#### Module 6: Report Generation

| **Report** | **Frequency** | **Format** |
|---|---|---|
| Monthly Sales Report | Monthly | Excel, CSV |
| Quarterly Business Review | Quarterly | Excel, CSV |
| Yearly Performance Report | Yearly | Excel, CSV |
| Customer Analysis Report | On-demand | Excel, CSV |
| Product Performance Report | On-demand | Excel, CSV |
| Regional Analysis Report | On-demand | Excel, CSV |

**Implementation File:** `python/export_reports.py`

---

### 4. Data Dictionary

#### Table: Orders (Main Fact Table)

| **Column** | **Type** | **Description** | **Constraints** |
|---|---|---|---|
| Order ID | VARCHAR(20) | Unique order identifier | PK |
| Order Date | DATE | Date order was placed | NOT NULL |
| Ship Date | DATE | Date order was shipped | >= Order Date |
| Shipping Mode | VARCHAR(50) | Shipping service level | FK to Shipping |
| Customer ID | VARCHAR(20) | Customer identifier | FK to Customers |
| Customer Name | VARCHAR(200) | Customer full name | NOT NULL |
| Segment | VARCHAR(50) | Customer segment | Consumer/Corporate/Home Office |
| Region | VARCHAR(50) | Geographic region | FK to Regions |
| State | VARCHAR(100) | US State | FK to States |
| City | VARCHAR(100) | City | FK to Cities |
| Category | VARCHAR(100) | Product category | FK to Categories |
| Sub-Category | VARCHAR(100) | Product sub-category | FK to SubCategories |
| Product Name | VARCHAR(300) | Product description | NOT NULL |
| Sales | DECIMAL(12,2) | Final sales amount | >= 0 |
| Quantity | INTEGER | Units purchased | > 0 |
| Discount | DECIMAL(4,2) | Discount applied | 0-1 |
| Profit | DECIMAL(12,2) | Profit/Loss amount | Calculated |
| Shipping Cost | DECIMAL(10,2) | Shipping charges | >= 0 |
| Payment Mode | VARCHAR(50) | Payment method | FK to Payments |
| Return Status | VARCHAR(20) | Return indicator | Returned/Not Returned |

*Full data dictionary with 60+ columns available in `documentation/Data_Dictionary.xlsx`*

---

### 5. SQL Analysis Categories

| **Category** | **Query Count** | **Description** |
|---|---|---|
| Sales Overview | 10 | Total sales, trends, growth rates |
| Product Analysis | 10 | Top products, categories, margins |
| Customer Analysis | 10 | LTV, segments, retention |
| Regional Analysis | 10 | State/City/Region performance |
| Discount & Profit | 10 | Discount impact, profit analysis |
| Advanced Analytics | 10 | Forecasting, cohorts, cross-sell |
| Business KPIs | 5 | Key performance indicators |
| Data Quality | 3 | Validation and audit queries |

---

### 6. Python Scripts Specification

| **Script** | **Purpose** | **Functions** | **Dependencies** |
|---|---|---|---|
| `clean_data.py` | Data cleaning pipeline | 10 | pandas, numpy |
| `validate_data.py` | Data validation engine | 10 | pandas, numpy, json |
| `analysis.py` | Business analysis & charts | 15 | pandas, numpy, matplotlib, seaborn |
| `export_reports.py` | Report generation | 12 | pandas, numpy, xlsxwriter |

---

### 7. Error Handling

| **Error Type** | **Handling Strategy** | **Logging** |
|---|---|---|
| Missing files | Graceful fallback with warning | WARNING |
| Data type errors | Coercion with error logging | ERROR |
| Validation failures | Report generation without abort | ERROR |
| Division by zero | NULLIF protection | INFO |
| Encoding issues | UTF-8 with fallback | WARNING |

---

### 8. Performance Requirements

| **Metric** | **Target** | **Measurement** |
|---|---|---|
| Data loading (15K records) | < 5 seconds | Timer |
| Data cleaning pipeline | < 30 seconds | Timer |
| SQL query execution | < 1 second per query | EXPLAIN ANALYZE |
| Dashboard page load | < 5 seconds | Power BI Performance Analyzer |
| Report generation | < 2 minutes | Timer |
| Chart generation (all) | < 30 seconds | Timer |

---

### 9. File Structure

```
Ecommerce-Sales-Analytics/
├── data/
│   ├── raw/           # Source CSV data
│   ├── cleaned/        # Processed data
│   └── database/       # Database files
├── sql/               # SQL scripts
├── python/            # Python scripts
├── powerbi/           # Power BI files
├── excel/             # Excel reports
├── reports/           # Generated reports
├── presentation/      # Project presentation
├── documentation/     # Project documentation
├── README.md          # Project overview
├── requirements.txt   # Python dependencies
├── .gitignore         # Git ignore file
└── LICENSE            # MIT License
```

---

### 10. Testing Strategy

| **Test Type** | **Scope** | **Tools** |
|---|---|---|
| Data Quality | Missing values, duplicates, outliers | Python scripts |
| Validation | Schema, domains, referential integrity | validate_data.py |
| SQL | Query correctness, performance | PostgreSQL EXPLAIN |
| Dashboard | Visual accuracy, filter functionality | Manual testing |
| Report | Data accuracy, formatting | Visual inspection |

---

### 11. Deployment Instructions

1. Clone repository from GitHub
2. Install Python dependencies: `pip install -r requirements.txt`
3. Run data generation: `python data/raw/generate_dataset.py`
4. Run cleaning pipeline: `python python/clean_data.py`
5. Run validation: `python python/validate_data.py`
6. Run analysis: `python python/analysis.py`
7. Load data into PostgreSQL: Execute `sql/schema.sql` and `sql/insert.sql`
8. Open Power BI dashboard: `powerbi/Ecommerce Dashboard.pbix`
9. Generate reports: `python python/export_reports.py`

---

### Document Approval

| **Role** | **Name** | **Signature** | **Date** |
|---|---|---|---|
| Business Analyst | [Name] | | |
| Technical Lead | [Name] | | |
| QA Lead | [Name] | | |
