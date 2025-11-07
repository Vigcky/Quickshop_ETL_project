import pytest
from Quickshop_ETL.transform import transform_orders

def test_order_total_calculation(sample_orders):
    transformed = transform_orders(sample_orders)
    assert "order_total" in transformed.columns
    assert transformed.loc[0, "order_total"] == 100.0
    assert transformed.loc[1, "order_total"] == 80.0

def test_invalid_data_handling(invalid_orders):
    transformed = transform_orders(invalid_orders)
    assert all(transformed["qty"] > 0)
    assert all(transformed["unit_price"] > 0)
