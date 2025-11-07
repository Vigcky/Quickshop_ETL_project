from pathlib import Path
from datetime import date, timedelta
import pandas as pd
import logging

def find_order_files(input_dir, start_date, end_date):
    """Find all order CSV files between start_date and end_date."""
    start, end = pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()
    files = []
    cur = start
    while cur <= end:
        f = Path(input_dir) / f"orders_{cur.strftime('%Y%m%d')}.csv"
        if f.exists():
            files.append(f)
        cur += timedelta(days=1)
    
    logging.info(f"Found {len(files)} order files for date range {start} to {end}")
    if files:
        logging.debug(f"Order files: {files}")
    return files

def read_orders(files):
    """Read and concatenate multiple order CSV files."""
    if not files:
        logging.warning("No order files to read")
        return pd.DataFrame()
    
    try:
        dfs = []
        for f in files:
            try:
                df = pd.read_csv(f)
                dfs.append(df)
                logging.debug(f"Read {len(df)} rows from {f}")
            except Exception as e:
                logging.error(f"Failed to read {f}: {e}")
                # Continue with other files instead of failing completely
                continue
        
        if not dfs:
            logging.warning("No valid order data found")
            return pd.DataFrame()
        
        result = pd.concat(dfs, ignore_index=True)
        logging.info(f"Loaded {len(result)} total order records from {len(dfs)} files")
        return result
    except Exception as e:
        logging.error(f"Error concatenating order files: {e}")
        raise

def read_products(input_dir):
    """Read products reference data."""
    f = Path(input_dir) / "products.csv"
    if not f.exists():
        logging.warning(f"Products file not found: {f}")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(f)
        logging.info(f"Loaded {len(df)} products")
        return df
    except Exception as e:
        logging.error(f"Failed to read products file: {e}")
        raise

def read_inventory(input_dir):
    """Read inventory reference data."""
    f = Path(input_dir) / "inventory.csv"
    if not f.exists():
        logging.warning(f"Inventory file not found: {f}")
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(f)
        logging.info(f"Loaded {len(df)} inventory records")
        return df
    except Exception as e:
        logging.error(f"Failed to read inventory file: {e}")
        raise