import pandas as pd
from Quickshop_ETL.load import write_to_db
from Quickshop_ETL.db import engine
from sqlalchemy import text

def test_write_to_db_replace_mode(tmp_path):
    df = pd.DataFrame([
        {"product_id": 101, "qty": 2, "unit_price": 50.0, "order_total": 100.0, "order_date": "2025-11-07"},
        {"product_id": 102, "qty": 1, "unit_price": 80.0, "order_total": 80.0, "order_date": "2025-11-07"}
    ])

    write_to_db(df, if_exists="replace")

    with engine.connect() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM orders_transformed"))
        count = result.scalar()
        assert count == 2
