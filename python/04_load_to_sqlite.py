"""
04_load_to_sqlite.py
Loads the CLEANED CSV files into a SQLite database using the schema
defined in sql/01_schema.sql, so the SQL analysis scripts can run.
"""

import sqlite3
import pandas as pd

base = "/home/claude/lamination_project/data"
sql_dir = "/home/claude/lamination_project/sql"
db_path = f"{base}/lamination_store.db"

conn = sqlite3.connect(db_path)
cur = conn.cursor()

with open(f"{sql_dir}/01_schema.sql") as f:
    schema_sql = f.read()
# SQLite doesn't support DECIMAL precision args or some CHECK syntax nuances but is lenient; still strip unsupported bits if needed
cur.executescript(schema_sql)

customers = pd.read_csv(f"{base}/customers_clean.csv")
employees = pd.read_csv(f"{base}/employees.csv")
products = pd.read_csv(f"{base}/products.csv")
orders = pd.read_csv(f"{base}/orders_clean.csv")
order_items = pd.read_csv(f"{base}/order_items_clean.csv")

customers.to_sql("customers", conn, if_exists="append", index=False)
employees.to_sql("employees", conn, if_exists="append", index=False)
products.to_sql("products", conn, if_exists="append", index=False)
orders.to_sql("orders", conn, if_exists="append", index=False)
order_items.to_sql("order_items", conn, if_exists="append", index=False)

conn.commit()

for t in ["customers", "employees", "products", "orders", "order_items"]:
    n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"{t}: {n} rows loaded")

conn.close()
print(f"\nSQLite DB created at {db_path}")
