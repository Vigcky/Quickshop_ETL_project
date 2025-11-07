import pandas as pd
from .schema import OrderRecord
import logging


def apply_transformations(df: pd.DataFrame) -> pd.DataFrame:
    """Apply validation and compute order_total for each record."""
    expected_cols = ["order_id", "product_id", "qty", "unit_price", "order_total", "order_date"]

    if df.empty:
        logging.warning("⚠️ Input DataFrame is empty — nothing to transform.")
        return pd.DataFrame(columns=expected_cols)

    transformed_rows = []

    for _, row in df.iterrows():
        try:
            record = OrderRecord(**row.to_dict())
            record_dict = record.model_dump() 
            record_dict["order_total"] = record_dict["qty"] * record_dict["unit_price"]
            transformed_rows.append(record_dict)
        except Exception as e:
            logging.warning(f"⚠️ Skipping invalid row: {e}")

    if not transformed_rows:
        logging.warning("⚠️ No valid rows after transformation!")
        return pd.DataFrame(columns=expected_cols)

    result_df = pd.DataFrame(transformed_rows)

    for col in expected_cols:
        if col not in result_df.columns:
            result_df[col] = None

    return result_df[expected_cols]


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Wrapper for ETL compatibility."""
    return apply_transformations(df)
