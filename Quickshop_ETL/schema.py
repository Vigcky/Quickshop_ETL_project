from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional
from datetime import date

class OrderRecord(BaseModel):
    order_id: Optional[int] = None
    product_id: int
    qty: int
    unit_price: float
    order_date: date

    @field_validator("qty")
    @classmethod
    def qty_non_neg(cls, v):
        if v < 0:
            raise ValueError("qty must be >= 0")
        return v

    @field_validator("unit_price")
    @classmethod
    def price_non_neg(cls, v):
        if v < 0:
            raise ValueError("unit_price must be >= 0")
        return v

    def compute_total(self):
        self.order_total = round(self.qty * self.unit_price, 2)
        return self.order_total