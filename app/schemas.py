from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, PositiveFloat, Field

from app.models.payment import PaymentStatus


class RequestPayment(BaseModel):
    wallet_id: int = Field(ge=1)
    amount: PositiveFloat
    service_id: int = Field(ge=1)
    country: str | None = None


class ResponsePostPayment(BaseModel):
    payment_id: UUID
    message: str


class ResponseGetPayment(BaseModel):
    status: PaymentStatus
    created_at: datetime


class PaymentCreate(BaseModel):
    id: UUID
    wallet_id: int
    amount: PositiveFloat
    service_id: int
    status: PaymentStatus
