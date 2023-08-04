from app.interaction.dao.wallet_dao import create_wallet as _create_wallet
from app.interaction.dao.wallet_dao import (
    fetch_wallet_token_by_customer_xid as _fetch_wallet_token_by_customer_xid,
)


async def create_wallet(customer_xid):
    data = await _fetch_wallet_token_by_customer_xid(customer_xid)
    if data:
        return data
    return await _create_wallet(customer_xid)
