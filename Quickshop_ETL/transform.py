import pandas as pd
from .schema import OrderRecord

def validate_and_transform(df: pd.DataFrame):
    valid, invalid = [], []
    for _, row in df.iterrows():
        try:
            rec = OrderRecord(**row.to_dict())
            rec.compute_total()
            valid.append(rec.dict())
        except Exception as e:
            bad = row.to_dict()
            bad["_error"] = str(e)
            invalid.append(bad)
    return pd.DataFrame(valid), pd.DataFrame(invalid)
