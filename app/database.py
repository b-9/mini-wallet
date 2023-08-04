import asyncpg
from setting import DB_CONFIG

sql_db = None


async def init_db():
    global sql_db

    sql_db = await asyncpg.connect(
        dsn=f"""postgres://{DB_CONFIG["DB_USER"]}:{DB_CONFIG["DB_PASSWORD"]}@{DB_CONFIG["DB_HOST"]}:{DB_CONFIG["DB_PORT"]}/{DB_CONFIG["DB_NAME"]}"""
    )


async def get_db():
    global sql_db
    return sql_db
