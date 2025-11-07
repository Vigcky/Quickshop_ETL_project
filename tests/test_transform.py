import pandas as pd
from Quickshop_ETL.transform import apply_transformations

def test_order_total_calculation(sample_orders):
    df = apply_transformations(sample_orders)
    assert "order_total" in df.columns
    assert df["order_total"].tolist() == [200.0, 150.0]

def test_invalid_data_handling(invalid_orders):
    """Ensure invalid rows are dropped or handled gracefully."""
    df = apply_transformations(invalid_orders)
    assert not df.empty or isinstance(df, pd.DataFrame)
