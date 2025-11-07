import pandas as pd
from Quickshop_ETL.transform import transform_orders

def test_order_total_calculation():
    df = pd.DataFrame([
        {"product_id": 101, "qty": 2, "unit_price": 100.0},
        {"product_id": 102, "qty": 1, "unit_price": 250.0},
    ])
    transformed = transform_orders(df)
    assert transformed.loc[0, "order_total"] == 200.0
    assert transformed.loc[1, "order_total"] == 250.0
