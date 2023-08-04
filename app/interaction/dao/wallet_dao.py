from fastapi.exceptions import HTTPException
from asyncpg.exceptions import UniqueViolationError
from fastapi.logger import logger
from datetime import datetime
from uuid import UUID, uuid4
from app.database import get_db


async def create_wallet(customer_xid):
    try:
        sql_db = await get_db()
        wallet_id = str(uuid4())
        token_id = str(uuid4())
        time = datetime.now()

        data = await sql_db.execute(
            f"""
                INSERT INTO wallets (id,balance,token,customer_id,status,created_at) 
                VALUES ('{wallet_id}',0.00,'{token_id}','{customer_xid}','disabled','{time}');"""
        )

        return {"token": token_id}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"error": "database error"})


async def fetch_wallet_token_by_customer_xid(customer_xid):
    try:
        sql_db = await get_db()

        data = await sql_db.fetch(
            f"""
                SELECT token 
                FROM wallets 
                WHERE customer_id = '{customer_xid}';"""
        )

        if len(data):
            return dict(data[0])
        return {}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"error": "database error"})


async def activate_wallet(token):
    try:
        sql_db = await get_db()

        time = datetime.now()

        data = await sql_db.execute(
            f"""
                UPDATE  wallets 
                SET status='enabled' ,enabled_at='{time}',updated_at='{time}' 
                WHERE token='{token}' AND status='disabled';"""
        )
        data = data.split(" ")
        return data
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"error": "database error"})


async def fetch_wallet_data_by_token(token):
    try:
        sql_db = await get_db()

        data = await sql_db.fetch(
            f"""
                SELECT id,balance,token,customer_id,status,created_at,enabled_at,updated_at 
                FROM wallets 
                WHERE token = '{token}';"""
        )

        if len(data):
            return dict(data[0])
        return {}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"error": "database error"})


async def disable_wallet(token):
    try:
        sql_db = await get_db()

        time = datetime.now()

        data = await sql_db.execute(
            f"""
                UPDATE  wallets 
                SET status='disabled' ,updated_at='{time}' 
                WHERE token='{token}' 
                    AND status='enabled';"""
        )
        data = data.split(" ")
        return data
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"error": "database error"})


async def add_funds(customer_id, wallet_id, amount, reference_id):
    try:
        sql_db = await get_db()
        transaction_id = str(uuid4())

        time = datetime.now()
        try:
            data = await sql_db.execute(
                f"""
                        
                UPDATE wallets 
                SET updated_at='{time}', balance=balance + {amount} 
                WHERE customer_id='{customer_id}';
                INSERT INTO transactions (id,wallet_id,created_at,type,reference_id,amount,status)
                VALUES('{transaction_id}','{wallet_id}','{time}','deposit','{reference_id}',{amount},'success');               

            """
            )
        except UniqueViolationError as exe:
            logger.exception(exe)
            raise HTTPException(
                400, detail={"error": "reference and type is not unique "}
            )

        return {
            "id": transaction_id,
            "deposited_by": customer_id,
            "status": "success",
            "deposited_at": time,
            "amount": amount,
            "reference_id": reference_id,
        }
    except HTTPException as e:
        logger.exception(e)
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"error": "database error"})


async def spend_funds(customer_id, wallet_id, amount, reference_id, status):
    try:
        sql_db = await get_db()
        transaction_id = str(uuid4())

        time = datetime.now()
        try:
            sub_query = ""
            if status == "success":
                sub_query = f"""UPDATE wallets 
                                SET updated_at='{time}', balance=balance - {amount} 
                                WHERE customer_id='{customer_id}';"""
            query = f"""

                {sub_query}
                INSERT INTO transactions (id,wallet_id,created_at,type,reference_id,amount,status)
                VALUES('{transaction_id}','{wallet_id}','{time}','withdrawal','{reference_id}',{amount},'{status}');               
            """
            data = await sql_db.execute(query)

        except UniqueViolationError as exe:
            raise HTTPException(
                400, detail={"error": "reference and type is not unique "}
            )

        return {
            "id": transaction_id,
            "deposited_by": customer_id,
            "status": status,
            "deposited_at": time,
            "amount": amount,
            "reference_id": reference_id,
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"error": "database error"})


async def get_transactions(wallet_id):
    try:
        sql_db = await get_db()

        data = await sql_db.fetch(
            f"""
                SELECT id,wallet_id,created_at,type,reference_id,status,amount 
                FROM transactions 
                WHERE wallet_id = '{wallet_id}' 
                ORDER BY created_at DESC ;"""
        )
        result = []
        for row in data:
            result.append(dict(row))

        return result
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"error": "database error"})
