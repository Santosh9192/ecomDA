/*
=============================================================================
E-Commerce Sales Analytics - PostgreSQL Database Schema
=============================================================================
Description: Normalized database schema for e-commerce sales analysis
Author: Business Analytics Team
Version: 1.0
Created: 2024-01-01
=============================================================================
*/

-- ==========================================================================
-- SCHEMA CREATION
-- ==========================================================================
-- Create schema for the project
CREATE SCHEMA IF NOT EXISTS ecommerce;
SET search_path TO ecommerce;

-- ==========================================================================
-- TABLE: Regions
-- ==========================================================================
CREATE TABLE IF NOT EXISTS Regions (
    region_id SERIAL PRIMARY KEY,
    region_name VARCHAR(50) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================================
-- TABLE: States
-- ==========================================================================
CREATE TABLE IF NOT EXISTS States (
    state_id SERIAL PRIMARY KEY,
    state_name VARCHAR(100) NOT NULL,
    region_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_states_region FOREIGN KEY (region_id) 
        REFERENCES Regions(region_id) ON DELETE CASCADE,
    CONSTRAINT uq_state_region UNIQUE (state_name, region_id)
);

-- ==========================================================================
-- TABLE: Cities
-- ==========================================================================
CREATE TABLE IF NOT EXISTS Cities (
    city_id SERIAL PRIMARY KEY,
    city_name VARCHAR(100) NOT NULL,
    state_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cities_state FOREIGN KEY (state_id) 
        REFERENCES States(state_id) ON DELETE CASCADE,
    CONSTRAINT uq_city_state UNIQUE (city_name, state_id)
);

-- ==========================================================================
-- TABLE: Categories
-- ==========================================================================
CREATE TABLE IF NOT EXISTS Categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================================
-- TABLE: SubCategories
-- ==========================================================================
CREATE TABLE IF NOT EXISTS SubCategories (
    subcategory_id SERIAL PRIMARY KEY,
    subcategory_name VARCHAR(100) NOT NULL,
    category_id INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_subcategories_category FOREIGN KEY (category_id) 
        REFERENCES Categories(category_id) ON DELETE CASCADE,
    CONSTRAINT uq_subcategory_category UNIQUE (subcategory_name, category_id)
);

-- ==========================================================================
-- TABLE: Customers
-- ==========================================================================
CREATE TABLE IF NOT EXISTS Customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(200) NOT NULL,
    segment VARCHAR(50) NOT NULL CHECK (segment IN ('Consumer', 'Corporate', 'Home Office')),
    email VARCHAR(200),
    registration_date DATE,
    city_id INTEGER,
    state_id INTEGER,
    region_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_customers_city FOREIGN KEY (city_id) 
        REFERENCES Cities(city_id) ON DELETE SET NULL,
    CONSTRAINT fk_customers_state FOREIGN KEY (state_id) 
        REFERENCES States(state_id) ON DELETE SET NULL,
    CONSTRAINT fk_customers_region FOREIGN KEY (region_id) 
        REFERENCES Regions(region_id) ON DELETE SET NULL
);

-- ==========================================================================
-- TABLE: Products
-- ==========================================================================
CREATE TABLE IF NOT EXISTS Products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(300) NOT NULL,
    subcategory_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL CHECK (unit_price > 0),
    unit_cost DECIMAL(10, 2) NOT NULL CHECK (unit_cost > 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_products_subcategory FOREIGN KEY (subcategory_id) 
        REFERENCES SubCategories(subcategory_id) ON DELETE CASCADE,
    CONSTRAINT fk_products_category FOREIGN KEY (category_id) 
        REFERENCES Categories(category_id) ON DELETE CASCADE,
    CONSTRAINT chk_price_gt_cost CHECK (unit_price >= unit_cost)
);

-- ==========================================================================
-- TABLE: Shipping
-- ==========================================================================
CREATE TABLE IF NOT EXISTS Shipping (
    shipping_id SERIAL PRIMARY KEY,
    shipping_mode VARCHAR(50) NOT NULL UNIQUE,
    shipping_cost DECIMAL(10, 2) DEFAULT 0,
    estimated_days INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================================
-- TABLE: Payments
-- ==========================================================================
CREATE TABLE IF NOT EXISTS Payments (
    payment_id SERIAL PRIMARY KEY,
    payment_mode VARCHAR(50) NOT NULL,
    payment_status VARCHAR(50) DEFAULT 'Completed' 
        CHECK (payment_status IN ('Pending', 'Completed', 'Failed', 'Refunded')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================================================
-- TABLE: Orders
-- ==========================================================================
CREATE TABLE IF NOT EXISTS Orders (
    order_id VARCHAR(20) PRIMARY KEY,
    order_date DATE NOT NULL,
    ship_date DATE,
    customer_id VARCHAR(20) NOT NULL,
    shipping_id INTEGER,
    payment_id INTEGER,
    city_id INTEGER,
    state_id INTEGER,
    region_id INTEGER,
    order_status VARCHAR(50) DEFAULT 'Completed'
        CHECK (order_status IN ('Pending', 'Processing', 'Completed', 'Cancelled')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_customer FOREIGN KEY (customer_id) 
        REFERENCES Customers(customer_id) ON DELETE CASCADE,
    CONSTRAINT fk_orders_shipping FOREIGN KEY (shipping_id) 
        REFERENCES Shipping(shipping_id) ON DELETE SET NULL,
    CONSTRAINT fk_orders_payment FOREIGN KEY (payment_id) 
        REFERENCES Payments(payment_id) ON DELETE SET NULL,
    CONSTRAINT fk_orders_city FOREIGN KEY (city_id) 
        REFERENCES Cities(city_id) ON DELETE SET NULL,
    CONSTRAINT fk_orders_state FOREIGN KEY (state_id) 
        REFERENCES States(state_id) ON DELETE SET NULL,
    CONSTRAINT fk_orders_region FOREIGN KEY (region_id) 
        REFERENCES Regions(region_id) ON DELETE SET NULL,
    CONSTRAINT chk_ship_date CHECK (ship_date >= order_date)
);

-- ==========================================================================
-- TABLE: Order_Items
-- ==========================================================================
CREATE TABLE IF NOT EXISTS Order_Items (
    order_item_id SERIAL PRIMARY KEY,
    order_id VARCHAR(20) NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    discount DECIMAL(4, 2) DEFAULT 0 CHECK (discount >= 0 AND discount <= 1),
    sales DECIMAL(12, 2) NOT NULL CHECK (sales >= 0),
    profit DECIMAL(12, 2) NOT NULL,
    shipping_cost DECIMAL(10, 2) DEFAULT 0,
    return_status VARCHAR(20) DEFAULT 'Not Returned'
        CHECK (return_status IN ('Returned', 'Not Returned')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_order_items_order FOREIGN KEY (order_id) 
        REFERENCES Orders(order_id) ON DELETE CASCADE,
    CONSTRAINT fk_order_items_product FOREIGN KEY (product_id) 
        REFERENCES Products(product_id) ON DELETE CASCADE
);

-- ==========================================================================
-- TABLE: Returns
-- ==========================================================================
CREATE TABLE IF NOT EXISTS Returns (
    return_id SERIAL PRIMARY KEY,
    order_item_id INTEGER NOT NULL,
    return_date DATE NOT NULL,
    return_reason VARCHAR(300),
    refund_amount DECIMAL(12, 2),
    return_status VARCHAR(50) DEFAULT 'Pending'
        CHECK (return_status IN ('Pending', 'Approved', 'Rejected', 'Processed')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_returns_order_item FOREIGN KEY (order_item_id) 
        REFERENCES Order_Items(order_item_id) ON DELETE CASCADE
);

-- ==========================================================================
-- INDEXES
-- ==========================================================================
-- Performance indexes for common query patterns
CREATE INDEX idx_orders_order_date ON Orders(order_date);
CREATE INDEX idx_orders_customer_id ON Orders(customer_id);
CREATE INDEX idx_orders_region_id ON Orders(region_id);
CREATE INDEX idx_orders_state_id ON Orders(state_id);
CREATE INDEX idx_order_items_order_id ON Order_Items(order_id);
CREATE INDEX idx_order_items_product_id ON Order_Items(product_id);
CREATE INDEX idx_order_items_return_status ON Order_Items(return_status);
CREATE INDEX idx_customers_segment ON Customers(segment);
CREATE INDEX idx_customers_region_id ON Customers(region_id);
CREATE INDEX idx_products_category_id ON Products(category_id);
CREATE INDEX idx_products_subcategory_id ON Products(subcategory_id);

-- Composite indexes for analytical queries
CREATE INDEX idx_orders_date_region ON Orders(order_date, region_id);
CREATE INDEX idx_order_items_sales_profit ON Order_Items(sales, profit);
CREATE INDEX idx_orders_customer_date ON Orders(customer_id, order_date);

-- ==========================================================================
-- CONSTRAINTS
-- ==========================================================================
-- Add check constraints for data integrity
-- Note: Profit calculation validation is handled at application level
-- Database CHECK constraints cannot reference other tables in PostgreSQL
ALTER TABLE Order_Items 
    ADD CONSTRAINT chk_sales_positive CHECK (sales >= 0);

ALTER TABLE Order_Items
    ADD CONSTRAINT chk_quantity_positive CHECK (quantity > 0);

ALTER TABLE Order_Items
    ADD CONSTRAINT chk_discount_range CHECK (discount >= 0 AND discount <= 1);

-- ==========================================================================
-- AUDIT TRIGGER FUNCTION
-- ==========================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply audit trigger to Customers table
CREATE TRIGGER update_customers_updated_at
    BEFORE UPDATE ON Customers
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ==========================================================================
-- VIEWS
-- ==========================================================================

-- View: Order Summary
CREATE OR REPLACE VIEW vw_order_summary AS
SELECT 
    o.order_id,
    o.order_date,
    o.ship_date,
    c.customer_name,
    c.segment,
    r.region_name,
    s.state_name,
    ci.city_name,
    COUNT(oi.order_item_id) AS item_count,
    SUM(oi.quantity) AS total_quantity,
    SUM(oi.sales) AS total_sales,
    SUM(oi.profit) AS total_profit,
    SUM(oi.shipping_cost) AS total_shipping_cost,
    AVG(oi.discount) AS avg_discount,
    sh.shipping_mode
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN Regions r ON o.region_id = r.region_id
JOIN States s ON o.state_id = s.state_id
JOIN Cities ci ON o.city_id = ci.city_id
JOIN Order_Items oi ON o.order_id = oi.order_id
JOIN Shipping sh ON o.shipping_id = sh.shipping_id
GROUP BY o.order_id, o.order_date, o.ship_date, c.customer_name, c.segment,
         r.region_name, s.state_name, ci.city_name, sh.shipping_mode;

-- View: Product Performance
CREATE OR REPLACE VIEW vw_product_performance AS
SELECT 
    p.product_id,
    p.product_name,
    cat.category_name,
    sc.subcategory_name,
    COUNT(DISTINCT oi.order_id) AS order_count,
    SUM(oi.quantity) AS total_quantity_sold,
    SUM(oi.sales) AS total_sales,
    SUM(oi.profit) AS total_profit,
    AVG(oi.discount) AS avg_discount,
    SUM(CASE WHEN oi.return_status = 'Returned' THEN 1 ELSE 0 END) AS return_count,
    ROUND(
        (SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2
    ) AS profit_margin_percent
FROM Products p
JOIN Categories cat ON p.category_id = cat.category_id
JOIN SubCategories sc ON p.subcategory_id = sc.subcategory_id
LEFT JOIN Order_Items oi ON p.product_id = oi.product_id
GROUP BY p.product_id, p.product_name, cat.category_name, sc.subcategory_name;

-- View: Customer Lifetime Value
CREATE OR REPLACE VIEW vw_customer_ltv AS
SELECT 
    c.customer_id,
    c.customer_name,
    c.segment,
    r.region_name,
    COUNT(DISTINCT o.order_id) AS total_orders,
    SUM(oi.sales) AS total_sales,
    SUM(oi.profit) AS total_profit,
    ROUND(SUM(oi.sales) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS avg_order_value,
    ROUND(
        (SUM(oi.sales) - SUM(oi.profit)) / NULLIF(SUM(oi.sales), 0) * 100, 2
    ) AS cost_ratio,
    MIN(o.order_date) AS first_order_date,
    MAX(o.order_date) AS last_order_date,
    ROUND(
        SUM(oi.profit) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2
    ) AS profit_per_order
FROM Customers c
LEFT JOIN Orders o ON c.customer_id = o.customer_id
LEFT JOIN Order_Items oi ON o.order_id = oi.order_id
LEFT JOIN Regions r ON c.region_id = r.region_id
GROUP BY c.customer_id, c.customer_name, c.segment, r.region_name;

-- ==========================================================================
-- STORED PROCEDURE: Get Sales by Date Range
-- ==========================================================================
CREATE OR REPLACE PROCEDURE sp_get_sales_by_date_range(
    p_start_date DATE,
    p_end_date DATE
)
LANGUAGE plpgsql
AS $$
BEGIN
    DROP TABLE IF EXISTS temp_sales_summary;
    CREATE TEMP TABLE temp_sales_summary AS
    SELECT 
        o.order_date,
        r.region_name,
        cat.category_name,
        COUNT(DISTINCT o.order_id) AS order_count,
        SUM(oi.quantity) AS items_sold,
        SUM(oi.sales) AS total_sales,
        SUM(oi.profit) AS total_profit,
        ROUND((SUM(oi.profit) / NULLIF(SUM(oi.sales), 0)) * 100, 2) AS profit_margin
    FROM Orders o
    JOIN Order_Items oi ON o.order_id = oi.order_id
    JOIN Regions r ON o.region_id = r.region_id
    JOIN Products p ON oi.product_id = p.product_id
    JOIN Categories cat ON p.category_id = cat.category_id
    WHERE o.order_date BETWEEN p_start_date AND p_end_date
    GROUP BY o.order_date, r.region_name, cat.category_name
    ORDER BY o.order_date;
END;
$$;

-- ==========================================================================
-- STORED PROCEDURE: Get Top Customers
-- ==========================================================================
CREATE OR REPLACE PROCEDURE sp_get_top_customers(
    p_limit INTEGER DEFAULT 10,
    p_start_date DATE DEFAULT '2021-01-01',
    p_end_date DATE DEFAULT '2024-12-31'
)
LANGUAGE plpgsql
AS $$
BEGIN
    DROP TABLE IF EXISTS temp_top_customers;
    CREATE TEMP TABLE temp_top_customers AS
    SELECT 
        c.customer_id,
        c.customer_name,
        c.segment,
        COUNT(DISTINCT o.order_id) AS order_count,
        SUM(oi.sales) AS total_sales,
        SUM(oi.profit) AS total_profit,
        ROUND(AVG(oi.sales), 2) AS avg_order_value
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    JOIN Order_Items oi ON o.order_id = oi.order_id
    WHERE o.order_date BETWEEN p_start_date AND p_end_date
    GROUP BY c.customer_id, c.customer_name, c.segment
    ORDER BY total_sales DESC
    LIMIT p_limit;
END;
$$;

-- ==========================================================================
-- TRIGGER: Prevent negative profit update
-- ==========================================================================
CREATE OR REPLACE FUNCTION check_order_item_profit()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.profit < 0 THEN
        INSERT INTO audit_log (table_name, record_id, action, old_value, new_value)
        VALUES ('Order_Items', NEW.order_item_id, 'NEGATIVE_PROFIT', 
                ROW(OLD.*)::TEXT, ROW(NEW.*)::TEXT);
    END IF;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- ==========================================================================
-- SCHEMA COMMENTS
-- ==========================================================================
COMMENT ON TABLE Regions IS 'Geographic regions for sales territories';
COMMENT ON TABLE States IS 'US states mapped to regions';
COMMENT ON TABLE Cities IS 'Cities within each state';
COMMENT ON TABLE Categories IS 'Product categories';
COMMENT ON TABLE SubCategories IS 'Product sub-categories under each category';
COMMENT ON TABLE Customers IS 'Customer master data';
COMMENT ON TABLE Products IS 'Product master data with pricing';
COMMENT ON TABLE Shipping IS 'Shipping mode reference data';
COMMENT ON TABLE Payments IS 'Payment method reference data';
COMMENT ON TABLE Orders IS 'Order header information';
COMMENT ON TABLE Order_Items IS 'Order line items with sales and profit details';
COMMENT ON TABLE Returns IS 'Product return transaction records';
COMMENT ON VIEW vw_order_summary IS 'Comprehensive order summary for reporting';
COMMENT ON VIEW vw_product_performance IS 'Product performance metrics for analysis';
COMMENT ON VIEW vw_customer_ltv IS 'Customer lifetime value analysis';

-- ==========================================================================
-- END OF SCHEMA
-- ==========================================================================
