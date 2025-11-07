import pytest
from Quickshop_ETL.db import Base, engine, SessionLocal
from Quickshop_ETL.models import OrderTransformed as Order
import pandas as pd

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)

@pytest.fixture()
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()
@pytest.fixture
def sample_orders():
    return pd.DataFrame([
        {"product_id": 101, "qty": 2, "unit_price": 50.0, "order_date": "2025-11-07"},
        {"product_id": 102, "qty": 1, "unit_price": 80.0, "order_date": "2025-11-07"}
    ])


@pytest.fixture
def invalid_orders():
    return pd.DataFrame([
        {"product_id": 103, "qty": -1, "unit_price": 20.0, "order_date": "2025-11-07"},  # invalid qty
        {"product_id": 104, "qty": 3, "unit_price": -50.0, "order_date": "2025-11-07"}  # invalid price
    ])