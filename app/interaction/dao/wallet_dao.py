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
                                  insert into wallets (id,balance,token,customer_id,status,created_at) 
                                  values('{wallet_id}',0.00,'{token_id}','{customer_xid}','disabled','{time}');"""
        )

        return {"token": token_id}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"message": "database error"})


async def fetch_wallet_token_by_customer_xid(customer_xid):
    try:
        sql_db = await get_db()

        data = await sql_db.fetch(
            f"""
                                  select token from wallets where customer_id = '{customer_xid}';"""
        )

        if len(data):
            return dict(data[0])
        return {}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"message": "database error"})


async def activate_wallet(token):
    try:
        sql_db = await get_db()

        time = datetime.now()

        data = await sql_db.execute(
            f"""
                                  update  wallets set status='enabled' ,enabled_at='{time}',updated_at='{time}' 
                                  where token='{token}' and status='disabled';"""
        )
        data = data.split(" ")
        return data
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"message": "database error"})


async def fetch_wallet_data_by_token(token):
    try:
        sql_db = await get_db()

        data = await sql_db.fetch(
            f"""
                                  select * from wallets where token = '{token}';"""
        )

        if len(data):
            return dict(data[0])
        return {}
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"message": "database error"})


async def disable_wallet(token):
    try:
        sql_db = await get_db()

        time = datetime.now()

        data = await sql_db.execute(
            f"""
                                  update  wallets set status='disabled' ,updated_at='{time}' 
                                  where token='{token}' and status='enabled';"""
        )
        data = data.split(" ")
        return data
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"message": "database error"})


async def add_funds(customer_id, wallet_id, amount, reference_id):
    try:
        sql_db = await get_db()
        transaction_id = str(uuid4())

        time = datetime.now()
        try:
            data = await sql_db.execute(
                f"""
                        
                update wallets set updated_at='{time}', balance=balance + {amount} 
                where customer_id='{customer_id}';
                insert into transactions (id,wallet_id,created_at,type,reference_id,amount,status)
                values('{transaction_id}','{wallet_id}','{time}','deposit','{reference_id}',{amount},'success');               

            """
            )
        except UniqueViolationError as exe:
            raise HTTPException(
                400, detail={"message": "reference and type is not unique "}
            )

        return {"id": transaction_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"message": "database error"})


async def spend_funds(customer_id, wallet_id, amount, reference_id, status):
    try:
        sql_db = await get_db()
        transaction_id = str(uuid4())

        time = datetime.now()
        try:
            sub_query = ""
            if status == "success":
                sub_query = f"""update wallets set updated_at='{time}', balance=balance - {amount} 
                                   where customer_id='{customer_id}';"""
            query = f"""

                {sub_query}
                insert into transactions (id,wallet_id,created_at,type,reference_id,amount,status)
                                    values('{transaction_id}','{wallet_id}','{time}','withdrawal','{reference_id}',{amount},'{status}');               
            """
            data = await sql_db.execute(query)

        except UniqueViolationError as exe:
            raise HTTPException(
                400, detail={"message": "reference and type is not unique "}
            )

        return {"id": transaction_id}
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"message": "database error"})


async def get_transactions(wallet_id):
    try:
        sql_db = await get_db()

        data = await sql_db.fetch(
            f"""
                select * from transactions where wallet_id = '{wallet_id}' order by created_at desc ;"""
        )
        result = []
        for row in data:
            result.append(dict(row))

        return result
    except Exception as e:
        logger.exception(e)
        raise HTTPException(500, detail={"message": "database error"})
