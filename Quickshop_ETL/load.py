from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
import logging


def write_parquet(df: pd.DataFrame, out_dir: str, filename: str) -> None:
    """Write DataFrame to a Parquet file."""
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    dest = Path(out_dir) / filename
    df.to_parquet(dest, index=False)
    logging.info(f"✅ Wrote {len(df)} rows to {dest}")


def write_to_db(df: pd.DataFrame, table: str, db_url: str, if_exists: str = "replace") -> None:
    """
    Write a DataFrame to a SQL database (Postgres, SQLite, MSSQL, etc.)
    Works safely with pandas >= 2.2.0 and SQLAlchemy 2.x.
    """
    try:
        engine = create_engine(db_url, future=True)

        # --- FIX: use the raw DBAPI connection under the hood ---
        with engine.connect() as conn:
            dbapi_conn = getattr(conn, "connection", conn)  # fallback if older SQLAlchemy
            df.to_sql(table, con=dbapi_conn, if_exists=if_exists, index=False, method="multi")

        logging.info(f"✅ Successfully wrote {len(df)} rows to '{table}' via {db_url}")
    except Exception as e:
        logging.error(f"❌ Database write failed: {e}")
        raise
