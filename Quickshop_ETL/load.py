from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
import logging

def write_parquet(df: pd.DataFrame, out_dir: str, filename: str) -> None:
    """
    Write a DataFrame to a Parquet file, creating the output directory if needed.
    """
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    dest = Path(out_dir) / filename
    df.to_parquet(dest, index=False)
    logging.info(f"✅ Wrote {len(df)} rows to {dest}")

def write_to_db(df: pd.DataFrame, table: str, db_url: str, if_exists: str = "replace") -> None:
    """
    Write a DataFrame to a SQL database table using SQLAlchemy.
    Works with PostgreSQL (psycopg2), SQLite, etc.
    """
    try:
        logging.info(f"Connecting to database: {db_url}")
        engine = create_engine(db_url)

        df.to_sql(table, engine, if_exists=if_exists, index=False, method='multi')

        logging.info(f"✅ Successfully wrote {len(df)} rows to table '{table}'")
    except Exception as e:
        logging.error(f"❌ Database write failed: {e}")
        raise