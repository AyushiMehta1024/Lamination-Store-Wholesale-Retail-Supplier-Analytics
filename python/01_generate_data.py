"""
01_generate_data.py
Generates a realistic synthetic dataset for a Lamination Store
(Wholesale + Retail Supplier) business.

Tables produced:
- customers.csv
- products.csv
- employees.csv
- orders.csv
- order_items.csv
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

# ----------------------------------------------------------------------
# 1. PRODUCTS  (Lamination film/pouch/roll products)
# ----------------------------------------------------------------------
product_lines = [
    ("Glossy Lamination Pouch", "Pouch", ["A4", "A3", "ID Card", "A5", "Letter"]),
    ("Matte Lamination Pouch", "Pouch", ["A4", "A3", "ID Card", "A5", "Letter"]),
    ("Thermal Lamination Roll", "Roll", ["12in", "25in", "27in", "36in"]),
    ("Cold Lamination Roll", "Roll", ["12in", "25in", "27in"]),
    ("Self-Adhesive Laminate Sheet", "Sheet", ["A4", "A3", "A2"]),
    ("Soft Touch Lamination Film", "Film", ["A4", "A3", "Roll-25in"]),
    ("Holographic Lamination Film", "Film", ["A4", "Roll-25in"]),
    ("PVC ID Card Laminate", "Pouch", ["ID Card", "Business Card"]),
    ("Anti-Scratch Lamination Sheet", "Sheet", ["A4", "A3"]),
    ("UV Protective Lamination Film", "Film", ["A4", "A3", "Roll-25in"]),
]

thickness_options = ["75 micron", "100 micron", "125 micron", "150 micron", "250 micron"]

rows = []
pid = 1000
for name, ptype, sizes in product_lines:
    for size in sizes:
        for thickness in np.random.choice(thickness_options, size=np.random.randint(2, 4), replace=False):
            base_cost = {
                "Pouch": np.random.uniform(2, 6),
                "Roll": np.random.uniform(15, 45),
                "Sheet": np.random.uniform(3, 8),
                "Film": np.random.uniform(4, 10),
            }[ptype]
            # thickness multiplier
            mult = 1 + (int(thickness.split()[0]) - 75) / 300
            unit_cost = round(base_cost * mult, 2)
            retail_price = round(unit_cost * np.random.uniform(1.6, 2.2), 2)
            wholesale_price = round(unit_cost * np.random.uniform(1.25, 1.5), 2)
            rows.append({
                "product_id": f"P{pid}",
                "product_name": f"{name} - {size}",
                "category": ptype,
                "size": size,
                "thickness": thickness,
                "unit_cost": unit_cost,
                "retail_price": retail_price,
                "wholesale_price": wholesale_price,
            })
            pid += 1

products = pd.DataFrame(rows).drop_duplicates(subset=["product_name"]).reset_index(drop=True)
print(f"Products: {len(products)} rows")

# ----------------------------------------------------------------------
# 2. CUSTOMERS (Wholesale & Retail)
# ----------------------------------------------------------------------
cities = [
    ("Mumbai", "Maharashtra"), ("Delhi", "Delhi"), ("Bengaluru", "Karnataka"),
    ("Ahmedabad", "Gujarat"), ("Pune", "Maharashtra"), ("Chennai", "Tamil Nadu"),
    ("Hyderabad", "Telangana"), ("Kolkata", "West Bengal"), ("Surat", "Gujarat"),
    ("Jaipur", "Rajasthan"), ("Lucknow", "Uttar Pradesh"), ("Indore", "Madhya Pradesh"),
    ("Nagpur", "Maharashtra"), ("Coimbatore", "Tamil Nadu"), ("Chandigarh", "Punjab"),
]

wholesale_name_pool = [
    "Print Hub", "Stationery World", "Office Mart", "Card Solutions", "PackPro Supplies",
    "Graphic Traders", "Print & Pack Co", "ID Card Distributors", "Stationery Junction",
    "Laminate Depot", "Business Supplies Co", "Print Express Wholesale", "MegaPrint Traders",
    "Office Essentials Wholesale", "PaperTech Distributors",
]
retail_name_pool = [
    "Quick Print Shop", "Campus Stationery", "City Photocopy Center", "Smart Print Studio",
    "Easy ID Cards", "Local Print Corner", "Student Stationery", "FastCard Print",
    "Neighborhood Printers", "Print N Bind", "Cyber Cafe & Print", "School Supplies Shop",
]

n_wholesale = 45
n_retail = 105
customers = []
cust_id = 1
for i in range(n_wholesale):
    city, state = cities[np.random.randint(len(cities))]
    customers.append({
        "customer_id": f"C{cust_id:04d}",
        "customer_name": f"{np.random.choice(wholesale_name_pool)} {city}",
        "customer_type": "Wholesale",
        "city": city,
        "state": state,
        "signup_date": (datetime(2022, 1, 1) + timedelta(days=int(np.random.uniform(0, 1200)))).date(),
        "credit_terms_days": int(np.random.choice([15, 30, 45, 60])),
    })
    cust_id += 1
for i in range(n_retail):
    city, state = cities[np.random.randint(len(cities))]
    customers.append({
        "customer_id": f"C{cust_id:04d}",
        "customer_name": f"{np.random.choice(retail_name_pool)} {city}",
        "customer_type": "Retail",
        "city": city,
        "state": state,
        "signup_date": (datetime(2022, 1, 1) + timedelta(days=int(np.random.uniform(0, 1200)))).date(),
        "credit_terms_days": 0,
    })
    cust_id += 1

customers = pd.DataFrame(customers)
print(f"Customers: {len(customers)} rows")

# ----------------------------------------------------------------------
# 3. EMPLOYEES (Sales Reps)
# ----------------------------------------------------------------------
emp_names = [
    "Rahul Sharma", "Priya Mehta", "Aman Verma", "Sneha Kapoor", "Vikram Rao",
    "Anita Desai", "Karan Malhotra", "Divya Nair", "Rohit Joshi", "Neha Gupta",
]
regions = ["North", "South", "East", "West", "Central"]
employees = pd.DataFrame([
    {
        "employee_id": f"E{100+i}",
        "employee_name": name,
        "region": regions[i % len(regions)],
        "hire_date": (datetime(2021, 1, 1) + timedelta(days=int(np.random.uniform(0, 900)))).date(),
    }
    for i, name in enumerate(emp_names)
])
print(f"Employees: {len(employees)} rows")

# ----------------------------------------------------------------------
# 4. ORDERS + ORDER ITEMS
# ----------------------------------------------------------------------
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

n_orders = 3200
order_rows = []
item_rows = []
order_item_id = 1

# seasonal boost for back-to-school (Apr-Jun, Sep) and Diwali period (Oct-Nov)
def seasonal_weight(d):
    m = d.month
    if m in (4, 5, 6, 9):
        return 1.4
    if m in (10, 11):
        return 1.3
    return 1.0

# build weighted day list
day_weights = []
for d in range(date_range_days):
    day = start_date + timedelta(days=d)
    day_weights.append(seasonal_weight(day))
day_weights = np.array(day_weights)
day_probs = day_weights / day_weights.sum()

order_dates = np.random.choice(np.arange(date_range_days), size=n_orders, p=day_probs)

statuses = ["Delivered", "Delivered", "Delivered", "Delivered", "Cancelled", "Returned"]
payment_methods = ["Bank Transfer", "Credit Terms", "UPI", "Cash", "Cheque"]

for i in range(n_orders):
    order_date = start_date + timedelta(days=int(order_dates[i]))
    cust = customers.iloc[np.random.randint(len(customers))]
    emp = employees[employees["region"] == regions[np.random.randint(len(regions))]].sample(1).iloc[0] \
        if np.random.rand() > 0.0 else employees.sample(1).iloc[0]

    is_wholesale = cust["customer_type"] == "Wholesale"
    n_line_items = np.random.randint(3, 9) if is_wholesale else np.random.randint(1, 4)

    order_id = f"O{10000+i}"
    status = np.random.choice(statuses, p=[0.78, 0.0, 0.0, 0.0, 0.07, 0.15] if False else None) \
        if False else np.random.choice(["Delivered", "Cancelled", "Returned"], p=[0.85, 0.06, 0.09])
    payment = np.random.choice(payment_methods, p=[0.35, 0.25, 0.2, 0.1, 0.1] if is_wholesale else [0.05, 0.0, 0.55, 0.35, 0.05])

    ship_delay = np.random.randint(1, 6)

    chosen_products = products.sample(n_line_items, replace=False)
    order_total = 0.0
    for _, prod in chosen_products.iterrows():
        qty = int(np.random.randint(20, 200)) if is_wholesale else int(np.random.randint(1, 25))
        unit_price = prod["wholesale_price"] if is_wholesale else prod["retail_price"]
        # small random discount for wholesale bulk
        discount_pct = round(np.random.uniform(0, 0.1), 3) if is_wholesale and qty > 100 else (
            round(np.random.uniform(0, 0.05), 3) if np.random.rand() < 0.2 else 0.0
        )
        line_total = round(qty * unit_price * (1 - discount_pct), 2)
        order_total += line_total
        item_rows.append({
            "order_item_id": f"OI{order_item_id:06d}",
            "order_id": order_id,
            "product_id": prod["product_id"],
            "quantity": qty,
            "unit_price": unit_price,
            "discount_pct": discount_pct,
            "line_total": line_total,
        })
        order_item_id += 1

    order_rows.append({
        "order_id": order_id,
        "customer_id": cust["customer_id"],
        "employee_id": emp["employee_id"],
        "order_date": order_date.date(),
        "ship_date": (order_date + timedelta(days=int(ship_delay))).date(),
        "order_status": status,
        "payment_method": payment,
        "order_total": round(order_total, 2) if status != "Cancelled" else 0.0,
    })

orders = pd.DataFrame(order_rows)
order_items = pd.DataFrame(item_rows)
print(f"Orders: {len(orders)} rows, Order Items: {len(order_items)} rows")

# ----------------------------------------------------------------------
# SAVE
# ----------------------------------------------------------------------
out = "/home/claude/lamination_project/data"
products.to_csv(f"{out}/products.csv", index=False)
customers.to_csv(f"{out}/customers.csv", index=False)
employees.to_csv(f"{out}/employees.csv", index=False)
orders.to_csv(f"{out}/orders.csv", index=False)
order_items.to_csv(f"{out}/order_items.csv", index=False)

print("\nAll CSVs saved to", out)
