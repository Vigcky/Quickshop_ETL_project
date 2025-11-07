from sqlalchemy import Column, Integer, Numeric, Date
from .db import Base


class OrderTransformed(Base):
    __tablename__ = "orders_transformed"

    order_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, nullable=False)
    qty = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    order_total = Column(Numeric(10, 2), nullable=False)
    order_date = Column(Date, nullable=False)
