import argparse, json, logging
import pandas as pd
from pathlib import Path

def find_order_files(input_dir, start_date, end_date):
    import pandas as pd
    from datetime import timedelta
    start, end = pd.to_datetime(start_date).date(), pd.to_datetime(end_date).date()
    files, cur = [], start
    while cur <= end:
        f = Path(input_dir) / f"orders_{cur.strftime('%Y%m%d')}.csv"
        if f.exists():
            files.append(f)
        cur += timedelta(days=1)
    return files

def read_orders(files):
    dfs = []
    for f in files:
        df = pd.read_csv(f)
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True) if dfs else pd.DataFrame()

def validate_and_transform(df):
    if df.empty:
        return pd.DataFrame(), pd.DataFrame()
    df["order_total"] = df["qty"] * df["unit_price"]
    return df, pd.DataFrame()

def write_parquet(df, out_dir, filename):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    df.to_parquet(Path(out_dir)/filename, index=False)

def write_to_db(df, table, db_url):
    from sqlalchemy import create_engine
    engine = create_engine(db_url)
    df.to_sql(table, engine, if_exists="replace", index=False)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--start-date", required=True)
    parser.add_argument("--end-date", required=True)
    parser.add_argument("--format", choices=["parquet", "db"], default="parquet")
    parser.add_argument("--db-url", default="postgresql+psycopg2://postgres:182003@localhost:5432/quickshop")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
    files = find_order_files(args.input_dir, args.start_date, args.end_date)
    df = read_orders(files)
    valid, invalid = validate_and_transform(df)

    if args.format == "parquet":
        write_parquet(valid, args.output_dir, "orders_transformed.parquet")
    else:
        write_to_db(valid, "orders_transformed", args.db_url)

    summary = {
        "rows_in": len(df),
        "rows_valid": len(valid),
        "rows_invalid": len(invalid),
        "revenue": float(valid["order_total"].sum() if not valid.empty else 0.0),
    }
    with open(f"{args.output_dir}/summary.json", "w") as f:
        json.dump(summary, f, indent=2)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
