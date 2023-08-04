from fastapi import APIRouter, Form, Header
from fastapi.exceptions import HTTPException
from app.utils.common_utils import get_token
from app.service.wallet_service import activate_wallet as _activate_wallet
from app.service.wallet_service import disable_wallet as _disable_wallet
from app.service.wallet_service import get_wallet_details as _get_wallet_details
from app.service.wallet_service import make_deposits as _make_deposits
from app.service.wallet_service import use_wallet as _use_wallet
from app.service.wallet_service import get_transactions as _get_transactions
from app.utils.response_handler import response_handler


router = APIRouter()


@router.post("")
async def activate_wallet(authorization: str = Header(...)):
    token = await get_token(authorization)
    data = await _activate_wallet(token)
    return response_handler(201, data)


@router.get("")
async def get_wallet_details(authorization: str = Header(...)):
    token = await get_token(authorization)
    data = await _get_wallet_details(token)
    return response_handler(200, data)


@router.get("/transactions")
async def get_transactions(authorization: str = Header(...)):
    token = await get_token(authorization)
    data = await _get_transactions(token)
    return response_handler(200, data)


@router.post("/deposits")
async def make_deposits(
    authorization: str = Header(...),
    amount: float = Form(..., gt=0),
    reference_id: str = Form(..., max_length=50),
):
    token = await get_token(authorization)
    data = await _make_deposits(token, amount, reference_id)
    return response_handler(201, data)


@router.post("/withdrawals")
async def use_wallet(
    authorization: str = Header(...),
    amount: float = Form(..., gt=0),
    reference_id: str = Form(..., max_length=50),
):
    token = await get_token(authorization)
    data = await _use_wallet(token, amount, reference_id)
    return response_handler(201, data)


@router.patch("")
async def disable_wallet(
    authorization: str = Header(...), is_disabled: bool = Form(...)
):
    token = await get_token(authorization)
    if is_disabled == False:
        raise HTTPException(
            400, detail={"error": "bad request only disable option is avalible"}
        )
    data = await _disable_wallet(token)
    return response_handler(status_code=201, data=data)
