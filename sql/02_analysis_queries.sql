-- ============================================================
-- 02_analysis_queries.sql
-- Lamination Store Wholesale & Retail Supplier
-- Business Analysis Queries (KPIs, Trends, Joins)
-- Compatible with SQLite / MySQL / PostgreSQL (minor date-fn differences noted)
-- ============================================================

-- ------------------------------------------------------------
-- 1. OVERALL KPIs
-- ------------------------------------------------------------
SELECT
    COUNT(DISTINCT o.order_id)                         AS total_orders,
    ROUND(SUM(oi.line_total), 2)                        AS total_revenue,
    ROUND(SUM(oi.line_total) * 1.0 / COUNT(DISTINCT o.order_id), 2) AS avg_order_value,
    ROUND(SUM((oi.unit_price - p.unit_cost) * oi.quantity * (1 - oi.discount_pct)), 2) AS total_profit
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p     ON p.product_id = oi.product_id
WHERE o.order_status <> 'Cancelled';


-- ------------------------------------------------------------
-- 2. REVENUE BY CUSTOMER TYPE (Wholesale vs Retail)
-- ------------------------------------------------------------
SELECT
    c.customer_type,
    COUNT(DISTINCT o.order_id)        AS orders,
    ROUND(SUM(oi.line_total), 2)      AS revenue,
    ROUND(AVG(oi.line_total), 2)      AS avg_line_value
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN customers c     ON c.customer_id = o.customer_id
WHERE o.order_status <> 'Cancelled'
GROUP BY c.customer_type
ORDER BY revenue DESC;


-- ------------------------------------------------------------
-- 3. MONTHLY REVENUE TREND
-- ------------------------------------------------------------
SELECT
    strftime('%Y-%m', o.order_date)   AS order_month,   -- MySQL: DATE_FORMAT(o.order_date,'%Y-%m')
    ROUND(SUM(oi.line_total), 2)      AS revenue,
    COUNT(DISTINCT o.order_id)        AS orders
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
WHERE o.order_status <> 'Cancelled'
GROUP BY order_month
ORDER BY order_month;


-- ------------------------------------------------------------
-- 4. TOP 10 PRODUCTS BY REVENUE
-- ------------------------------------------------------------
SELECT
    p.product_name,
    p.category,
    SUM(oi.quantity)                  AS units_sold,
    ROUND(SUM(oi.line_total), 2)      AS revenue,
    ROUND(SUM((oi.unit_price - p.unit_cost) * oi.quantity * (1 - oi.discount_pct)), 2) AS profit
FROM order_items oi
JOIN orders o     ON o.order_id = oi.order_id
JOIN products p   ON p.product_id = oi.product_id
WHERE o.order_status <> 'Cancelled'
GROUP BY p.product_name, p.category
ORDER BY revenue DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 5. SALES PERFORMANCE BY EMPLOYEE / REGION
-- ------------------------------------------------------------
SELECT
    e.employee_name,
    e.region,
    COUNT(DISTINCT o.order_id)        AS orders_handled,
    ROUND(SUM(oi.line_total), 2)      AS revenue_generated
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN employees e    ON e.employee_id = o.employee_id
WHERE o.order_status <> 'Cancelled'
GROUP BY e.employee_name, e.region
ORDER BY revenue_generated DESC;


-- ------------------------------------------------------------
-- 6. TOP 10 CUSTOMERS BY LIFETIME VALUE
-- ------------------------------------------------------------
SELECT
    c.customer_name,
    c.customer_type,
    c.city,
    COUNT(DISTINCT o.order_id)        AS total_orders,
    ROUND(SUM(oi.line_total), 2)      AS lifetime_value
FROM customers c
JOIN orders o        ON o.customer_id = c.customer_id
JOIN order_items oi  ON oi.order_id = o.order_id
WHERE o.order_status <> 'Cancelled'
GROUP BY c.customer_name, c.customer_type, c.city
ORDER BY lifetime_value DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 7. PRODUCT CATEGORY PROFIT MARGIN %
-- ------------------------------------------------------------
SELECT
    p.category,
    ROUND(SUM(oi.line_total), 2) AS revenue,
    ROUND(SUM((oi.unit_price - p.unit_cost) * oi.quantity * (1 - oi.discount_pct)), 2) AS profit,
    ROUND(
        100.0 * SUM((oi.unit_price - p.unit_cost) * oi.quantity * (1 - oi.discount_pct))
        / SUM(oi.line_total), 1
    ) AS margin_pct
FROM order_items oi
JOIN orders o    ON o.order_id = oi.order_id
JOIN products p  ON p.product_id = oi.product_id
WHERE o.order_status <> 'Cancelled'
GROUP BY p.category
ORDER BY margin_pct DESC;


-- ------------------------------------------------------------
-- 8. ORDER STATUS BREAKDOWN (Delivered / Cancelled / Returned)
-- ------------------------------------------------------------
SELECT
    order_status,
    COUNT(*)                                    AS order_count,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 1) AS pct_of_total
FROM orders
GROUP BY order_status
ORDER BY order_count DESC;


-- ------------------------------------------------------------
-- 9. CITY-WISE REVENUE (Top 10)
-- ------------------------------------------------------------
SELECT
    c.city,
    c.state,
    COUNT(DISTINCT o.order_id)   AS orders,
    ROUND(SUM(oi.line_total), 2) AS revenue
FROM orders o
JOIN order_items oi ON oi.order_id = o.order_id
JOIN customers c     ON c.customer_id = o.customer_id
WHERE o.order_status <> 'Cancelled'
GROUP BY c.city, c.state
ORDER BY revenue DESC
LIMIT 10;


-- ------------------------------------------------------------
-- 10. AVERAGE PROCESSING (SHIPPING) TIME BY CUSTOMER TYPE
-- ------------------------------------------------------------
SELECT
    c.customer_type,
    ROUND(AVG(o.processing_days), 2) AS avg_processing_days
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.order_status <> 'Cancelled'
GROUP BY c.customer_type;


-- ------------------------------------------------------------
-- 11. MONTH-OVER-MONTH GROWTH % (window function)
-- ------------------------------------------------------------
WITH monthly_rev AS (
    SELECT
        strftime('%Y-%m', o.order_date) AS order_month,
        SUM(oi.line_total) AS revenue
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.order_status <> 'Cancelled'
    GROUP BY order_month
)
SELECT
    order_month,
    ROUND(revenue, 2) AS revenue,
    ROUND(
        100.0 * (revenue - LAG(revenue) OVER (ORDER BY order_month))
        / LAG(revenue) OVER (ORDER BY order_month), 1
    ) AS mom_growth_pct
FROM monthly_rev
ORDER BY order_month;


-- ------------------------------------------------------------
-- 12. CUSTOMER SEGMENTATION: REPEAT vs ONE-TIME BUYERS
-- ------------------------------------------------------------
SELECT
    CASE WHEN order_count = 1 THEN 'One-Time Buyer' ELSE 'Repeat Buyer' END AS segment,
    COUNT(*) AS customer_count,
    ROUND(AVG(total_spend), 2) AS avg_spend_per_customer
FROM (
    SELECT
        o.customer_id,
        COUNT(DISTINCT o.order_id) AS order_count,
        SUM(oi.line_total) AS total_spend
    FROM orders o
    JOIN order_items oi ON oi.order_id = o.order_id
    WHERE o.order_status <> 'Cancelled'
    GROUP BY o.customer_id
) sub
GROUP BY segment;
