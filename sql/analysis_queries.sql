/*
=============================================================================
E-Commerce Sales Analytics - 50+ SQL Analysis Queries
=============================================================================
Description: Comprehensive business analysis queries for e-commerce data
Author: Business Analytics Team
Version: 2.0
=============================================================================
*/

-- Set schema
SET search_path TO ecommerce;

-- ==========================================================================
-- SECTION 1: SALES OVERVIEW (Queries 1-10)
-- ==========================================================================

-- Q1: Total Sales, Profit, and Order Count
SELECT 
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(
        (SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2
    ) AS profit_margin_percent,
    ROUND(SUM(oi.sales) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS avg_order_value
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id;

-- Q2: Monthly Revenue Trend
SELECT 
    TO_CHAR(o.order_date, 'YYYY-MM') AS month,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(
        (SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2
    ) AS profit_margin
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
ORDER BY month;

-- Q3: Yearly Revenue
SELECT 
    EXTRACT(YEAR FROM o.order_date) AS year,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(SUM(oi.sales) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS avg_order_value
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY EXTRACT(YEAR FROM o.order_date)
ORDER BY year;

-- Q4: Average Order Value (AOV) Over Time
SELECT 
    TO_CHAR(o.order_date, 'YYYY-MM') AS month,
    ROUND(SUM(oi.sales)::numeric / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS aov,
    ROUND(AVG(oi.sales)::numeric, 2) AS avg_line_item_value
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
ORDER BY month;

-- Q5: Daily Sales Summary
SELECT 
    o.order_date,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS profit,
    ROUND(SUM(oi.quantity)::numeric, 0) AS items_sold
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY o.order_date
ORDER BY o.order_date DESC;

-- Q6: Weekday vs Weekend Sales Analysis
SELECT 
    CASE 
        WHEN EXTRACT(DOW FROM o.order_date) IN (0, 6) THEN 'Weekend'
        ELSE 'Weekday'
    END AS day_type,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS profit,
    ROUND(AVG(oi.sales)::numeric, 2) AS avg_sale
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY day_type;

-- Q7: Sales by Day of Week
SELECT 
    EXTRACT(DOW FROM o.order_date) AS day_number,
    TO_CHAR(o.order_date, 'Day') AS day_name,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS profit
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY day_number, day_name
ORDER BY day_number;

-- Q8: Monthly Growth Rate (Using Window Functions)
WITH monthly_sales AS (
    SELECT 
        TO_CHAR(o.order_date, 'YYYY-MM') AS month,
        ROUND(SUM(oi.sales)::numeric, 2) AS total_sales
    FROM Orders o
    JOIN Order_Items oi ON o.order_id = oi.order_id
    GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
)
SELECT 
    month,
    total_sales,
    LAG(total_sales) OVER (ORDER BY month) AS prev_month_sales,
    ROUND(
        ((total_sales - LAG(total_sales) OVER (ORDER BY month)) / 
         NULLIF(LAG(total_sales) OVER (ORDER BY month), 0)) * 100, 2
    ) AS growth_percent
FROM monthly_sales
ORDER BY month;

-- Q9: Quarterly Sales and Growth
SELECT 
    EXTRACT(YEAR FROM o.order_date) AS year,
    EXTRACT(QUARTER FROM o.order_date) AS quarter,
    CONCAT('Q', EXTRACT(QUARTER FROM o.order_date), '-', EXTRACT(YEAR FROM o.order_date)) AS quarter_label,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS profit
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY year, quarter, quarter_label
ORDER BY year, quarter;

-- Q10: Running Total of Sales (Window Function)
SELECT 
    o.order_date,
    ROUND(SUM(oi.sales)::numeric, 2) AS daily_sales,
    ROUND(SUM(SUM(oi.sales)) OVER (ORDER BY o.order_date)::numeric, 2) AS running_total_sales
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY o.order_date
ORDER BY o.order_date;

-- ==========================================================================
-- SECTION 2: PRODUCT ANALYSIS (Queries 11-20)
-- ==========================================================================

-- Q11: Top 10 Best Selling Products by Revenue
SELECT 
    p.product_name,
    cat.category_name,
    sc.subcategory_name,
    COUNT(DISTINCT oi.order_id) AS order_count,
    SUM(oi.quantity) AS total_quantity,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit
FROM Products p
JOIN Categories cat ON p.category_id = cat.category_id
JOIN SubCategories sc ON p.subcategory_id = sc.subcategory_id
JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY p.product_name, cat.category_name, sc.subcategory_name
ORDER BY total_sales DESC
LIMIT 10;

-- Q12: Top 10 Most Profitable Products
SELECT 
    p.product_name,
    cat.category_name,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(
        (SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2
    ) AS profit_margin_percent
FROM Products p
JOIN Categories cat ON p.category_id = cat.category_id
JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY p.product_name, cat.category_name
ORDER BY total_profit DESC
LIMIT 10;

-- Q13: Products with Loss (Negative Profit)
SELECT 
    p.product_name,
    cat.category_name,
    COUNT(DISTINCT oi.order_id) AS affected_orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_loss,
    ROUND(AVG(oi.discount)::numeric, 2) AS avg_discount
FROM Products p
JOIN Categories cat ON p.category_id = cat.category_id
JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY p.product_name, cat.category_name
HAVING SUM(oi.profit) < 0
ORDER BY total_loss
LIMIT 10;

-- Q14: Sales by Product Category
SELECT 
    cat.category_name,
    COUNT(DISTINCT oi.order_id) AS orders,
    SUM(oi.quantity) AS quantity_sold,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(
        (SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2
    ) AS profit_margin,
    ROUND(SUM(oi.sales) / NULLIF(COUNT(DISTINCT oi.order_id), 0), 2) AS aov
FROM Categories cat
JOIN Products p ON cat.category_id = p.category_id
JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY cat.category_name
ORDER BY total_sales DESC;

-- Q15: Sales by Sub-Category
SELECT 
    cat.category_name,
    sc.subcategory_name,
    COUNT(DISTINCT oi.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(
        (SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2
    ) AS profit_margin
FROM Categories cat
JOIN SubCategories sc ON cat.category_id = sc.category_id
JOIN Products p ON sc.subcategory_id = p.subcategory_id
JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY cat.category_name, sc.subcategory_name
ORDER BY total_sales DESC;

-- Q16: Product Quantity Distribution
SELECT 
    quantity,
    COUNT(*) AS transaction_count,
    ROUND(SUM(sales)::numeric, 2) AS total_sales,
    ROUND(AVG(sales)::numeric, 2) AS avg_sale
FROM Order_Items
GROUP BY quantity
ORDER BY quantity;

-- Q17: Top Categories by Order Volume
SELECT 
    cat.category_name,
    COUNT(DISTINCT o.order_id) AS order_volume,
    ROUND(SUM(oi.quantity)::numeric, 0) AS units_sold,
    ROUND(
        COUNT(DISTINCT o.order_id) * 100.0 / SUM(COUNT(DISTINCT o.order_id)) OVER(), 2
    ) AS order_share_percent
FROM Categories cat
JOIN Products p ON cat.category_id = p.category_id
JOIN Order_Items oi ON p.product_id = oi.product_id
JOIN Orders o ON oi.order_id = o.order_id
GROUP BY cat.category_name
ORDER BY order_volume DESC;

-- Q18: Product Price Range Analysis
SELECT 
    CASE 
        WHEN p.unit_price < 50 THEN 'Under $50'
        WHEN p.unit_price BETWEEN 50 AND 100 THEN '$50-$100'
        WHEN p.unit_price BETWEEN 101 AND 200 THEN '$101-$200'
        WHEN p.unit_price BETWEEN 201 AND 500 THEN '$201-$500'
        WHEN p.unit_price BETWEEN 501 AND 1000 THEN '$501-$1000'
        ELSE 'Over $1000'
    END AS price_range,
    COUNT(DISTINCT p.product_id) AS product_count,
    SUM(oi.quantity) AS units_sold,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales
FROM Products p
JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY price_range
ORDER BY MIN(p.unit_price);

-- Q19: Products with Highest Return Rate
SELECT 
    p.product_name,
    cat.category_name,
    COUNT(*) AS total_sold,
    SUM(CASE WHEN oi.return_status = 'Returned' THEN 1 ELSE 0 END) AS returned,
    ROUND(
        SUM(CASE WHEN oi.return_status = 'Returned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS return_rate_percent,
    ROUND(SUM(oi.sales)::numeric, 2) AS revenue_at_risk
FROM Products p
JOIN Categories cat ON p.category_id = cat.category_id
JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY p.product_name, cat.category_name
HAVING COUNT(*) >= 10
ORDER BY return_rate_percent DESC
LIMIT 10;

-- Q20: Category-wise Monthly Trends
SELECT 
    cat.category_name,
    TO_CHAR(o.order_date, 'YYYY-MM') AS month,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales
FROM Categories cat
JOIN Products p ON cat.category_id = p.category_id
JOIN Order_Items oi ON p.product_id = oi.product_id
JOIN Orders o ON oi.order_id = o.order_id
GROUP BY cat.category_name, TO_CHAR(o.order_date, 'YYYY-MM')
ORDER BY cat.category_name, month;

-- ==========================================================================
-- SECTION 3: CUSTOMER ANALYSIS (Queries 21-30)
-- ==========================================================================

-- Q21: Top 10 Customers by Total Sales
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(SUM(oi.sales) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS avg_order_value
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY total_sales DESC
LIMIT 10;

-- Q22: Customer Lifetime Value (LTV)
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(oi.sales)::numeric, 2) AS ltv,
    ROUND(AVG(oi.sales)::numeric, 2) AS avg_order_value,
    ROUND(
        (MAX(o.order_date)::date - MIN(o.order_date)::date) / 30.0, 1
    ) AS customer_tenure_months,
    ROUND(
        SUM(oi.sales) / NULLIF(
            (EXTRACT(YEAR FROM AGE(MAX(o.order_date), MIN(o.order_date))) * 12 + 
             EXTRACT(MONTH FROM AGE(MAX(o.order_date), MIN(o.order_date)))), 0
        ), 2
    ) AS monthly_value
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY ltv DESC
LIMIT 20;

-- Q23: Repeat Customer Rate
WITH customer_orders AS (
    SELECT 
        c.customer_id,
        c.customer_name,
        COUNT(DISTINCT o.order_id) AS order_count
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.customer_name
)
SELECT 
    CASE 
        WHEN order_count = 1 THEN 'One-time'
        WHEN order_count BETWEEN 2 AND 3 THEN '2-3 Orders'
        WHEN order_count BETWEEN 4 AND 6 THEN '4-6 Orders'
        ELSE '7+ Orders'
    END AS customer_category,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS customer_share_percent
FROM customer_orders
GROUP BY customer_category
ORDER BY customer_category;

-- Q24: Customer Segmentation by Spending
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_spent,
    NTILE(4) OVER (ORDER BY SUM(oi.sales) DESC) AS spending_quartile,
    CASE 
        WHEN SUM(oi.sales) >= PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY SUM(oi.sales)) OVER() 
            THEN 'High Value'
        WHEN SUM(oi.sales) >= PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY SUM(oi.sales)) OVER() 
            THEN 'Medium Value'
        WHEN SUM(oi.sales) >= PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY SUM(oi.sales)) OVER() 
            THEN 'Low Value'
        ELSE 'Minimal'
    END AS customer_tier
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY total_spent DESC;

-- Q25: Customer Segment Analysis
SELECT 
    segment,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(AVG(oi.sales)::numeric, 2) AS avg_order_value,
    ROUND(SUM(oi.sales) / NULLIF(COUNT(DISTINCT c.customer_id), 0), 2) AS revenue_per_customer
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY segment
ORDER BY total_sales DESC;

-- Q26: New vs Returning Customer Revenue
WITH customer_first_order AS (
    SELECT 
        customer_id,
        MIN(order_date) AS first_order_date
    FROM Orders
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN o.order_date = cfo.first_order_date THEN 'New Customer'
        ELSE 'Returning Customer'
    END AS customer_type,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
JOIN customer_first_order cfo ON o.customer_id = cfo.customer_id
GROUP BY customer_type;

-- Q27: Top 10 Customers by Profit Contribution
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(
        SUM(oi.profit) * 100.0 / SUM(SUM(oi.profit)) OVER(), 2
    ) AS profit_share_percent
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name, c.segment
ORDER BY total_profit DESC
LIMIT 10;

-- Q28: Customer Acquisition Trend
SELECT 
    TO_CHAR(MIN(order_date), 'YYYY-MM') AS cohort_month,
    COUNT(DISTINCT customer_id) AS new_customers
FROM Orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY cohort_month;

-- Q29: Most Recent Order per Customer
WITH ranked_orders AS (
    SELECT 
        customer_id,
        order_id,
        order_date,
        ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date DESC) AS rn
    FROM Orders
)
SELECT 
    c.customer_id,
    c.customer_name,
    ro.order_id AS last_order_id,
    ro.order_date AS last_order_date,
    CASE 
        WHEN ro.order_date >= CURRENT_DATE - INTERVAL '30 days' THEN 'Active (30 days)'
        WHEN ro.order_date >= CURRENT_DATE - INTERVAL '90 days' THEN 'Active (90 days)'
        WHEN ro.order_date >= CURRENT_DATE - INTERVAL '180 days' THEN 'At Risk'
        ELSE 'Lost'
    END AS customer_status
FROM ranked_orders ro
JOIN Customers c ON ro.customer_id = c.customer_id
WHERE ro.rn = 1
ORDER BY ro.order_date DESC;

-- Q30: Customers with Highest Average Order Value
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.sales) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS avg_order_value
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY c.customer_id, c.customer_name, c.segment
HAVING COUNT(DISTINCT o.order_id) >= 3
ORDER BY avg_order_value DESC
LIMIT 10;

-- ==========================================================================
-- SECTION 4: REGIONAL ANALYSIS (Queries 31-40)
-- ==========================================================================

-- Q31: Sales by Region
SELECT 
    r.region_name,
    COUNT(DISTINCT o.order_id) AS orders,
    COUNT(DISTINCT c.customer_id) AS customers,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(
        (SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2
    ) AS profit_margin
FROM Regions r
JOIN Orders o ON r.region_id = o.region_id
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY r.region_name
ORDER BY total_sales DESC;

-- Q32: Most Profitable States
SELECT 
    s.state_name,
    r.region_name,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(
        (SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2
    ) AS profit_margin
FROM States s
JOIN Orders o ON s.state_id = o.state_id
JOIN Regions r ON s.region_id = r.region_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY s.state_name, r.region_name
ORDER BY total_profit DESC
LIMIT 10;

-- Q33: Least Profitable States
SELECT 
    s.state_name,
    r.region_name,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit
FROM States s
JOIN Orders o ON s.state_id = o.state_id
JOIN Regions r ON s.region_id = r.region_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY s.state_name, r.region_name
ORDER BY total_profit
LIMIT 10;

-- Q34: Top City by Sales
SELECT 
    ci.city_name,
    s.state_name,
    r.region_name,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit
FROM Cities ci
JOIN States s ON ci.state_id = s.state_id
JOIN Regions r ON s.region_id = r.region_id
JOIN Orders o ON ci.city_id = o.city_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY ci.city_name, s.state_name, r.region_name
ORDER BY total_sales DESC
LIMIT 15;

-- Q35: Region-wise Category Performance
SELECT 
    r.region_name,
    cat.category_name,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS profit
FROM Regions r
JOIN Orders o ON r.region_id = o.region_id
JOIN Order_Items oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
JOIN Categories cat ON p.category_id = cat.category_id
GROUP BY r.region_name, cat.category_name
ORDER BY r.region_name, sales DESC;

-- Q36: State-wise Average Order Value
SELECT 
    s.state_name,
    ROUND(AVG(oi.sales)::numeric, 2) AS avg_order_value,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    COUNT(DISTINCT o.order_id) AS order_count
FROM States s
JOIN Orders o ON s.state_id = o.state_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY s.state_name
ORDER BY avg_order_value DESC;

-- Q37: Regional Customer Density
SELECT 
    r.region_name,
    COUNT(DISTINCT c.customer_id) AS customer_count,
    COUNT(DISTINCT o.order_id) AS order_count,
    ROUND(
        COUNT(DISTINCT o.order_id)::numeric / NULLIF(COUNT(DISTINCT c.customer_id), 0), 2
    ) AS orders_per_customer
FROM Regions r
LEFT JOIN Customers c ON r.region_id = c.region_id
LEFT JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY r.region_name
ORDER BY customer_count DESC;

-- Q38: Regional Quarterly Performance
SELECT 
    r.region_name,
    EXTRACT(YEAR FROM o.order_date) AS year,
    EXTRACT(QUARTER FROM o.order_date) AS quarter,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS profit
FROM Regions r
JOIN Orders o ON r.region_id = o.region_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY r.region_name, year, quarter
ORDER BY r.region_name, year, quarter;

-- Q39: Regional Market Share
SELECT 
    r.region_name,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales,
    ROUND(
        SUM(oi.sales) * 100.0 / SUM(SUM(oi.sales)) OVER(), 2
    ) AS market_share_percent
FROM Regions r
JOIN Orders o ON r.region_id = o.region_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY r.region_name
ORDER BY sales DESC;

-- Q40: Regions with Highest Growth
WITH yearly_sales AS (
    SELECT 
        r.region_name,
        EXTRACT(YEAR FROM o.order_date) AS year,
        ROUND(SUM(oi.sales)::numeric, 2) AS sales
    FROM Regions r
    JOIN Orders o ON r.region_id = o.region_id
    JOIN Order_Items oi ON o.order_id = oi.order_id
    GROUP BY r.region_name, EXTRACT(YEAR FROM o.order_date)
)
SELECT 
    region_name,
    year,
    sales,
    LAG(sales) OVER (PARTITION BY region_name ORDER BY year) AS prev_year_sales,
    ROUND(
        ((sales - LAG(sales) OVER (PARTITION BY region_name ORDER BY year)) / 
         NULLIF(LAG(sales) OVER (PARTITION BY region_name ORDER BY year), 0)) * 100, 2
    ) AS yoy_growth_percent
FROM yearly_sales
ORDER BY region_name, year;

-- ==========================================================================
-- SECTION 5: DISCOUNT & PROFIT ANALYSIS (Queries 41-50)
-- ==========================================================================

-- Q41: Discount Impact on Sales and Profit
SELECT 
    CASE 
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount BETWEEN 0.01 AND 0.05 THEN '0-5%'
        WHEN discount BETWEEN 0.06 AND 0.10 THEN '6-10%'
        WHEN discount BETWEEN 0.11 AND 0.20 THEN '11-20%'
        WHEN discount BETWEEN 0.21 AND 0.30 THEN '21-30%'
        ELSE 'Over 30%'
    END AS discount_range,
    COUNT(*) AS transactions,
    ROUND(SUM(sales)::numeric, 2) AS total_sales,
    ROUND(SUM(profit)::numeric, 2) AS total_profit,
    ROUND(AVG(sales)::numeric, 2) AS avg_sale
FROM Order_Items
GROUP BY discount_range
ORDER BY MIN(discount);

-- Q42: Profit Margin Analysis by Category
SELECT 
    cat.category_name,
    ROUND(AVG(oi.profit)::numeric, 2) AS avg_profit_per_item,
    ROUND(
        (SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2
    ) AS overall_profit_margin,
    ROUND(
        STDDEV(oi.profit / NULLIF(oi.sales, 0))::numeric, 4
    ) AS profit_margin_volatility
FROM Categories cat
JOIN Products p ON cat.category_id = p.category_id
JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY cat.category_name
ORDER BY overall_profit_margin DESC;

-- Q43: Orders with Highest Discount Impact
SELECT 
    o.order_id,
    c.customer_name,
    o.order_date,
    ROUND(SUM(oi.sales)::numeric, 2) AS original_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS actual_profit,
    ROUND(AVG(oi.discount)::numeric, 2) AS avg_discount,
    ROUND(
        SUM(oi.quantity * p.unit_price * oi.discount)::numeric, 2
    ) AS total_discount_given
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Order_Items oi ON o.order_id = oi.order_id
JOIN Products p ON oi.product_id = p.product_id
GROUP BY o.order_id, c.customer_name, o.order_date
ORDER BY total_discount_given DESC
LIMIT 10;

-- Q44: Correlation Between Discount and Quantity
SELECT 
    CASE 
        WHEN discount = 0 THEN 'No Discount'
        WHEN discount <= 0.10 THEN 'Low (1-10%)'
        WHEN discount <= 0.20 THEN 'Medium (11-20%)'
        ELSE 'High (21%+)'
    END AS discount_level,
    COUNT(*) AS transactions,
    ROUND(AVG(quantity)::numeric, 2) AS avg_quantity,
    ROUND(SUM(quantity)::numeric, 0) AS total_quantity,
    ROUND(AVG(sales)::numeric, 2) AS avg_sales
FROM Order_Items
GROUP BY discount_level
ORDER BY MIN(discount);

-- Q45: Profit Analysis by Shipping Mode
SELECT 
    sh.shipping_mode,
    COUNT(DISTINCT oi.order_item_id) AS items_shipped,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(AVG(oi.shipping_cost)::numeric, 2) AS avg_shipping_cost,
    ROUND(
        (SUM(oi.profit) - SUM(oi.shipping_cost)) / NULLIF(SUM(oi.sales), 0) * 100, 2
    ) AS net_margin
FROM Shipping sh
JOIN Orders o ON sh.shipping_id = o.shipping_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY sh.shipping_mode
ORDER BY total_profit DESC;

-- Q46: Payment Mode Analysis
SELECT 
    oi.order_id,
    p.payment_mode,
    COUNT(*) AS items,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS profit
FROM Payments p
JOIN Orders o ON p.payment_id = o.payment_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY oi.order_id, p.payment_mode
ORDER BY sales DESC;

-- Q47: Overall Payment Method Preference
SELECT 
    p.payment_mode,
    COUNT(DISTINCT o.order_id) AS transaction_count,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.sales) * 100.0 / SUM(SUM(oi.sales)) OVER(), 2) AS sales_share_percent
FROM Payments p
JOIN Orders o ON p.payment_id = o.payment_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY p.payment_mode
ORDER BY total_sales DESC;

-- Q48: Return Analysis
SELECT 
    oi.return_status,
    COUNT(*) AS item_count,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales_affected,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit_impact,
    ROUND(AVG(oi.sales)::numeric, 2) AS avg_return_value
FROM Order_Items oi
GROUP BY oi.return_status;

-- Q49: Monthly Return Rate Trend
SELECT 
    TO_CHAR(o.order_date, 'YYYY-MM') AS month,
    COUNT(*) AS total_items,
    SUM(CASE WHEN oi.return_status = 'Returned' THEN 1 ELSE 0 END) AS returned_items,
    ROUND(
        SUM(CASE WHEN oi.return_status = 'Returned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2
    ) AS return_rate_percent
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
ORDER BY month;

-- Q50: Profit vs Sales Scatter Analysis (for identifying outliers)
SELECT 
    order_id,
    ROUND(sales::numeric, 2) AS sales,
    ROUND(profit::numeric, 2) AS profit,
    quantity,
    discount,
    CASE 
        WHEN profit < 0 THEN 'Loss Making'
        WHEN profit >= 0 AND profit < sales * 0.1 THEN 'Low Margin'
        WHEN profit >= sales * 0.1 AND profit < sales * 0.2 THEN 'Medium Margin'
        ELSE 'High Margin'
    END AS profitability_category
FROM Order_Items
ORDER BY sales DESC
LIMIT 50;

-- ==========================================================================
-- SECTION 6: ADVANCED ANALYTICS (Queries 51-60)
-- ==========================================================================

-- Q51: Year-over-Year Revenue Comparison
WITH yearly_revenue AS (
    SELECT 
        EXTRACT(YEAR FROM o.order_date) AS year,
        ROUND(SUM(oi.sales)::numeric, 2) AS revenue
    FROM Orders o
    JOIN Order_Items oi ON o.order_id = oi.order_id
    GROUP BY EXTRACT(YEAR FROM o.order_date)
)
SELECT 
    year,
    revenue,
    LAG(revenue) OVER (ORDER BY year) AS prev_year_revenue,
    ROUND(revenue - LAG(revenue) OVER (ORDER BY year), 2) AS absolute_change,
    ROUND(
        ((revenue - LAG(revenue) OVER (ORDER BY year)) / 
         NULLIF(LAG(revenue) OVER (ORDER BY year), 0)) * 100, 2
    ) AS yoy_growth_percent
FROM yearly_revenue
ORDER BY year;

-- Q52: Moving Average (3-Month) of Sales
WITH monthly_sales AS (
    SELECT 
        TO_CHAR(o.order_date, 'YYYY-MM') AS month,
        ROUND(SUM(oi.sales)::numeric, 2) AS sales
    FROM Orders o
    JOIN Order_Items oi ON o.order_id = oi.order_id
    GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
)
SELECT 
    month,
    sales,
    ROUND(
        AVG(sales) OVER (ORDER BY month ROWS BETWEEN 2 PRECEDING AND CURRENT ROW), 2
    ) AS moving_avg_3month
FROM monthly_sales
ORDER BY month;

-- Q53: Cumulative Sales by Month (Running Total)
SELECT 
    TO_CHAR(o.order_date, 'YYYY-MM') AS month,
    ROUND(SUM(oi.sales)::numeric, 2) AS monthly_sales,
    ROUND(
        SUM(SUM(oi.sales)) OVER (ORDER BY TO_CHAR(o.order_date, 'YYYY-MM'))::numeric, 2
    ) AS cumulative_sales
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY TO_CHAR(o.order_date, 'YYYY-MM')
ORDER BY month;

-- Q54: Best Performing Month Each Year
WITH ranked_months AS (
    SELECT 
        EXTRACT(YEAR FROM o.order_date) AS year,
        TO_CHAR(o.order_date, 'Month') AS month_name,
        ROUND(SUM(oi.sales)::numeric, 2) AS sales,
        ROW_NUMBER() OVER (
            PARTITION BY EXTRACT(YEAR FROM o.order_date) 
            ORDER BY SUM(oi.sales) DESC
        ) AS rank
    FROM Orders o
    JOIN Order_Items oi ON o.order_id = oi.order_id
    GROUP BY EXTRACT(YEAR FROM o.order_date), TO_CHAR(o.order_date, 'Month')
)
SELECT 
    year,
    month_name,
    sales
FROM ranked_months
WHERE rank = 1
ORDER BY year;

-- Q55: Customer Cohort Analysis
WITH customer_cohort AS (
    SELECT 
        customer_id,
        TO_CHAR(MIN(order_date), 'YYYY-MM') AS cohort_month
    FROM Orders
    GROUP BY customer_id
),
cohort_orders AS (
    SELECT 
        cc.cohort_month,
        EXTRACT(MONTH FROM AGE(o.order_date, MIN(cc.cohort_month || '-01')::DATE)) AS month_offset,
        COUNT(DISTINCT o.order_id) AS orders
    FROM customer_cohort cc
    JOIN Orders o ON cc.customer_id = o.customer_id
    GROUP BY cc.cohort_month, EXTRACT(MONTH FROM AGE(o.order_date, MIN(cc.cohort_month || '-01')::DATE))
)
SELECT 
    cohort_month,
    month_offset,
    orders
FROM cohort_orders
WHERE month_offset IS NOT NULL
ORDER BY cohort_month, month_offset;

-- Q56: Cross-Selling Analysis (Products frequently bought together)
SELECT 
    p1.product_name AS product_a,
    p2.product_name AS product_b,
    COUNT(*) AS times_bought_together
FROM Order_Items oi1
JOIN Order_Items oi2 ON oi1.order_id = oi2.order_id 
    AND oi1.product_id < oi2.product_id
JOIN Products p1 ON oi1.product_id = p1.product_id
JOIN Products p2 ON oi2.product_id = p2.product_id
GROUP BY p1.product_name, p2.product_name
ORDER BY times_bought_together DESC
LIMIT 20;

-- Q57: Shipping Delay Analysis
SELECT 
    sh.shipping_mode,
    ROUND(AVG((o.ship_date - o.order_date)::numeric), 1) AS avg_delivery_days,
    MAX(o.ship_date - o.order_date) AS max_delivery_days,
    MIN(o.ship_date - o.order_date) AS min_delivery_days,
    COUNT(*) AS total_orders
FROM Shipping sh
JOIN Orders o ON sh.shipping_id = o.shipping_id
GROUP BY sh.shipping_mode
ORDER BY avg_delivery_days;

-- Q58: Seasonal Sales Pattern
SELECT 
    EXTRACT(MONTH FROM o.order_date) AS month_number,
    TO_CHAR(o.order_date, 'Month') AS month_name,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales,
    ROUND(AVG(oi.sales)::numeric, 2) AS avg_sale
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY month_number, month_name
ORDER BY month_number;

-- Q59: Sales by Time of Day (if time data available)
-- Placeholder: Extend when time data is available
SELECT 
    'Full Day' AS time_period,
    COUNT(DISTINCT o.order_id) AS orders,
    ROUND(SUM(oi.sales)::numeric, 2) AS sales
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id;

-- Q60: Complete Business Health Dashboard Query
SELECT 
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    ROUND(SUM(oi.profit)::numeric, 2) AS total_profit,
    ROUND(
        (SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2
    ) AS profit_margin_percent,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    ROUND(SUM(oi.sales) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS avg_order_value,
    ROUND(
        COUNT(DISTINCT o.order_id)::numeric / NULLIF(COUNT(DISTINCT c.customer_id), 0), 2
    ) AS orders_per_customer,
    ROUND(
        (SELECT COUNT(*) FROM Order_Items WHERE return_status = 'Returned') * 100.0 / 
        NULLIF(COUNT(*), 0), 2
    ) AS return_rate_percent,
    ROUND(AVG(oi.discount)::numeric, 2) AS avg_discount
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
JOIN Customers c ON o.customer_id = c.customer_id;

-- ==========================================================================
-- SECTION 7: BUSINESS INSIGHTS & KPI QUERIES
-- ==========================================================================

-- KPI 1: Customer Acquisition Cost (Proxy)
SELECT 
    TO_CHAR(o.order_date, 'YYYY') AS year,
    COUNT(DISTINCT o.customer_id) AS new_customers,
    ROUND(SUM(oi.shipping_cost)::numeric, 2) AS total_shipping_cost,
    ROUND(
        SUM(oi.shipping_cost) / NULLIF(COUNT(DISTINCT o.customer_id), 0), 2
    ) AS estimated_acquisition_cost
FROM Orders o
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY TO_CHAR(o.order_date, 'YYYY')
ORDER BY year;

-- KPI 2: Customer Retention Rate by Year
WITH yearly_customers AS (
    SELECT 
        EXTRACT(YEAR FROM o.order_date) AS year,
        o.customer_id
    FROM Orders o
    GROUP BY EXTRACT(YEAR FROM o.order_date), o.customer_id
)
SELECT 
    a.year,
    COUNT(DISTINCT a.customer_id) AS active_customers,
    COUNT(DISTINCT b.customer_id) AS retained_customers,
    ROUND(
        COUNT(DISTINCT b.customer_id) * 100.0 / NULLIF(COUNT(DISTINCT a.customer_id), 0), 2
    ) AS retention_rate
FROM yearly_customers a
LEFT JOIN yearly_customers b 
    ON a.customer_id = b.customer_id 
    AND b.year = a.year + 1
GROUP BY a.year
ORDER BY a.year;

-- KPI 3: Repeat Purchase Rate
WITH customer_purchases AS (
    SELECT 
        customer_id,
        COUNT(DISTINCT order_id) AS purchase_count
    FROM Orders
    GROUP BY customer_id
)
SELECT 
    CASE 
        WHEN purchase_count = 1 THEN 'One-time Buyer'
        ELSE 'Repeat Buyer'
    END AS buyer_type,
    COUNT(*) AS customer_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER(), 2) AS percentage
FROM customer_purchases
GROUP BY buyer_type;

-- KPI 4: Top Product by Category
SELECT 
    cat.category_name,
    p.product_name,
    ROUND(SUM(oi.sales)::numeric, 2) AS total_sales,
    RANK() OVER (PARTITION BY cat.category_name ORDER BY SUM(oi.sales) DESC) AS rank_in_category
FROM Categories cat
JOIN Products p ON cat.category_id = p.category_id
JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY cat.category_name, p.product_name
ORDER BY cat.category_name, rank_in_category;

-- KPI 5: Revenue per Region with Target Comparison
SELECT 
    r.region_name,
    ROUND(SUM(oi.sales)::numeric, 2) AS actual_sales,
    ROUND(SUM(oi.sales) * 1.15::numeric, 2) AS sales_target_115pct,
    ROUND(
        CASE 
            WHEN SUM(oi.sales) >= SUM(oi.sales) * 1.15 THEN 100
            ELSE (SUM(oi.sales) / (SUM(oi.sales) * 1.15)) * 100
        END, 2
    ) AS target_achievement_pct
FROM Regions r
JOIN Orders o ON r.region_id = o.region_id
JOIN Order_Items oi ON o.order_id = oi.order_id
GROUP BY r.region_name
ORDER BY actual_sales DESC;

-- ==========================================================================
-- DATA QUALITY & AUDIT QUERIES
-- ==========================================================================

-- Data Quality: Check NULL values in critical fields
SELECT 'Order_Items - Sales' AS field, COUNT(*) AS null_count FROM Order_Items WHERE sales IS NULL
UNION ALL
SELECT 'Order_Items - Profit', COUNT(*) FROM Order_Items WHERE profit IS NULL
UNION ALL
SELECT 'Orders - Order_Date', COUNT(*) FROM Orders WHERE order_date IS NULL
UNION ALL
SELECT 'Orders - Customer_ID', COUNT(*) FROM Orders WHERE customer_id IS NULL
UNION ALL
SELECT 'Customers - Name', COUNT(*) FROM Customers WHERE customer_name IS NULL;

-- Schema Metadata
SELECT 
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'ecommerce'
ORDER BY table_name, ordinal_position;

-- ==========================================================================
-- END OF ANALYSIS QUERIES
-- ==========================================================================
