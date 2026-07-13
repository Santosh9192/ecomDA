# E-Commerce Sales Analytics & Business Intelligence Dashboard

## Technical Documentation

---

### Document Control

| **Document Name** | E-Commerce Sales Analytics Technical Documentation |
|---|---|
| **Version** | 1.0 |
| **Date** | January 2024 |
| **Author** | Business Analytics Team |

---

### 1. System Overview

The E-Commerce Sales Analytics & Business Intelligence Dashboard is a comprehensive data analytics solution designed to process, analyze, and visualize e-commerce transaction data. The system implements a complete data pipeline from raw CSV ingestion through cleaning, validation, analysis, and visualization.

#### 1.1 System Requirements

**Hardware Requirements:**
- CPU: 4+ cores (recommended)
- RAM: 8GB minimum (16GB recommended)
- Storage: 1GB free space
- Display: 1920x1080 or higher

**Software Requirements:**
- Python 3.8 or higher
- PostgreSQL 15 or higher (optional)
- Power BI Desktop (for .pbix file)
- Git 2.0+
- VS Code (recommended)

---

### 2. Installation Guide

#### 2.1 Clone Repository

```bash
git clone https://github.com/yourusername/Ecommerce-Sales-Analytics.git
cd Ecommerce-Sales-Analytics
```

#### 2.2 Python Environment Setup

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### 2.3 PostgreSQL Setup (Optional)

```sql
-- Create database
CREATE DATABASE ecommerce_analytics;

-- Execute schema
\i sql/schema.sql

-- Load data (adjust paths as needed)
\copy ecommerce.Regions(region_name) FROM 'data/cleaned/regions_cleaned.csv' DELIMITER ',' CSV HEADER;
\copy ecommerce.States(state_name, region_id) FROM 'data/cleaned/states_cleaned.csv' DELIMITER ',' CSV HEADER;
```

---

### 3. Data Pipeline Architecture

#### 3.1 Pipeline Flow

```
                    ┌──────────────────────┐
                    │    Raw CSV Data      │
                    │  (15,000 records)    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  generate_dataset.py │
                    └──────────┬───────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│                     clean_data.py                            │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────────┐  │
│  │Load Raw Data│→ │Handle Missing│→ │Remove Duplicates   │  │
│  └─────────────┘  └─────────────┘  └────────────────────┘  │
│                                          │                   │
│  ┌────────────────────┐  ┌──────────┐  │                   │
│  │Feature Engineering │← │Outlier   │←┘                   │
│  │                    │  │Detection │                     │
│  └────────────────────┘  └──────────┘                     │
│           │                                                │
│           ▼                                                │
│  ┌────────────────────┐  ┌────────────────────┐          │
│  │Standardize Dtypes  │→ │Quality Report Gen  │          │
│  └────────────────────┘  └────────────────────┘          │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────┐    ┌──────────────────────┐
│  Cleaned CSV Data    │    │  Validation Report   │
│  (data/cleaned/)     │    │  (reports/)          │
└──────────┬───────────┘    └──────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│                     analysis.py                              │
│                                                              │
│  ┌─────────────┐  ┌─────────────┐  ┌────────────────────┐  │
│  │KPI Calculation│→│Chart Gen   │→ │Insights Extraction  │  │
│  └─────────────┘  └─────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌──────────────────────┐    ┌──────────────────────┐
│  Power BI Dashboard  │    │  Excel Reports       │
│  (8 Pages)           │    │  (Pivot + Charts)    │
└──────────────────────┘    └──────────────────────┘
```

#### 3.2 Data Flow Details

**Stage 1: Data Ingestion**
- Source: CSV files with 15,000+ records
- Format: Comma-separated with header row
- Load: pandas.read_csv()

**Stage 2: Data Cleaning**
- Handle missing values: Median for numeric, Mode for categorical
- Remove duplicates: Based on Order ID and Customer ID
- Outlier detection: IQR method (1.5x multiplier)
- Feature engineering: 15+ new features created

**Stage 3: Data Validation**
- Schema validation: 30+ column checks
- Type validation: Numeric, categorical, datetime
- Domain validation: 8 categorical domain checks
- Referential integrity: Cross-table validation
- Business rules: 5 business logic checks

**Stage 4: Analysis & Visualization**
- KPI calculation: 15+ business metrics
- Chart generation: 9+ analytical visualizations
- Insight extraction: 8+ actionable business insights

**Stage 5: Reporting**
- Excel reports: 6 sheets with formatting
- CSV exports: 6 report files
- Statistical summary: Text report

---

### 4. Database Design

#### 4.1 Entity Relationship Diagram

```
┌──────────────┐    ┌────────────────┐    ┌──────────────┐
│   Regions    │    │    States      │    │    Cities    │
├──────────────┤    ├────────────────┤    ├──────────────┤
│PK region_id  │───>│PK state_id     │───>│PK city_id    │
│   region_name│    │FK region_id    │    │FK state_id   │
└──────────────┘    │   state_name   │    │   city_name  │
                    └────────────────┘    └──────────────┘
                           │                     │
                           │                     │
┌──────────────┐          │                     │
│  Categories  │          │                     │
├──────────────┤          │                     │
│PK category_id│          │                     │
│   category...│          │                     │
└──────┬───────┘          │                     │
       │                  │                     │
┌──────▼───────┐          │                     │
│ SubCategories│          │                     │
├──────────────┤          │                     │
│PK subcat_id  │          │                     │
│FK category_id│          │                     │
└──────┬───────┘          │                     │
       │                  │                     │
┌──────▼───────┐    ┌────┴─────────────────────┴──────┐
│   Products   │    │           Orders                 │
├──────────────┤    ├──────────────────────────────────┤
│PK product_id │    │PK order_id                       │
│FK subcat_id  │<───│FK customer_id                    │
│FK category_id│    │FK shipping_id                    │
│   product... │    │FK payment_id                     │
│   unit_price │    │FK city_id                        │
│   unit_cost  │    │FK state_id                       │
└──────────────┘    │FK region_id                      │
                    │   order_date                      │
┌──────────────┐    │   ship_date                       │
│   Shipping   │    └──────────┬────────────────────────┘
├──────────────┤               │
│PK shipping_id│               │
│   shipping   │    ┌──────────▼────────────────────────┐
│   mode       │    │        Order_Items                │
└──────────────┘    ├───────────────────────────────────┤
                    │PK order_item_id                   │
┌──────────────┐    │FK order_id                        │
│   Payments   │    │FK product_id                      │
├──────────────┤    │   quantity                         │
│PK payment_id │    │   discount                         │
│   payment    │    │   sales                            │
│   mode       │    │   profit                           │
└──────────────┘    │   shipping_cost                    │
                    │   return_status                    │
                    └──────────┬────────────────────────┘
                               │
                    ┌──────────▼────────────────────────┐
                    │           Returns                  │
                    ├───────────────────────────────────┤
                    │PK return_id                       │
                    │FK order_item_id                   │
                    │   return_date                      │
                    │   return_reason                    │
                    │   refund_amount                    │
                    └───────────────────────────────────┘
```

#### 4.2 Table Specifications

| **Table** | **Rows** | **Columns** | **Primary Key** | **Foreign Keys** |
|---|---|---|---|---|
| Regions | 4 | 3 | region_id | - |
| States | 20 | 4 | state_id | region_id |
| Cities | 100 | 4 | city_id | state_id |
| Categories | 3 | 4 | category_id | - |
| SubCategories | 26 | 5 | subcategory_id | category_id |
| Customers | 2,000 | 10 | customer_id | city_id, state_id, region_id |
| Products | 78 | 7 | product_id | subcategory_id, category_id |
| Shipping | 4 | 4 | shipping_id | - |
| Payments | 10 | 4 | payment_id | - |
| Orders | 15,000 | 14 | order_id | customer_id, shipping_id, payment_id, city_id, state_id, region_id |
| Order_Items | 15,000 | 10 | order_item_id | order_id, product_id |
| Returns | Variable | 6 | return_id | order_item_id |

#### 4.3 Index Strategy

```sql
-- Primary indexes (auto-created with PKs)
-- Secondary indexes for performance
CREATE INDEX idx_orders_order_date ON Orders(order_date);
CREATE INDEX idx_orders_customer_id ON Orders(customer_id);
CREATE INDEX idx_order_items_product_id ON Order_Items(product_id);
CREATE INDEX idx_order_items_return_status ON Order_Items(return_status);
CREATE INDEX idx_customers_segment ON Customers(segment);

-- Composite indexes for analytical queries
CREATE INDEX idx_orders_date_region ON Orders(order_date, region_id);
CREATE INDEX idx_order_items_sales_profit ON Order_Items(sales, profit);
```

#### 4.4 Views

```sql
-- 1. vw_order_summary: Comprehensive order view
-- 2. vw_product_performance: Product analytics
-- 3. vw_customer_ltv: Customer lifetime value
```

---

### 5. Python Module Specifications

#### 5.1 clean_data.py

| **Function** | **Parameters** | **Returns** | **Complexity** |
|---|---|---|---|
| `load_raw_data()` | data_dir | Dict[str, DataFrame] | O(n) |
| `handle_missing_values()` | df, df_name | DataFrame | O(n*m) |
| `remove_duplicates()` | df, df_name, subset | DataFrame | O(n log n) |
| `detect_outliers()` | df, columns, method | DataFrame | O(n) |
| `engineer_features()` | orders_df | DataFrame | O(n) |
| `run_cleaning_pipeline()` | input_dir, output_dir | Dict[str, DataFrame] | O(n*m) |

#### 5.2 validate_data.py

| **Method** | **Parameters** | **Returns** |
|---|---|---|
| `__init__()` | dataframes | None |
| `run_all_checks()` | - | ValidationReport |
| `_check_schema()` | df, name | List[Check] |
| `_check_data_types()` | df, name | List[Check] |
| `_check_numeric_ranges()` | df, name | List[Check] |
| `_check_categorical_domains()` | df, name | List[Check] |
| `_check_uniqueness()` | df, name | List[Check] |
| `_check_referential_integrity()` | df, name | List[Check] |
| `_check_business_rules()` | df, name | List[Check] |

#### 5.3 analysis.py

| **Function** | **Output** | **Libraries** |
|---|---|---|
| `calculate_kpis()` | Dict of KPIs | pandas |
| `plot_monthly_sales_trend()` | Chart file | matplotlib |
| `plot_sales_by_category()` | Chart file | matplotlib |
| `plot_top_products()` | Chart file | matplotlib |
| `plot_regional_performance()` | Chart file | matplotlib |
| `plot_customer_segment_analysis()` | Chart file | matplotlib |
| `plot_discount_impact()` | Chart file | matplotlib |
| `plot_profit_margin_analysis()` | Chart file | matplotlib |
| `plot_shipping_analysis()` | Chart file | matplotlib |
| `plot_monthly_growth_rate()` | Chart file | matplotlib |
| `extract_business_insights()` | DataFrame | pandas |

#### 5.4 export_reports.py

| **Function** | **Output** | **Format** |
|---|---|---|
| `generate_monthly_report()` | DataFrame | Tabular |
| `generate_quarterly_report()` | DataFrame | Tabular |
| `generate_yearly_report()` | DataFrame | Tabular |
| `generate_sales_report()` | DataFrame | Tabular |
| `generate_customer_report()` | DataFrame | Tabular |
| `generate_regional_report()` | DataFrame | Tabular |
| `generate_excel_reports()` | .xlsx file | Excel |
| `export_csv_reports()` | .csv files | CSV |

---

### 6. Code Standards

#### 6.1 Python (PEP8)

- **Indentation**: 4 spaces
- **Line length**: Maximum 100 characters
- **Naming**: snake_case for functions/variables, PascalCase for classes
- **Docstrings**: Google-style docstrings for all functions
- **Imports**: Standard library → Third-party → Local (alphabetical)
- **Type hints**: Used for all function parameters and returns

#### 6.2 SQL

- **Keywords**: UPPERCASE (SELECT, FROM, WHERE)
- **Identifiers**: lowercase with underscores (order_date, customer_id)
- **Indentation**: Aligned for readability
- **Comments**: Section headers with `--` for clarity
- **Aliases**: Clear, meaningful table aliases

#### 6.3 File Organization

- One primary class per file
- Functions grouped by functionality
- Constants at top of file
- Configuration in capitalized variables
- main() function at bottom for entry point

---

### 7. Performance Optimization

#### 7.1 Python Optimization

- Use vectorized pandas operations instead of loops
- Chunk large file operations when needed
- Use appropriate data types (category for low-cardinality strings)
- Profile with cProfile for bottlenecks

#### 7.2 SQL Optimization

- Use EXPLAIN ANALYZE for query tuning
- Create indexes on foreign keys and filtered columns
- Avoid SELECT *; specify required columns
- Use CTEs for complex queries to improve readability
- Partition large tables if needed

#### 7.3 Power BI Optimization

- Reduce column cardinality where possible
- Use aggregations instead of detailed data
- Limit visuals per page (max 6-8)
- Use bookmarks for state management

---

### 8. Troubleshooting Guide

| **Issue** | **Cause** | **Solution** |
|---|---|---|
| pandas ImportError | Missing dependency | `pip install -r requirements.txt` |
| CSV file not found | Wrong working directory | Run scripts from project root |
| UnicodeEncodeError | Terminal encoding | Set PYTHONIOENCODING=utf-8 |
| MemoryError | Large dataset | Increase available RAM |
| psycopg2 connection error | PostgreSQL not running | Start PostgreSQL service |
| Power BI file corruption | Version mismatch | Update Power BI Desktop |

---

### 9. API Reference

#### 9.1 Command Line Interface

```bash
# Generate synthetic dataset
python data/raw/generate_dataset.py

# Run cleaning pipeline
python python/clean_data.py

# Run validation
python python/validate_data.py

# Run analysis & generate charts
python python/analysis.py

# Export reports
python python/export_reports.py
```

#### 9.2 Function API Example

```python
# Import and use cleaning pipeline
from python.clean_data import run_cleaning_pipeline

# Run the complete pipeline
cleaned_data = run_cleaning_pipeline(
    input_dir='data/raw',
    output_dir='data/cleaned'
)

# Access cleaned DataFrames
orders_clean = cleaned_data['orders']
customers_clean = cleaned_data['customers']
```

---

### 10. Version History

| **Version** | **Date** | **Author** | **Changes** |
|---|---|---|---|
| 0.1 | 2024-01-01 | Analytics Team | Initial draft |
| 0.5 | 2024-01-15 | Analytics Team | Implementation |
| 1.0 | 2024-01-31 | Analytics Team | Final release |

---

### Document Approval

| **Role** | **Name** | **Signature** | **Date** |
|---|---|---|---|
| Lead Developer | [Name] | | |
| QA Engineer | [Name] | | |
| Project Manager | [Name] | | |
