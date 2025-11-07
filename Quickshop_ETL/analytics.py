from sqlalchemy import create_engine, text
import pandas as pd

def run_sql(sql, db_url="sqlite:///quickshop.db"):
    engine = create_engine(db_url)
    with engine.begin() as conn:
        res = conn.execute(text(sql))
        df = pd.DataFrame(res.fetchall(), columns=res.keys())
    return df
