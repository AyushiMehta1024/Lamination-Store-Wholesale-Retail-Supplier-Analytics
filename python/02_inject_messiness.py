"""
02_inject_messiness.py
Introduces realistic, controlled data quality issues into the raw CSVs
so the cleaning step in 03_clean_and_eda.py has real work to do.
This simulates what a real-world export from a POS/ERP system looks like.
"""

import numpy as np
import pandas as pd

np.random.seed(7)
base = "/home/claude/lamination_project/data"

customers = pd.read_csv(f"{base}/customers.csv")
orders = pd.read_csv(f"{base}/orders.csv")
order_items = pd.read_csv(f"{base}/order_items.csv")

# 1. Duplicate a few customer rows (common export issue)
dupes = customers.sample(4, random_state=1)
customers = pd.concat([customers, dupes], ignore_index=True)

# 2. Inconsistent casing / whitespace in city names
idx = customers.sample(15, random_state=2).index
customers.loc[idx, "city"] = customers.loc[idx, "city"].str.upper()
idx2 = customers.sample(10, random_state=3).index
customers.loc[idx2, "city"] = " " + customers.loc[idx2, "city"] + "  "

# 3. Missing values in credit_terms_days for some wholesale customers
idx3 = customers[customers.customer_type == "Wholesale"].sample(5, random_state=4).index
customers.loc[idx3, "credit_terms_days"] = np.nan

# 4. A few negative / nonsensical order_total caused by refund glitches
idx4 = orders.sample(6, random_state=5).index
orders.loc[idx4, "order_total"] = -orders.loc[idx4, "order_total"]

# 5. Some null employee_id (sales rep not logged)
idx5 = orders.sample(20, random_state=6).index
orders.loc[idx5, "employee_id"] = np.nan

# 6. Some order_items with 0 or negative quantity (data entry error)
idx6 = order_items.sample(8, random_state=7).index
order_items.loc[idx6, "quantity"] = -order_items.loc[idx6, "quantity"]

# 7. Duplicate order_items rows
dupe_items = order_items.sample(10, random_state=8)
order_items = pd.concat([order_items, dupe_items], ignore_index=True)

# 8. ship_date earlier than order_date for a handful of rows (logic error)
idx7 = orders.sample(5, random_state=9).index
orders.loc[idx7, "ship_date"] = orders.loc[idx7, "order_date"]

customers.to_csv(f"{base}/customers_raw.csv", index=False)
orders.to_csv(f"{base}/orders_raw.csv", index=False)
order_items.to_csv(f"{base}/order_items_raw.csv", index=False)

print("Messy raw files created: customers_raw.csv, orders_raw.csv, order_items_raw.csv")
