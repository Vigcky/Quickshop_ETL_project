import pytest
import pandas as pd
from datetime import datetime

@pytest.fixture
def sample_orders():
    return pd.DataFrame({
        "order_id": ["1", "2"],
        "customer_id": ["cust_001", "cust_002"],
        "product_id": ["101", "102"],
        "qty": [2, 3],
        "unit_price": [100.0, 50.0],
        "order_date": [datetime(2025, 11, 1), datetime(2025, 11, 2)]
    })

@pytest.fixture
def invalid_orders():
    return pd.DataFrame({
        "order_id": ["3"],
        "customer_id": ["cust_003"],
        "product_id": ["103"],
        "qty": [2],
        "unit_price": [75.0],
        "order_date": [datetime(2025, 11, 3)]
    })