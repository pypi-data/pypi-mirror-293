# db/connection.py
import aiomysql
from typing import Optional
from personage_net.settings import logger

db_pool: Optional[aiomysql.Pool] = None

async def init_db_pool(host: str, port: int, user: str, password: str, db: str):
    global db_pool
    try:
        db_pool = await aiomysql.create_pool(
            host=host,
            port=port,
            user=user,
            password=password,
            db=db,
            autocommit=True,
            cursorclass=aiomysql.DictCursor
        )
        logger.info('数据库连接成功')
    except Exception as e:
        logger.error(f'数据库连接失败,失败原因: {e}')

async def close_db_pool():
    global db_pool
    if db_pool:
        try:
            db_pool.close()
            await db_pool.wait_closed()
            logger.info('数据库关闭成功')
        except Exception as e:
            logger.error(f'数据库关闭失败，失败原因{e}')

# 获取数据库连接
async def get_db_conn():
    global db_pool
    if db_pool:
        try:
            conn = await db_pool.acquire()
            return conn
        except Exception as e:
            logger.error(f'数据库实例获取失败, 错误原因：{e}')
            raise
    else:
        raise RuntimeError("Database connection pool is not initialized.")

