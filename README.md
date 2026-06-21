# 🗂️ Lamination Store — Wholesale & Retail Supplier Analytics
### End-to-End Data Analyst Portfolio Project

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-F2C811?style=for-the-badge&logo=powerbi&logoColor=black)
![Excel](https://img.shields.io/badge/Excel-Analytics-217346?style=for-the-badge&logo=microsoftexcel&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=for-the-badge)

---

## 📌 Project Overview

A complete, end-to-end data analytics project built around a **Lamination Store business** that supplies lamination products (pouches, rolls, films, sheets) to both **wholesale distributors** and **retail customers** across India.

The project simulates a real-world analyst workflow — from raw messy data all the way to an interactive Power BI dashboard — using **Python, SQL, Excel, and Power BI**.

---

## 🎯 Business Problem

The lamination store management needed answers to:

- Which products and categories generate the most revenue and profit?
- How does wholesale performance compare to retail?
- Which sales reps and regions are top performers?
- What are the monthly and seasonal revenue trends?
- What is the order return rate and how can it be reduced?
- Who are our most valuable customers?

---

## 🧰 Tech Stack

| Tool | Purpose |
|---|---|
| **Python** (pandas, numpy, matplotlib) | Data generation, cleaning, EDA, chart exports |
| **SQL** (SQLite) | Schema design, 12 business analysis queries |
| **Excel** (openpyxl) | 6-sheet analytics workbook with embedded charts |
| **Power BI** | 4-page interactive dashboard with DAX measures |

---

## 📁 Project Structure

```
lamination_project/
│
├── data/
│   ├── customers_raw.csv          ← Intentionally messy (for cleaning demo)
│   ├── customers_clean.csv        ← After cleaning
│   ├── orders_raw.csv
│   ├── orders_clean.csv
│   ├── order_items_clean.csv
│   ├── products.csv
│   ├── employees.csv
│   ├── fact_sales.csv             ← Merged analysis-ready table (main input)
│   └── lamination_store.db        ← SQLite database
│
├── python/
│   ├── 01_generate_data.py        ← Synthetic dataset generation
│   ├── 02_inject_messiness.py     ← Adds real-world data quality issues
│   ├── 03_clean_and_eda.py        ← Data cleaning + EDA + 6 charts
│   ├── 04_load_to_sqlite.py       ← Loads data into SQLite DB
│   ├── 05_build_excel.py          ← Generates the full Excel workbook
│   └── charts/
│       ├── 01_monthly_revenue_trend.png
│       ├── 02_revenue_by_customer_type.png
│       ├── 03_top_products.png
│       ├── 04_revenue_by_region.png
│       ├── 05_order_status.png
│       └── 06_category_margin.png
│
├── sql/
│   ├── 01_schema.sql              ← Full normalized schema (5 tables)
│   └── 02_analysis_queries.sql    ← 12 business KPI queries
│
├── excel/
│   └── Lamination_Store_Analytics.xlsx   ← 6-sheet analytics workbook
│
└── powerbi/
    ├── DAX_Measures.dax           ← 20+ DAX measures ready to paste
    └── PowerBI_Setup_Guide.md     ← Step-by-step dashboard build guide
```

---

## 📊 Dataset Summary

| Table | Rows | Description |
|---|---|---|
| customers | 150 | 45 wholesale + 105 retail customers across 15 Indian cities |
| products | 32 | Pouches, rolls, films, sheets in various sizes & thickness |
| employees | 10 | Sales reps across 5 regions (North, South, East, West, Central) |
| orders | 3,200 | Orders from Jan 2024 – Dec 2025 with seasonal patterns |
| order_items | 9,703 | Line-level product quantities, prices, discounts |
| fact_sales | 9,703 | Fully merged analysis-ready table |

> **Data quality issues introduced for cleaning demo:** duplicate rows, missing values, negative quantities, impossible ship dates, inconsistent city name casing.

---

## 🐍 Python Workflow

### Step 1 — Data Generation (`01_generate_data.py`)
- Generates 5 realistic tables using `numpy` and `pandas`
- Includes seasonal demand patterns (April–May peak, October–November Diwali peak)
- Products span 4 categories × multiple sizes × multiple thickness options
- Wholesale customers get bulk pricing; retail gets individual pricing

### Step 2 — Inject Real-World Issues (`02_inject_messiness.py`)
Deliberately introduces:
- 4 duplicate customer rows
- Inconsistent city name casing (`MUMBAI`, ` Mumbai  `)
- 5 missing `credit_terms_days` values
- 6 negative `order_total` values
- 20 missing `employee_id` entries
- 8 negative quantity line items
- 10 duplicate order item rows
- 5 ship dates before order dates

### Step 3 — Clean & EDA (`03_clean_and_eda.py`)
**Cleaning actions:**
- Strip whitespace and normalize city names to Title Case
- Remove duplicate rows
- Impute missing credit terms with median
- Fix negative totals (abs value)
- Flag unknown employee IDs
- Correct impossible ship dates
- Fix negative quantities and recalculate line totals

**EDA outputs (6 charts):**

| Chart | Insight |
|---|---|
| Monthly Revenue Trend | Clear seasonal peaks in Apr–May and Oct–Nov |
| Revenue by Customer Type | Wholesale = 86.6% of total revenue |
| Top 10 Products | Cold Lamination Roll (12in) leads at Rs. 11.6L |
| Revenue by Region | East region leads (Rs. 22.4L) |
| Order Status Distribution | 84.3% delivered, 9.1% returned |
| Category Margin % | Film products have highest margin (31.3%) |

---

## 🗄️ SQL Analysis

The database uses a **normalized star schema**:

```
order_items ──< orders >── customers
     |                         
  products       employees ──< orders
```

### 12 Business Queries Included

| # | Query | Purpose |
|---|---|---|
| 1 | Overall KPIs | Total revenue, profit, avg order value |
| 2 | Revenue by customer type | Wholesale vs Retail split |
| 3 | Monthly revenue trend | Seasonal pattern analysis |
| 4 | Top 10 products | Best-performing products by revenue |
| 5 | Sales by employee | Rep-level performance ranking |
| 6 | Top 10 customers | Lifetime value ranking |
| 7 | Category profit margin % | Which category is most profitable |
| 8 | Order status breakdown | Delivery / cancellation / return rates |
| 9 | City-wise revenue | Geographic performance (top 10 cities) |
| 10 | Avg processing time | Shipping efficiency by customer type |
| 11 | Month-over-month growth | MoM % change using window functions |
| 12 | Customer segmentation | Repeat vs one-time buyer analysis |

---

## 📈 Excel Workbook

6 sheets in `Lamination_Store_Analytics.xlsx`:

| Sheet | Contents |
|---|---|
| Dashboard | KPI summary cards with live Excel formulas + key insights |
| RawData | Full 9,703-row fact table |
| Monthly Revenue | Pivot-style monthly summary + embedded line chart |
| Product Analysis | Revenue / Profit / Margin per product + bar chart |
| Customer Analysis | Top 20 customers colour-coded by type |
| Region & Employee | Sales rep performance + column chart |

---

## 📊 Power BI Dashboard

4 interactive pages built with **20+ DAX measures**:

### Page 1 — Executive Summary
- 4 KPI cards: Total Revenue, Total Profit, Total Orders, Return Rate %
- Monthly Revenue & Profit line chart (2024–2025)
- Wholesale vs Retail donut chart
- Year and Customer Type slicers (cross-filter all visuals)

### Page 2 — Product Performance
- Top 10 products horizontal bar chart
- Revenue by category treemap
- Full product matrix with Revenue / Profit / Margin %

### Page 3 — Customer & Region
- Top 15 customers bar chart
- City bubble map
- State-wise stacked revenue bar
- Customer type slicer

### Page 4 — Sales Team
- Revenue by sales rep column chart
- Avg processing days gauge (target: 3 days)
- Revenue by region donut
- Payment method breakdown

---

## 🔑 Key Business Results

| KPI | Value |
|---|---|
| Total Revenue | Rs. 1,01,21,718 |
| Total Profit | Rs. 29,59,184 |
| Profit Margin | 29.2% |
| Total Orders | 2,987 |
| Avg Order Value | Rs. 3,389 |
| Wholesale Revenue Share | 86.6% |
| Return Rate | 9.1% |
| Avg Processing Time | 3.0 days |
| Top City | Chandigarh (Rs. 15.2L) |
| Top Product | Cold Lamination Roll 12in (Rs. 11.6L) |
| Best Margin Category | Film (31.3%) |

---

## 🙋 About This Project

Built as a complete end-to-end data analyst portfolio project demonstrating:
- **Data Engineering** — synthetic data generation, pipeline design
- **Data Cleaning** — real-world quality issues and remediation
- **Exploratory Data Analysis** — trend discovery, outlier detection
- **SQL Analytics** — complex joins, window functions, CTEs
- **Data Visualization** — matplotlib charts, Excel dashboards, Power BI
- **Business Intelligence** — DAX measures, KPI design, interactive dashboards

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

⭐ **If you found this useful, give it a star!**
