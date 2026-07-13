<div align="center">

# 🛒 E-Commerce Sales Analytics Dashboard

### Business Intelligence | Data Analytics | SQL | Power BI | Python

<p align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791?style=for-the-badge&logo=postgresql)
![Power BI](https://img.shields.io/badge/Power%20BI-Desktop-F2C811?style=for-the-badge&logo=powerbi)
![SQL](https://img.shields.io/badge/SQL-Analytics-green?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=for-the-badge&logo=pandas)
![License](https://img.shields.io/badge/License-MIT-success?style=for-the-badge)

</p>

### 📊 Transforming Raw E-Commerce Data into Actionable Business Insights

A complete Business Intelligence portfolio project demonstrating SQL, PostgreSQL, Python, Power BI, Excel, Data Analysis, Dashboard Development, and Reporting skills.

---

⭐ If you like this project, don't forget to star the repository.

</div>

---

# 📌 Table of Contents

- Project Overview
- Business Problem
- Project Objectives
- Key Features
- Technology Stack
- System Architecture
- Dataset Information
- Folder Structure
- Database Design
- SQL Analytics
- Python ETL Pipeline
- Power BI Dashboard
- Business KPIs
- Business Questions Solved
- Reports
- Installation
- Usage
- Resume Description
- Future Enhancements
- License

---

# 📖 Project Overview

The **E-Commerce Sales Analytics Dashboard** is a complete Business Intelligence project developed to analyze sales transactions, customer purchasing behavior, product performance, and regional profitability.

The objective of this project is to convert raw business data into meaningful insights that help organizations make data-driven decisions.

The project demonstrates the complete analytics lifecycle including:

- Data Collection
- Data Cleaning
- Data Validation
- SQL Analysis
- KPI Calculation
- Dashboard Development
- Business Reporting
- Documentation

This project is suitable for showcasing Business Analyst, Data Analyst, and Business Intelligence skills.

---

# 💼 Business Problem

Modern e-commerce companies generate thousands of sales transactions every day.

Although large amounts of data are available, decision-makers often struggle to answer important business questions such as:

- Which products generate the highest revenue?
- Which customers contribute the most profit?
- Which region performs the best?
- Which categories are losing profit?
- How do discounts affect revenue?
- Which shipping method is most profitable?
- What are the monthly sales trends?
- Which customers are likely to become repeat buyers?

Without proper business analytics, management cannot make informed decisions.

This project solves that problem by creating a complete analytics solution capable of answering these questions using SQL, Python, PostgreSQL, Excel, and Power BI.

---

# 🎯 Project Objectives

The main objectives of this project are:

- Analyze sales performance using SQL.
- Build an interactive Power BI dashboard.
- Clean and validate raw sales data.
- Calculate important business KPIs.
- Identify profitable products and customers.
- Monitor regional sales performance.
- Perform customer segmentation.
- Generate automated business reports.
- Create professional project documentation.

---

# 🚀 Key Features

## 📊 Data Processing

- Data Cleaning
- Missing Value Handling
- Duplicate Removal
- Outlier Detection
- Feature Engineering
- Data Validation
- Data Transformation

---

## 🗄 SQL Analytics

- Complex SQL Queries
- Joins
- Window Functions
- Common Table Expressions (CTEs)
- Views
- Stored Procedures
- Index Optimization
- Business KPI Queries

---

## 📈 Dashboard Development

- Executive Dashboard
- Sales Dashboard
- Customer Dashboard
- Product Dashboard
- Regional Dashboard
- Profit Dashboard
- Interactive Filters
- KPI Cards

---

## 📑 Reporting

- Monthly Reports
- Quarterly Reports
- Annual Reports
- Customer Reports
- Product Reports
- Sales Reports
- Regional Reports

---

# 🛠 Technology Stack

| Category | Technologies |
|-----------|-------------|
| Programming Language | Python |
| Database | PostgreSQL |
| Query Language | SQL |
| Data Processing | Pandas, NumPy |
| Visualization | Power BI |
| Reporting | Excel |
| Charts | Matplotlib, Plotly |
| IDE | VS Code |
| Version Control | Git & GitHub |

---

# 🏗 System Architecture

```

Raw CSV Dataset

↓

Python Data Cleaning

↓

PostgreSQL Database

↓

SQL Business Analysis

↓

Power BI Dashboard

↓

Business Reports

↓

Management Decision Making

```

---

# 📂 Dataset Information

The project uses a realistic e-commerce sales dataset containing approximately **15,000 sales transactions**.

### Dataset Includes

- Orders
- Customers
- Products
- Categories
- Sub Categories
- Cities
- States
- Regions
- Sales
- Profit
- Quantity
- Discount
- Shipping Mode
- Payment Mode
- Customer Segment
- Order Date
- Ship Date

---

### Dataset Statistics

| Attribute | Value |
|------------|------|
| Total Orders | 15,000+ |
| Customers | 2,000+ |
| Products | 500+ |
| Categories | 3 |
| Sub Categories | 17 |
| Regions | 4 |
| States | 49 |
| Years Covered | 2021–2024 |

---

# 📁 Project Structure

```text
Ecommerce-Sales-Analytics/

│

├── data/
│ ├── raw/
│ ├── cleaned/
│ └── database/

│

├── sql/
│ ├── schema.sql
│ ├── insert.sql
│ └── analysis_queries.sql

│

├── python/
│ ├── clean_data.py
│ ├── validate_data.py
│ ├── analysis.py
│ ├── export_reports.py
│ ├── dashboard.py
│ └── analytics_utils.py

│

├── powerbi/
│ ├── Ecommerce_Dashboard.pbix
│ └── DAX_Measures.txt

│

├── reports/
│ ├── screenshots/
│ ├── excel/
│ └── html/

│

├── documentation/

│

├── README.md

├── requirements.txt

└── LICENSE
```

---

## 📸 Dashboard Preview

> Dashboard screenshots will be added after completing the Power BI dashboard.

- Executive Dashboard
- Sales Dashboard
- Customer Dashboard
- Product Dashboard
- Regional Dashboard

---
# 🗄️ Database Design

The project follows a normalized relational database model to maintain data integrity, improve query performance, and support analytical reporting.

## Database Tables

| Table | Description |
|--------|-------------|
| Customers | Customer information |
| Orders | Order details |
| Order_Items | Individual products within an order |
| Products | Product master data |
| Categories | Product categories |
| Returns | Returned orders |
| Payments | Payment information |
| Shipping | Shipping details |
| Regions | Regional information |
| States | State information |
| Cities | City information |

---

## Entity Relationship Diagram

> ER Diagram available in

```text
documentation/ER_Diagram.png
```

The database follows a **one-to-many** relationship model.

```
Customers
    │
    │
    ▼
Orders
    │
    ▼
Order Items
    │
    ▼
Products
    │
    ▼
Categories

Orders
   │
   ▼
Shipping

Orders
   │
   ▼
Payments

Orders
   │
   ▼
Returns
```

---

# 📊 Business KPIs

The dashboard calculates important business KPIs to monitor overall company performance.

| KPI | Description |
|------|-------------|
| Total Sales | Overall revenue generated |
| Total Profit | Overall business profit |
| Total Orders | Number of orders |
| Average Order Value | Revenue per order |
| Profit Margin | Profit percentage |
| Customer Lifetime Value | Revenue generated by each customer |
| Repeat Purchase Rate | Customer retention metric |
| Average Discount | Discount percentage |
| Return Rate | Percentage of returned products |
| Monthly Growth | Month-over-Month sales growth |

---

# 🔍 SQL Analytics

The project contains **50+ SQL queries** for solving real-world business problems.

## SQL Concepts Used

- SELECT
- WHERE
- GROUP BY
- ORDER BY
- HAVING
- CASE WHEN
- INNER JOIN
- LEFT JOIN
- RIGHT JOIN
- SELF JOIN
- Common Table Expressions (CTE)
- Window Functions
- Views
- Stored Procedures
- Indexing

---

## Business Analysis Queries

### Sales Analysis

- Monthly Sales
- Quarterly Sales
- Yearly Sales
- Revenue Growth
- Average Order Value
- Daily Sales Trend

---

### Customer Analysis

- Top Customers
- Repeat Customers
- Customer Lifetime Value
- Customer Segmentation
- Purchase Frequency

---

### Product Analysis

- Top Selling Products
- Low Performing Products
- Category Analysis
- Sub Category Analysis
- Product Profitability

---

### Regional Analysis

- Sales by Region
- Sales by State
- Sales by City
- Regional Profit
- Regional Growth

---

### Shipping Analysis

- Shipping Mode Performance
- Delivery Time Analysis
- Shipping Cost Analysis

---

### Discount Analysis

- Average Discount
- Discount Impact on Profit
- Discount by Category
- Discount by Region

---

## Sample SQL Query

```sql
SELECT
    category,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM orders
GROUP BY category
ORDER BY total_sales DESC;
```

---

## Advanced SQL Query

```sql
WITH MonthlySales AS
(
SELECT
DATE_TRUNC('month',order_date) AS month,
SUM(sales) total_sales
FROM orders
GROUP BY month
)

SELECT
month,
total_sales,
LAG(total_sales)
OVER(ORDER BY month) previous_month_sales
FROM MonthlySales;
```

---

# 🐍 Python ETL Pipeline

Python is used for complete data preprocessing before visualization.

## Pipeline Workflow

```
Raw Dataset

↓

Data Cleaning

↓

Validation

↓

Feature Engineering

↓

Data Transformation

↓

Analytics

↓

Report Generation

↓

Power BI
```

---

## Python Modules

| File | Purpose |
|------|----------|
| clean_data.py | Clean raw dataset |
| validate_data.py | Validate records |
| analysis.py | Perform business analysis |
| export_reports.py | Generate reports |
| analytics_utils.py | Shared utility functions |
| dashboard.py | Dashboard generation |

---

## Data Cleaning

The cleaning pipeline performs

- Missing value handling

- Duplicate removal

- Data type conversion

- Invalid record removal

- Date formatting

- String normalization

- Currency formatting

- Feature engineering

---

## Feature Engineering

The following derived columns are generated.

- Order Month

- Order Year

- Profit Margin

- Order Value

- Customer Age Group

- Delivery Days

- Profit Percentage

- Sales Category

- Discount Group

- Customer Type

---

# 📈 Data Validation

The validation engine performs more than 30 quality checks.

### Validation Checks

✔ Missing Values

✔ Duplicate Records

✔ Invalid Dates

✔ Invalid Emails

✔ Incorrect Phone Numbers

✔ Negative Sales

✔ Negative Profit

✔ Duplicate Customer IDs

✔ Null Categories

✔ Foreign Key Validation

✔ Order Consistency

✔ Payment Validation

---

# 📊 Power BI Dashboard

The Power BI dashboard is designed for management reporting.

## Dashboard Pages

### Executive Dashboard

Displays

- Total Sales

- Total Profit

- Total Orders

- Average Order Value

- Monthly Sales Trend

- KPI Cards

---

### Sales Dashboard

Displays

- Sales Trend

- Monthly Revenue

- Quarterly Revenue

- Category Analysis

- Sales Funnel

---

### Customer Dashboard

Displays

- Customer Segmentation

- Top Customers

- Customer Lifetime Value

- Repeat Customers

---

### Product Dashboard

Displays

- Top Products

- Bottom Products

- Category Performance

- Product Profitability

---

### Regional Dashboard

Displays

- Regional Sales

- State Sales

- City Sales

- Regional Profit

---

### Profit Dashboard

Displays

- Profit Trend

- Profit Margin

- Discount Impact

- Profit by Category

---

## Dashboard Features

✔ Interactive Filters

✔ Drill Through

✔ Bookmarks

✔ Tooltips

✔ Slicers

✔ Dynamic Titles

✔ KPI Cards

✔ Responsive Layout

✔ Dark Professional Theme

---

# 📊 Dashboard Visualizations

The dashboard contains

- KPI Cards

- Line Charts

- Clustered Bar Charts

- Pie Charts

- Donut Charts

- Treemaps

- Maps

- Scatter Charts

- Waterfall Charts

- Matrix Tables

- Heatmaps

- Area Charts

---

# 📷 Dashboard Screenshots

After completing the project, add screenshots in

```
reports/screenshots/
```

Recommended screenshots

```
Executive_Dashboard.png

Sales_Dashboard.png

Customer_Dashboard.png

Regional_Dashboard.png

Product_Dashboard.png

Profit_Dashboard.png

Database_Model.png

PowerBI_Model.png
```

---
# 💡 Business Insights

The analysis performed in this project helps answer several important business questions.

## Sales Insights

- Technology category generates the highest revenue.
- Office Supplies contribute consistent monthly sales.
- Furniture has lower profit margins due to higher discounts.
- Q4 records the highest sales every year.

---

## Customer Insights

- Corporate customers have the highest Average Order Value.
- Consumer segment contributes the largest number of orders.
- A small percentage of customers generate a significant share of total revenue.
- Repeat customers have a higher lifetime value.

---

## Product Insights

- Top-selling products contribute a major portion of total sales.
- Some products generate high sales but low profits because of discounts.
- Product profitability varies across categories.

---

## Regional Insights

- West region generates the highest revenue.
- East region has the highest profit margin.
- Central region requires improvement in profitability.
- Some states have high sales but comparatively lower profits.

---

## Shipping Insights

- Standard Class is the most frequently used shipping mode.
- Same Day shipping contributes higher profit per order.
- Delivery time directly impacts customer satisfaction.

---

## Discount Insights

- Discounts above 20% significantly reduce profitability.
- Moderate discounts improve sales without affecting profit considerably.
- Certain categories are highly sensitive to discount strategies.

---

# 📑 Reports Generated

The project automatically generates various reports to support business decision-making.

## Reports

- Monthly Sales Report
- Quarterly Sales Report
- Annual Sales Report
- Customer Analysis Report
- Product Performance Report
- Regional Performance Report
- Profit Analysis Report
- KPI Summary Report

Generated reports are available inside

```text
reports/
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/Ecommerce-Sales-Analytics.git

cd Ecommerce-Sales-Analytics
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### Linux / Mac

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Generate Dataset

```bash
python data/raw/generate_dataset.py
```

---

## Run Data Cleaning

```bash
python python/clean_data.py
```

---

## Validate Data

```bash
python python/validate_data.py
```

---

## Perform Analysis

```bash
python python/analysis.py
```

---

## Export Reports

```bash
python python/export_reports.py
```

---

## Launch Dashboard

```bash
python python/dashboard.py
```

---

## Run Flask Application

```bash
python python/web_app.py
```

---

# 💻 PostgreSQL Setup

Create Database

```sql
CREATE DATABASE ecommerce_sales;
```

Execute

```text
sql/schema.sql
```

Then execute

```text
sql/insert.sql
```

---

# 📊 Power BI Setup

Open

```text
powerbi/Ecommerce_Dashboard.pbix
```

Connect the dashboard to

```text
data/cleaned/orders_cleaned.csv
```

Refresh the data.

The dashboard will automatically update all KPIs and visualizations.

---

# ▶️ Project Workflow

```
Raw Dataset

↓

Python ETL Pipeline

↓

Data Cleaning

↓

PostgreSQL Database

↓

SQL Analytics

↓

Power BI Dashboard

↓

Business Reports

↓

Management Insights
```

---

# 📁 Folder Description

| Folder | Purpose |
|----------|----------|
| data | Raw and cleaned datasets |
| sql | Database scripts |
| python | ETL pipeline |
| powerbi | Dashboard |
| reports | Generated reports |
| documentation | Project documents |

---

# 💼 Resume Description

### E-Commerce Sales Analytics Dashboard

**Technologies Used**

SQL • PostgreSQL • Python • Pandas • Power BI • Excel

**Project Summary**

Developed a complete Business Intelligence solution for analyzing over **15,000+ e-commerce transactions**.

Designed a normalized PostgreSQL database and implemented **50+ SQL queries** using Joins, Window Functions, CTEs, Views, and Stored Procedures for business reporting.

Built an interactive Power BI dashboard featuring sales trends, customer insights, regional analysis, product performance, and executive KPIs.

Automated data cleaning, preprocessing, and reporting using Python and Pandas.

Generated actionable business insights supporting data-driven decision making.

---

# 🎓 Skills Demonstrated

- SQL

- PostgreSQL

- Power BI

- Excel

- Python

- Pandas

- Data Cleaning

- Data Analysis

- Business Intelligence

- Dashboard Development

- Reporting

- KPI Analysis

- Database Design

- Data Visualization

- Business Reporting

---

# 🚀 Future Enhancements

- Real-Time Dashboard

- Machine Learning Sales Forecasting

- Customer Churn Prediction

- Product Recommendation System

- Inventory Analytics

- Automated Email Reports

- Cloud Deployment

- Mobile Dashboard

---

# 🤝 Contributing

Contributions are welcome.

If you find any issue or would like to improve the project, feel free to fork the repository and submit a pull request.

---

# ⭐ Support

If you found this project helpful,

please consider giving it a ⭐ on GitHub.

It helps others discover the project.

---

# 📜 License

This project is licensed under the MIT License.

See the LICENSE file for more details.

---

# 👨‍💻 Developed By

## Santosh Babar

**Aspiring Business Analyst | Data Analyst | Software Developer**

### Skills

- SQL

- Power BI

- Python

- PostgreSQL

- Excel

- Data Analytics

- Business Intelligence

- Dashboard Development

- Machine Learning

- Git & GitHub

---

### Connect With Me

**LinkedIn**

www.linkedin.com/in/santosh-babar-839767407

**GitHub**

https://github.com/Santosh9192

**Email**

santoshbabar919200@gmail.com

---

<div align="center">

## ⭐ Thank You for Visiting ⭐

If you like this project,

please consider giving it a ⭐

Happy Learning 🚀

</div>
