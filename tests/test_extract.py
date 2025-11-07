import pandas as pd
import pytest
from Quickshop_ETL.extract import read_orders, find_order_files
from pathlib import Path


def test_find_order_files(tmp_path):
    csv_file = tmp_path / "orders_20251101.csv"
    csv_file.write_text("order_id,product_id,qty,unit_price,order_date\n1,101,2,100.0,2025-11-01\n")

    files = find_order_files(tmp_path, "2025-11-01", "2025-11-05")
    assert len(files) == 1
    assert files[0].name == "orders_20251101.csv"


def test_read_orders_valid(tmp_path):
    f = tmp_path / "orders_20251101.csv"
    f.write_text("order_id,product_id,qty,unit_price,order_date\n1,101,2,100.0,2025-11-01\n")
    df = read_orders([f])
    assert not df.empty
    assert "order_id" in df.columns


def test_read_orders_no_files(caplog):
    caplog.set_level("WARNING")
    df = read_orders([])
    assert df.empty
    assert any("No order files" in message for message in caplog.messages)
