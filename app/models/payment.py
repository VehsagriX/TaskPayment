from datetime import datetime
from enum import Enum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

class PaymentBase(DeclarativeBase):
    pass

class PaymentStatus(Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class Payment(PaymentBase):
    __tablename__ = "payments"

    id: Mapped[UUID]= mapped_column(UUID(as_uuid=True), primary_key=True, unique=True)
    wallet_id: Mapped[int] = mapped_column(index=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(default=PaymentStatus.pending)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)
