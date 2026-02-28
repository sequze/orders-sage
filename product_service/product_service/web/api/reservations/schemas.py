import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    product_id: uuid.UUID
    order_id: uuid.UUID
    qty: int = Field(gt=0)


class ReservationResponse(BaseModel):
    id: uuid.UUID
    product_id: uuid.UUID
    order_id: uuid.UUID
    qty: int
    created_at: datetime

    model_config = {"from_attributes": True}


class ReservationListResponse(BaseModel):
    items: list[ReservationResponse]
    total: int
