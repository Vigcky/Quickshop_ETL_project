from sqlalchemy import text
from .db import engine
import pandas as pd

def fetch_sales_summary():
    query = text("""
        SELECT order_date, SUM(order_total) AS total_sales
        FROM orders_transformed
        GROUP BY order_date
        ORDER BY order_date;
    """)
    with engine.connect() as conn:
        df = pd.read_sql(query, conn)
    return df
