-- ============================================================
-- 01_schema.sql
-- Lamination Store Wholesale & Retail Supplier
-- Database Schema (works in MySQL / PostgreSQL / SQLite with minor tweaks)
-- ============================================================

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS employees;

CREATE TABLE customers (
    customer_id        VARCHAR(10) PRIMARY KEY,
    customer_name       VARCHAR(150) NOT NULL,
    customer_type        VARCHAR(20) CHECK (customer_type IN ('Wholesale','Retail')),
    city                VARCHAR(100),
    state               VARCHAR(100),
    signup_date         DATE,
    credit_terms_days   INTEGER DEFAULT 0
);

CREATE TABLE employees (
    employee_id     VARCHAR(10) PRIMARY KEY,
    employee_name   VARCHAR(150) NOT NULL,
    region          VARCHAR(50),
    hire_date       DATE
);

CREATE TABLE products (
    product_id       VARCHAR(10) PRIMARY KEY,
    product_name     VARCHAR(150) NOT NULL,
    category         VARCHAR(50),
    size             VARCHAR(50),
    thickness        VARCHAR(50),
    unit_cost        DECIMAL(10,2),
    retail_price     DECIMAL(10,2),
    wholesale_price  DECIMAL(10,2)
);

CREATE TABLE orders (
    order_id          VARCHAR(10) PRIMARY KEY,
    customer_id       VARCHAR(10) REFERENCES customers(customer_id),
    employee_id       VARCHAR(10) REFERENCES employees(employee_id),
    order_date        DATE NOT NULL,
    ship_date         DATE,
    order_status      VARCHAR(20) CHECK (order_status IN ('Delivered','Cancelled','Returned')),
    payment_method    VARCHAR(30),
    order_total       DECIMAL(12,2),
    processing_days   INTEGER
);

CREATE TABLE order_items (
    order_item_id   VARCHAR(12) PRIMARY KEY,
    order_id        VARCHAR(10) REFERENCES orders(order_id),
    product_id      VARCHAR(10) REFERENCES products(product_id),
    quantity        INTEGER NOT NULL,
    unit_price      DECIMAL(10,2),
    discount_pct    DECIMAL(5,3),
    line_total      DECIMAL(12,2)
);

CREATE INDEX idx_orders_customer ON orders(customer_id);
CREATE INDEX idx_orders_employee ON orders(employee_id);
CREATE INDEX idx_orders_date ON orders(order_date);
CREATE INDEX idx_items_order ON order_items(order_id);
CREATE INDEX idx_items_product ON order_items(product_id);
