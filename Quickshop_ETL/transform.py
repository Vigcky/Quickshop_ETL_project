import pandas as pd
from .schema import OrderRecord


def apply_transformations(df: pd.DataFrame) -> pd.DataFrame:
    expected_cols = ["order_id", "product_id", "qty", "unit_price", "order_total", "order_date"]
    if df.empty:
        return pd.DataFrame(columns=expected_cols)

    transformed_rows = []
    for _, row in df.iterrows():
        try:
            rec = OrderRecord(**row.to_dict())
            rec.compute_total()
            transformed_rows.append(rec.dict())
        except Exception:
            continue

    if not transformed_rows:
        return pd.DataFrame(columns=expected_cols)

    result = pd.DataFrame(transformed_rows)
    if "order_total" not in result.columns:
        result["order_total"] = result["qty"] * result["unit_price"]

    for col in expected_cols:
        if col not in result.columns:
            result[col] = None

    return result


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Alias for backward compatibility."""
    return apply_transformations(df)
