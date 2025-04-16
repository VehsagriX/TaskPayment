from datetime import datetime
from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy.orm import DeclarativeBase

class WalletBase(DeclarativeBase):
    pass


class Wallet(WalletBase):
    __tablename__ = "wallets"

    id: Mapped[int]= mapped_column(primary_key=True)
    user_number: Mapped[int] = mapped_column(unique=True, index=True)
    amount: Mapped[float] = mapped_column(nullable=False)



