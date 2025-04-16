import uuid

import uvicorn
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import JSONResponse

from .models.payment import PaymentBase, Payment, PaymentStatus
from .models.wallet import WalletBase, Wallet
from .models.db_help import wallet_db, payment_db
from .schemas import RequestPayment, ResponsePayment, PaymentSchema
from .models.db_work import get_item_by_id, create_item


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with wallet_db.engin.begin() as conn:
        await conn.run_sync(WalletBase.metadata.create_all)
    async with payment_db.engin.begin() as conn:
        await conn.run_sync(PaymentBase.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


@app.post("/payment")
async def root(payment: RequestPayment,
               wallet_session: AsyncSession = Depends(wallet_db.session_dependency),
               payment_session: AsyncSession = Depends(payment_db.session_dependency)):
    my_wallet = await get_item_by_id(session=wallet_session, item_id=payment.wallet_id, model=Wallet)
    if my_wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    if my_wallet.amount < payment.amount:
        raise HTTPException(status_code=400, detail="Wallet amount too low")
    payment_id = uuid.uuid4()
    my_payment = PaymentSchema(id=payment_id, wallet_id=my_wallet.id, amount=my_wallet.amount, status=PaymentStatus.pending)
    try:

        my_payment.status = PaymentStatus.success
        res_payment = await create_item(session=payment_session, item_in=my_payment, model=Payment,)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=ResponsePayment(payment_id=res_payment.id, message="success")
        )

    except Exception as e:
        my_payment.status = PaymentStatus.failed
        res_payment = await create_item(session=payment_session, item_in=my_payment, model=Payment)
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"data": ResponsePayment(payment_id=res_payment.id, message="External service unavailable")}
        )




@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
