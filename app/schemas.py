from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, PositiveFloat

from app.models.payment import PaymentStatus


class RequestPayment(BaseModel):
    wallet_id: int
    amount: PositiveFloat



class ResponsePayment(BaseModel):
    payment_id: UUID
    message: str

class PaymentSchema(BaseModel):
    id: UUID
    wallet_id: int
    amount: PositiveFloat
    status: PaymentStatus

class ResponseFullPayment(PaymentSchema):

    created_at: datetime



class FullWallet(BaseModel):
    id: int
    user_id: int
    amount: int

