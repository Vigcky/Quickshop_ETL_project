import pandas as pd
from datetime import datetime
from Quickshop_ETL.transform import transform_orders

def test_order_total_calculation():
    df = pd.DataFrame([
        {
            "order_id": "1",
            "customer_id": "cust_001",
            "product_id": "101",
            "qty": 2,
            "unit_price": 100.0,
            "order_date": datetime(2025, 11, 1)
        },
        {
            "order_id": "2",
            "customer_id": "cust_002",
            "product_id": "102",
            "qty": 1,
            "unit_price": 250.0,
            "order_date": datetime(2025, 11, 2)
        },
    ])
    transformed = transform_orders(df)
    assert transformed.loc[0, "order_total"] == 200.0
    assert transformed.loc[1, "order_total"] == 250.0