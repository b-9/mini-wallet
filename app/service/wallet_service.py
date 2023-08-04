from app.interaction.dao.wallet_dao import activate_wallet as _activate_wallet
from app.interaction.dao.wallet_dao import (
    fetch_wallet_data_by_token as _fetch_wallet_data_by_token,
)
from app.interaction.dao.wallet_dao import spend_funds as _spend_funds
from app.interaction.dao.wallet_dao import add_funds as _add_funds
from app.interaction.dao.wallet_dao import disable_wallet as _disable_wallet
from app.interaction.dao.wallet_dao import get_transactions as _get_transactions
from app.mapper.wallet_mapper import wallet_info_mapper, transactions_mapper
from fastapi.exceptions import HTTPException


async def activate_wallet(token):
    data = await _activate_wallet(token)
    if data[1] == "0":
        raise HTTPException(400, detail={"error": "Already enabled"})

    data = await _fetch_wallet_data_by_token(token)
    data = wallet_info_mapper(data)
    return {"wallet": data}


async def disable_wallet(token):
    data = await _disable_wallet(token)
    if data[1] == "0":
        raise HTTPException(400, detail={"error": "Already disabled"})
    data = await _fetch_wallet_data_by_token(token)
    data = wallet_info_mapper(data)
    return {"wallet": data}


async def get_wallet_details(token):
    data = await _fetch_wallet_data_by_token(token)
    if data["status"] == "disabled":
        raise HTTPException(404, detail={"error": "Wallet disabled"})
    data = wallet_info_mapper(data)
    return {"wallet": data}


async def make_deposits(token, amount, reference_id):
    data = await _fetch_wallet_data_by_token(token)
    if data["status"] == "disabled":
        raise HTTPException(404, detail={"error": "Wallet disabled"})
    data = await _add_funds(data["customer_id"], data["id"], amount, reference_id)
    return {"deposit": data}


async def use_wallet(token, amount, reference_id):
    data = await _fetch_wallet_data_by_token(token)
    if data["status"] == "disabled":
        raise HTTPException(404, detail={"error": "Wallet disabled"})
    if data["balance"] < amount:
        data = await _spend_funds(
            data["customer_id"], data["id"], amount, reference_id, "failed"
        )
        raise HTTPException(
            422,
            detail={"error": "funds are not avaliable to complete this transaction"},
        )

    data = await _spend_funds(
        data["customer_id"], data["id"], amount, reference_id, "success"
    )
    return {"withdrawal": data}


async def get_transactions(token):
    data = await _fetch_wallet_data_by_token(token)
    if data["status"] == "disabled":
        raise HTTPException(404, detail={"error": "Wallet disabled"})
    result = await _get_transactions(wallet_id=data["id"])
    result = transactions_mapper(result)
    return {"transactions": result}
