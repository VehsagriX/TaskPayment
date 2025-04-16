import asyncio
import uuid

import uvicorn
from contextlib import asynccontextmanager
from uuid import UUID
from aiohttp import ClientResponseError
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from .models.payment import PaymentBase, Payment, PaymentStatus
from .models.wallet import WalletBase, Wallet
from .models.db_help import wallet_db, payment_db
from .schemas import RequestPayment, ResponsePostPayment, PaymentCreate, ResponseGetPayment

from .models.db_work import get_item_by_id, create_item
from .service import get_api_country, get_api_chukc


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with wallet_db.engin.begin() as conn:
        await conn.run_sync(WalletBase.metadata.create_all)
    async with payment_db.engin.begin() as conn:
        await conn.run_sync(PaymentBase.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


@app.post("/payment", status_code=status.HTTP_201_CREATED)
async def root(payment: RequestPayment,
               wallet_session: AsyncSession = Depends(wallet_db.session_dependency),
               payment_session: AsyncSession = Depends(payment_db.session_dependency)) -> ResponsePostPayment:
    wallet = await get_item_by_id(session=wallet_session, item_id=payment.wallet_id, model=Wallet)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if wallet.amount < payment.amount:
        raise HTTPException(status_code=400, detail="Wallet amount too low")

    wallet.amount -= payment.amount

    payment_id = uuid.uuid4()
    my_payment = PaymentCreate(id=payment_id, wallet_id=wallet.id, amount=payment.amount,
                               status=PaymentStatus.pending)
    try:
        serv_1, serv_2 = await asyncio.gather(get_api_country(country=payment.country), get_api_chukc())
        print(serv_1, serv_2, sep='\n')
        my_payment.status = PaymentStatus.success
        res_payment = await create_item(session=payment_session, item_in=my_payment, model=Payment)
        await wallet_session.commit()
        return ResponsePostPayment(payment_id=res_payment.id, message="created payment")
    except ClientResponseError as e:
        my_payment.status = PaymentStatus.failed
        res_payment = await create_item(session=payment_session, item_in=my_payment, model=Payment)
        await wallet_session.rollback()
        print(e.message)
        return ResponsePostPayment(payment_id=res_payment.id, message=e.message)


@app.get("/payment/{payment_id}")
async def get_pyment_by_id(payment_id: UUID,
                           session: AsyncSession = Depends(payment_db.session_dependency)):
    payment = await get_item_by_id(session=session, item_id=payment_id, model=Payment)
    if payment is None:
        raise HTTPException(status_code=404, detail="Payment not found")
    return ResponseGetPayment.model_validate(payment, from_attributes=True)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
