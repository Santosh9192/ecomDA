# E-Commerce Sales Analytics
## Data Dictionary

---

### Version 1.0 | January 2024

---

## Table of Contents

1. [Orders Table](#1-orders-table)
2. [Customers Table](#2-customers-table)
3. [Products Reference](#3-products-reference)
4. [Categories Reference](#4-categories-reference)
5. [Regions & States Reference](#5-regions--states-reference)
6. [Derived/Engineered Fields](#6-derivedengineered-fields)

---

### 1. Orders Table

**File:** `data/raw/ecommerce_orders.csv` | **Records:** 15,000

| **Column Name** | **Data Type** | **Description** | **Sample Values** | **Constraints** |
|---|---|---|---|---|
| Order ID | VARCHAR(20) | Unique identifier for each order | ORD-000001, ORD-015000 | Primary Key, Unique |
| Order Date | DATE | Date when the order was placed | 2024-07-23, 2021-04-11 | NOT NULL, YYYY-MM-DD |
| Ship Date | DATE | Date when the order was shipped | 2024-07-28, 2021-04-16 | >= Order Date |
| Shipping Mode | VARCHAR(50) | Method of shipping selected | Standard Class, Same Day | Referential |
| Customer ID | VARCHAR(20) | Unique customer identifier | CUST-00001, CUST-01500 | Foreign Key → Customers |
| Customer Name | VARCHAR(200) | Full name of the customer | Joshua Parker, Susan Gray | NOT NULL |
| Segment | VARCHAR(50) | Customer market segment | Consumer, Corporate, Home Office | Categorical (3 values) |
| Country | VARCHAR(50) | Country of the customer | USA | Constant |
| Region | VARCHAR(50) | Geographic region | West, East, Central, South | Categorical (4 values) |
| State | VARCHAR(100) | US State | California, New York, Texas | Referential |
| City | VARCHAR(100) | City name | Los Angeles, New York City | Referential |
| Category | VARCHAR(100) | Product category | Furniture, Office Supplies, Technology | Categorical (3 values) |
| Sub-Category | VARCHAR(100) | Product sub-category | Chairs, Binders, Phones | Categorical (26 values) |
| Product Name | VARCHAR(300) | Name of the product purchased | Executive Office Chair, Laptop Pro | NOT NULL |
| Sales | DECIMAL(12,2) | Final sales amount after discount | 361.25, 1800.00 | >= 0, Continuous |
| Quantity | INTEGER | Number of units purchased | 1, 3, 5 | >= 1, Discrete (1-10) |
| Discount | DECIMAL(4,2) | Discount applied as decimal | 0.00, 0.10, 0.20 | 0 to 1 |
| Profit | DECIMAL(12,2) | Profit/Loss on the sale | 127.50, -50.00 | Continuous |
| Shipping Cost | DECIMAL(10,2) | Cost of shipping | 15.00, 35.50 | >= 0 |
| Payment Mode | VARCHAR(50) | Payment method used | Credit Card, PayPal, Cash | Categorical (6 values) |
| Return Status | VARCHAR(20) | Whether the item was returned | Returned, Not Returned | Categorical (2 values) |

---

### 2. Customers Table

**File:** `data/raw/customers.csv` | **Records:** 2,000

| **Column Name** | **Data Type** | **Description** | **Sample Values** | **Constraints** |
|---|---|---|---|---|
| Customer ID | VARCHAR(20) | Unique customer identifier | CUST-00001 | Primary Key, Unique |
| Customer Name | VARCHAR(200) | Customer full name | Samantha Anderson | NOT NULL |
| Segment | VARCHAR(50) | Customer market segment | Consumer, Corporate, Home Office | Categorical (3 values) |
| Region | VARCHAR(50) | Geographic region | West, East, Central, South | Referential |
| State | VARCHAR(100) | US State | Oregon, Arizona | Referential |
| City | VARCHAR(100) | City of residence | Salem, Portland | Referential |
| Email | VARCHAR(200) | Customer email address | samantha.anderson@email.com | Unique |
| Registration Date | DATE | Date of customer registration | 2023-05-12 | YYYY-MM-DD |

---

### 3. Products Reference

**Source:** Derived from `ecommerce_orders.csv`

| **Category** | **Sub-Category** | **Product Examples** | **Price Range** |
|---|---|---|---|
| Furniture | Bookcases | Classic Bookcase, Modern Bookshelf | $180 - $320 |
| Furniture | Chairs | Executive Office Chair, Ergonomic Chair | $120 - $450 |
| Furniture | Furnishings | Desk Lamp, Throw Pillow Set | $45 - $200 |
| Furniture | Tables | Coffee Table, Dining Table | $300 - $550 |
| Furniture | Office Furniture | Standing Desk, Filing Cabinet | $180 - $600 |
| Furniture | Sofas | 3-Seater Sofa, Loveseat | $600 - $1,200 |
| Office Supplies | Binders | A4 Ring Binder, Presentation Binder | $8 - $15 |
| Office Supplies | Paper | Ream A4 Paper, Glossy Photo Paper | $10 - $18 |
| Office Supplies | Labels | Address Labels, Shipping Labels | $12 - $25 |
| Office Supplies | Storage | Plastic Storage Bin, Storage Cabinet | $22 - $200 |
| Office Supplies | Art | Canvas Print, Wall Art Set | $40 - $90 |
| Office Supplies | Envelopes | #10 Envelopes, Padded Mailers | $15 - $22 |
| Office Supplies | Appliances | Coffee Maker, Mini Fridge | $80 - $150 |
| Office Supplies | Fasteners | Stapler, Paper Clips Pack | $3 - $25 |
| Office Supplies | Scissors | Office Scissors, Safety Scissors | $8 - $12 |
| Office Supplies | Pens | Ballpoint Pens, Fountain Pen | $12 - $35 |
| Technology | Phones | Smartphone, Office Phone | $85 - $699 |
| Technology | Computers | Laptop Pro, Desktop PC | $900 - $1,200 |
| Technology | Accessories | USB-C Hub, Wireless Mouse | $35 - $60 |
| Technology | Printers | Laser Printer, Inkjet Printer | $150 - $350 |
| Technology | Monitors | 24-inch Monitor, Ultrawide Monitor | $280 - $550 |
| Technology | Tablets | 10-inch Tablet, iPad Pro | $150 - $999 |
| Technology | Cameras | Webcam, DSLR Camera | $70 - $800 |
| Technology | Software | Office Suite, Antivirus | $60 - $300 |
| Technology | Networking | WiFi Router, Network Switch | $25 - $100 |
| Technology | Smart Home Devices | Smart Speaker, Smart Bulbs Pack | $50 - $200 |

---

### 4. Categories Reference

| **Category ID** | **Category Name** | **Sub-Categories** | **Product Count** |
|---|---|---|---|
| 1 | Furniture | 6 (Bookcases, Chairs, Furnishings, Tables, Office Furniture, Sofas) | 18 |
| 2 | Office Supplies | 10 (Binders, Paper, Labels, Storage, Art, Envelopes, Appliances, Fasteners, Scissors, Pens) | 30 |
| 3 | Technology | 10 (Phones, Computers, Accessories, Printers, Monitors, Tablets, Cameras, Software, Networking, Smart Home Devices) | 30 |

---

### 5. Regions & States Reference

| **Region** | **States** | **Sample Cities** |
|---|---|---|
| **West** | California, Washington, Oregon, Nevada, Arizona | Los Angeles, Seattle, Portland, Las Vegas, Phoenix |
| **East** | New York, Massachusetts, Pennsylvania, New Jersey, Virginia | New York City, Boston, Philadelphia, Newark, Virginia Beach |
| **Central** | Texas, Illinois, Ohio, Michigan, Indiana | Houston, Chicago, Columbus, Detroit, Indianapolis |
| **South** | Florida, Georgia, North Carolina, Tennessee, Alabama | Miami, Atlanta, Charlotte, Nashville, Birmingham |

---

### 6. Derived/Engineered Fields

**Generated by:** `python/clean_data.py`

| **Field Name** | **Data Type** | **Description** | **Formula/Logic** |
|---|---|---|---|
| Order Year | INTEGER | Year of the order | EXTRACT(YEAR FROM Order Date) |
| Order Month | INTEGER | Month of the order (1-12) | EXTRACT(MONTH FROM Order Date) |
| Order Quarter | INTEGER | Quarter of the order (1-4) | EXTRACT(QUARTER FROM Order Date) |
| Order Weekday | INTEGER | Day of week (0=Monday, 6=Sunday) | EXTRACT(DOW FROM Order Date) |
| Order Month Name | VARCHAR(20) | Month name | TO_CHAR(Order Date, 'Month') |
| Order Quarter Label | VARCHAR(10) | Quarter label | 'Q' + Quarter + '-' + Year |
| Is Weekend | BOOLEAN | Whether ordered on weekend | Order Weekday IN (5,6) |
| Season | VARCHAR(20) | Marketing season | Holiday/Spring/Summer/Fall |
| Delivery Days | INTEGER | Days taken for delivery | Ship Date - Order Date |
| Is Delayed | BOOLEAN | Delivery > 7 days | Delivery Days > 7 |
| Profit Margin % | DECIMAL(5,2) | Profit as percentage of sales | (Profit / Sales) * 100 |
| Discount Amount | DECIMAL(12,2) | Calculated discount value | Sales * Discount |
| Profit Category | VARCHAR(20) | Profitability category | Loss/Low/Medium/High Margin |
| Sales Bucket | VARCHAR(20) | Sales amount range | Under $50 to Over $1000 |
| Is Returned | BOOLEAN | Whether item was returned | Return Status = 'Returned' |

---

### Version History

| **Version** | **Date** | **Author** | **Changes** |
|---|---|---|---|
| 1.0 | 2024-01-31 | Analytics Team | Initial release |

---

*For the full Data Dictionary Excel file, see `documentation/Data_Dictionary.xlsx`*
