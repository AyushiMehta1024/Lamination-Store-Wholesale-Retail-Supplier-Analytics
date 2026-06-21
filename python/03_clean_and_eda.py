"""
03_clean_and_eda.py
Data Cleaning + Exploratory Data Analysis (EDA)
for the Lamination Store Wholesale & Retail Supplier project.

Input  : customers_raw.csv, orders_raw.csv, order_items_raw.csv, products.csv, employees.csv
Output : cleaned CSVs (ready for SQL/Power BI/Excel) + EDA charts (PNG) + summary printed to console
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

base = "/home/claude/lamination_project/data"
charts = "/home/claude/lamination_project/python/charts"
import os
os.makedirs(charts, exist_ok=True)

pd.set_option("display.width", 120)

# ------------------------------------------------------------------
# LOAD
# ------------------------------------------------------------------
customers = pd.read_csv(f"{base}/customers_raw.csv")
orders = pd.read_csv(f"{base}/orders_raw.csv")
order_items = pd.read_csv(f"{base}/order_items_raw.csv")
products = pd.read_csv(f"{base}/products.csv")
employees = pd.read_csv(f"{base}/employees.csv")

print("="*70)
print("RAW DATA SHAPES")
print("="*70)
for name, df in [("customers", customers), ("orders", orders), ("order_items", order_items)]:
    print(f"{name}: {df.shape}")

# ------------------------------------------------------------------
# CLEAN: CUSTOMERS
# ------------------------------------------------------------------
print("\n" + "="*70)
print("CLEANING CUSTOMERS")
print("="*70)

before = len(customers)
customers["city"] = customers["city"].str.strip().str.title()
customers = customers.drop_duplicates(subset=["customer_id"]).reset_index(drop=True)
print(f"Removed {before - len(customers)} duplicate customer rows")

missing_credit = customers["credit_terms_days"].isna().sum()
customers.loc[
    (customers["customer_type"] == "Wholesale") & (customers["credit_terms_days"].isna()),
    "credit_terms_days"
] = customers.loc[customers["customer_type"] == "Wholesale", "credit_terms_days"].median()
customers["credit_terms_days"] = customers["credit_terms_days"].fillna(0).astype(int)
print(f"Imputed {missing_credit} missing credit_terms_days values (median for Wholesale)")

customers["signup_date"] = pd.to_datetime(customers["signup_date"])

# ------------------------------------------------------------------
# CLEAN: ORDERS
# ------------------------------------------------------------------
print("\n" + "="*70)
print("CLEANING ORDERS")
print("="*70)

neg_totals = (orders["order_total"] < 0).sum()
orders["order_total"] = orders["order_total"].abs()
print(f"Fixed {neg_totals} negative order_total values (took absolute value)")

missing_emp = orders["employee_id"].isna().sum()
orders["employee_id"] = orders["employee_id"].fillna("UNKNOWN")
print(f"Flagged {missing_emp} orders with missing employee_id as 'UNKNOWN'")

orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["ship_date"] = pd.to_datetime(orders["ship_date"])
bad_ship = (orders["ship_date"] <= orders["order_date"]).sum()
orders.loc[orders["ship_date"] <= orders["order_date"], "ship_date"] = \
    orders["order_date"] + pd.Timedelta(days=2)
print(f"Corrected {bad_ship} rows where ship_date <= order_date (set +2 days)")

orders["processing_days"] = (orders["ship_date"] - orders["order_date"]).dt.days

# ------------------------------------------------------------------
# CLEAN: ORDER ITEMS
# ------------------------------------------------------------------
print("\n" + "="*70)
print("CLEANING ORDER ITEMS")
print("="*70)

before = len(order_items)
order_items = order_items.drop_duplicates(subset=["order_item_id"]).reset_index(drop=True)
print(f"Removed {before - len(order_items)} duplicate order_item rows")

neg_qty = (order_items["quantity"] < 0).sum()
order_items["quantity"] = order_items["quantity"].abs()
order_items["line_total"] = (order_items["quantity"] * order_items["unit_price"] *
                              (1 - order_items["discount_pct"])).round(2)
print(f"Fixed {neg_qty} negative quantity rows and recalculated line_total")

# ------------------------------------------------------------------
# MERGE INTO ANALYSIS-READY TABLE
# ------------------------------------------------------------------
print("\n" + "="*70)
print("BUILDING ANALYSIS-READY MERGED DATASET")
print("="*70)

fact = (
    order_items
    .merge(orders, on="order_id", how="left")
    .merge(customers[["customer_id", "customer_name", "customer_type", "city", "state"]],
           on="customer_id", how="left")
    .merge(products[["product_id", "product_name", "category", "size", "thickness",
                      "unit_cost", "retail_price", "wholesale_price"]],
           on="product_id", how="left")
    .merge(employees[["employee_id", "employee_name", "region"]], on="employee_id", how="left")
)

fact = fact[fact["order_status"] != "Cancelled"].copy()
fact["profit"] = (fact["unit_price"] - fact["unit_cost"]) * fact["quantity"] * (1 - fact["discount_pct"])
fact["profit"] = fact["profit"].round(2)
fact["order_month"] = fact["order_date"].dt.to_period("M").astype(str)

print(f"Final analysis-ready fact table: {fact.shape}")

# ------------------------------------------------------------------
# SAVE CLEANED FILES
# ------------------------------------------------------------------
customers.to_csv(f"{base}/customers_clean.csv", index=False)
orders.to_csv(f"{base}/orders_clean.csv", index=False)
order_items.to_csv(f"{base}/order_items_clean.csv", index=False)
fact.to_csv(f"{base}/fact_sales.csv", index=False)
print(f"\nSaved cleaned files + fact_sales.csv (merged analysis table) to {base}")

# ------------------------------------------------------------------
# EDA
# ------------------------------------------------------------------
print("\n" + "="*70)
print("EXPLORATORY DATA ANALYSIS")
print("="*70)

total_revenue = fact["line_total"].sum()
total_profit = fact["profit"].sum()
total_orders = orders[orders["order_status"] != "Cancelled"]["order_id"].nunique()
avg_order_value = fact.groupby("order_id")["line_total"].sum().mean()

print(f"Total Revenue: Rs. {total_revenue:,.0f}")
print(f"Total Profit: Rs. {total_profit:,.0f}")
print(f"Total Valid Orders: {total_orders:,}")
print(f"Avg Order Value: Rs. {avg_order_value:,.2f}")
print(f"Profit Margin: {100*total_profit/total_revenue:.1f}%")

# Revenue by customer type
rev_by_type = fact.groupby("customer_type")["line_total"].sum().sort_values(ascending=False)
print("\nRevenue by Customer Type:\n", rev_by_type)

# Top products
top_products = fact.groupby("product_name")["line_total"].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Products by Revenue:\n", top_products)

# Monthly trend
monthly = fact.groupby("order_month")["line_total"].sum()

# Region performance
region_perf = fact.groupby("region")["line_total"].sum().sort_values(ascending=False)

# ------------------------------------------------------------------
# CHARTS
# ------------------------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")

# 1. Monthly Revenue Trend
fig, ax = plt.subplots(figsize=(10, 5))
monthly.plot(kind="line", marker="o", ax=ax, color="#2E5984")
ax.set_title("Monthly Revenue Trend", fontsize=14, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (Rs. )")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(f"{charts}/01_monthly_revenue_trend.png", dpi=150)
plt.close()

# 2. Revenue by Customer Type
fig, ax = plt.subplots(figsize=(6, 5))
rev_by_type.plot(kind="bar", ax=ax, color=["#2E5984", "#E8964D"])
ax.set_title("Revenue: Wholesale vs Retail", fontsize=14, fontweight="bold")
ax.set_ylabel("Revenue (Rs. )")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{charts}/02_revenue_by_customer_type.png", dpi=150)
plt.close()

# 3. Top 10 Products
fig, ax = plt.subplots(figsize=(9, 6))
top_products.sort_values().plot(kind="barh", ax=ax, color="#3E7CB1")
ax.set_title("Top 10 Products by Revenue", fontsize=14, fontweight="bold")
ax.set_xlabel("Revenue (Rs. )")
plt.tight_layout()
plt.savefig(f"{charts}/03_top_products.png", dpi=150)
plt.close()

# 4. Revenue by Region
fig, ax = plt.subplots(figsize=(7, 5))
region_perf.plot(kind="bar", ax=ax, color="#5B8C5A")
ax.set_title("Revenue by Sales Region", fontsize=14, fontweight="bold")
ax.set_ylabel("Revenue (Rs. )")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{charts}/04_revenue_by_region.png", dpi=150)
plt.close()

# 5. Order Status Distribution
status_counts = orders["order_status"].value_counts()
fig, ax = plt.subplots(figsize=(6, 6))
ax.pie(status_counts, labels=status_counts.index, autopct="%1.1f%%",
       colors=["#5B8C5A", "#E8964D", "#C0504D"], startangle=90)
ax.set_title("Order Status Distribution", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.savefig(f"{charts}/05_order_status.png", dpi=150)
plt.close()

# 6. Category-wise profit margin
cat_margin = fact.groupby("category").agg(revenue=("line_total","sum"), profit=("profit","sum"))
cat_margin["margin_pct"] = 100*cat_margin["profit"]/cat_margin["revenue"]
fig, ax = plt.subplots(figsize=(7,5))
cat_margin["margin_pct"].sort_values().plot(kind="barh", ax=ax, color="#8064A2")
ax.set_title("Profit Margin % by Product Category", fontsize=14, fontweight="bold")
ax.set_xlabel("Margin %")
plt.tight_layout()
plt.savefig(f"{charts}/06_category_margin.png", dpi=150)
plt.close()

print(f"\n6 EDA charts saved to {charts}")
print("\nDONE.")
