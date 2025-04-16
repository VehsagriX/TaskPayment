from typing import Type
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from .wallet import Wallet
from .payment import Payment
from ..schemas import PaymentCreate


async def get_item_by_id(
    session: AsyncSession,
    item_id: int | UUID,
    model: Type[Wallet | Payment],
) -> Wallet | None:
    return await session.get(model, item_id)


async def create_item(
    session: AsyncSession,
    item_in: PaymentCreate,
    model: Type[Wallet | Payment],
) -> Payment:
    item = model(**item_in.model_dump())
    session.add(item)
    await session.commit()
    # await session.refresh(product)
    return item
