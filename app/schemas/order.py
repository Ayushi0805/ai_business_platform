from pydantic import BaseModel
from typing import Optional

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    quantity: int
    total_price: float

class OrderResponse(BaseModel):
    order_id: int
    status: str
    fraud: bool
    image_analysis: Optional[dict] = None
    invoice_data: Optional[dict] = None
    decision: str
    n8n_triggered: bool

    class Config:
        from_attributes = True
