/*
=============================================================================
E-Commerce Sales Analytics - Data Insertion Script
=============================================================================
Description: Populates the normalized PostgreSQL database from CSV data files
Author: Business Analytics Team
Version: 1.0
=============================================================================
*/

-- Set schema
SET search_path TO ecommerce;

-- ==========================================================================
-- 1. INSERT REGIONS
-- ==========================================================================
INSERT INTO Regions (region_name) VALUES
    ('West'),
    ('East'),
    ('Central'),
    ('South')
ON CONFLICT (region_name) DO NOTHING;

-- ==========================================================================
-- 2. INSERT CATEGORIES
-- ==========================================================================
INSERT INTO Categories (category_name, description) VALUES
    ('Furniture', 'Home and office furniture including chairs, tables, and sofas'),
    ('Office Supplies', 'General office supplies including binders, paper, and pens'),
    ('Technology', 'Electronic products including computers, phones, and accessories')
ON CONFLICT (category_name) DO NOTHING;

-- ==========================================================================
-- 3. INSERT SUB-CATEGORIES
-- ==========================================================================
INSERT INTO SubCategories (subcategory_name, category_id) VALUES
    -- Furniture sub-categories
    ('Bookcases', 1),
    ('Chairs', 1),
    ('Furnishings', 1),
    ('Tables', 1),
    ('Office Furniture', 1),
    ('Sofas', 1),
    -- Office Supplies sub-categories
    ('Binders', 2),
    ('Paper', 2),
    ('Labels', 2),
    ('Storage', 2),
    ('Art', 2),
    ('Envelopes', 2),
    ('Appliances', 2),
    ('Fasteners', 2),
    ('Scissors', 2),
    ('Pens', 2),
    -- Technology sub-categories
    ('Phones', 3),
    ('Computers', 3),
    ('Accessories', 3),
    ('Printers', 3),
    ('Monitors', 3),
    ('Tablets', 3),
    ('Cameras', 3),
    ('Software', 3),
    ('Networking', 3),
    ('Smart Home Devices', 3);

-- ==========================================================================
-- 4. INSERT SHIPPING MODES
-- ==========================================================================
INSERT INTO Shipping (shipping_mode, shipping_cost, estimated_days) VALUES
    ('Standard Class', 15.00, 7),
    ('Second Class', 10.00, 5),
    ('First Class', 25.00, 3),
    ('Same Day', 40.00, 1);

-- ==========================================================================
-- 5. INSERT PAYMENT MODES
-- ==========================================================================
INSERT INTO Payments (payment_mode, payment_status) VALUES
    ('Credit Card', 'Completed'),
    ('Debit Card', 'Completed'),
    ('PayPal', 'Completed'),
    ('Bank Transfer', 'Completed'),
    ('Cash', 'Completed'),
    ('UPI/Wallet', 'Completed'),
    ('Credit Card', 'Pending'),
    ('PayPal', 'Pending'),
    ('Credit Card', 'Failed'),
    ('Debit Card', 'Failed');

-- ==========================================================================
-- 6. BULK INSERT FROM CSV (using COPY command)
-- ==========================================================================
-- Note: Run these commands from psql or your SQL client
-- Adjust file paths according to your system

-- \copy ecommerce.States(state_name, region_id) FROM 'data/raw/states.csv' DELIMITER ',' CSV HEADER;
-- \copy ecommerce.Cities(city_name, state_id) FROM 'data/raw/cities.csv' DELIMITER ',' CSV HEADER;
-- \copy ecommerce.Customers(customer_id, customer_name, segment, email, registration_date, city_id, state_id, region_id) FROM 'data/raw/customers_cleaned.csv' DELIMITER ',' CSV HEADER;
-- \copy ecommerce.Products(product_name, subcategory_id, category_id, unit_price, unit_cost) FROM 'data/raw/products.csv' DELIMITER ',' CSV HEADER;
-- \copy ecommerce.Orders(order_id, order_date, ship_date, customer_id, shipping_id, payment_id, city_id, state_id, region_id) FROM 'data/raw/orders.csv' DELIMITER ',' CSV HEADER;
-- \copy ecommerce.Order_Items(order_id, product_id, quantity, discount, sales, profit, shipping_cost, return_status) FROM 'data/raw/order_items.csv' DELIMITER ',' CSV HEADER;

-- ==========================================================================
-- 7. ALTERNATIVE: INSERT USING PYTHON-SCRIPTED DATA
-- ==========================================================================
-- The Python scripts in the python/ directory handle the ETL process
-- Use python/clean_data.py to transform and load data into the database
-- See python/ directory for detailed ETL pipeline

-- ==========================================================================
-- DATA QUALITY CHECKS
-- ==========================================================================

-- Check record counts
SELECT 'Customers' AS table_name, COUNT(*) AS record_count FROM Customers
UNION ALL
SELECT 'Orders', COUNT(*) FROM Orders
UNION ALL
SELECT 'Order_Items', COUNT(*) FROM Order_Items
UNION ALL
SELECT 'Products', COUNT(*) FROM Products
UNION ALL
SELECT 'Categories', COUNT(*) FROM Categories
UNION ALL
SELECT 'Regions', COUNT(*) FROM Regions;

-- Verify foreign key integrity
SELECT 'Orders without valid customers' AS check_name, COUNT(*) AS issues
FROM Orders o
WHERE NOT EXISTS (SELECT 1 FROM Customers c WHERE c.customer_id = o.customer_id);

-- Check for negative sales or profit
SELECT 'Negative sales records' AS check_name, COUNT(*) AS count
FROM Order_Items
WHERE sales < 0;

SELECT 'Negative profit records' AS check_name, COUNT(*) AS count
FROM Order_Items
WHERE profit < 0;

-- ==========================================================================
-- END OF INSERT SCRIPT
-- ==========================================================================
