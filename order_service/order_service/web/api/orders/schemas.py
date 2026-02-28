import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, Field

from order_service.db.models.order import OrderStatus


class OrderCreate(BaseModel):
    product_id: uuid.UUID
    qty: int = Field(gt=0)
    total: Decimal = Field(gt=0, max_digits=12, decimal_places=2)


class OrderUpdate(BaseModel):
    qty: Optional[int] = Field(default=None, gt=0)
    total: Optional[Decimal] = Field(default=None, gt=0, max_digits=12, decimal_places=2)
    status: Optional[OrderStatus] = None


class OrderResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    qty: int
    total: Decimal
    status: OrderStatus
    created_at: datetime

    model_config = {"from_attributes": True}


class OrderListResponse(BaseModel):
    items: list[OrderResponse]
    total: int

