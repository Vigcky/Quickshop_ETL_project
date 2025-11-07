import pandas as pd
from Quickshop_ETL.load import write_parquet, write_to_db
from sqlalchemy import create_engine, text

def test_write_parquet(tmp_path, sample_orders):
    """Ensure DataFrame is written to a Parquet file."""
    output_dir = tmp_path / "out"
    write_parquet(sample_orders, output_dir, "test_orders.parquet")
    parquet_file = output_dir / "test_orders.parquet"
    assert parquet_file.exists()

def test_write_to_db_replace_mode(tmp_path, sample_orders):
    """Ensure if_exists='replace' overwrites existing table."""
    db_file = tmp_path / "test_orders.db"
    engine_url = f"sqlite:///{db_file}"
    
    # Write once
    write_to_db(sample_orders, "orders_transformed", engine_url)
    
    # Create a smaller dataframe and write again with replace
    smaller_orders = sample_orders.iloc[:1]
    write_to_db(smaller_orders, "orders_transformed", engine_url, if_exists="replace")
    
    engine = create_engine(engine_url)
    df_read = pd.read_sql("SELECT * FROM orders_transformed", con=engine)
    
    # Should only have 1 row, not original count
    assert len(df_read) == 1
