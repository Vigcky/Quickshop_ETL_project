from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class OrderRecord(BaseModel):
    order_id: str = Field(..., min_length=1)
    customer_id: str
    order_date: datetime
    product_id: str
    qty: int
    unit_price: float
    order_total: Optional[float] = None

    @validator("qty")
    def qty_non_neg(cls, v):
        if v < 0:
            raise ValueError("qty must be >= 0")
        return v

    @validator("unit_price")
    def price_non_neg(cls, v):
        if v < 0:
            raise ValueError("unit_price must be >= 0")
        return v

    def compute_total(self):
        self.order_total = round(self.qty * self.unit_price, 2)
        return self.order_total
