from typing import Union
from setting import BASE_ROUTER
from fastapi import FastAPI, Form
from app.database import init_db
from app.router.wallet_router import router as wallet_router
from app.service.common_service import create_wallet as _create_wallet
from app.utils.response_handler import response_handler
from fastapi.exceptions import HTTPException

app = FastAPI()
app.include_router(router=wallet_router, prefix=f"{BASE_ROUTER}/api/v1/wallet")


@app.on_event("startup")
async def startup_proccess():
    await init_db()


@app.exception_handler(HTTPException)
async def error_http_middleware(request, exe):
    return response_handler(exe.status_code, data=exe.detail, status="failed")


@app.post(f"{BASE_ROUTER}/api/v1/init")
async def create_wallet(customer_xid: str = Form(..., max_length=50)):
    data = await _create_wallet(customer_xid)
    return response_handler(201, data)
