# coding = utf-8
# app/sql/routes.py
from fastapi import APIRouter, Depends
from aiomysql import Connection
from personage_net.db.connection import get_db_conn
from personage_net.utils.response import response_result, error_message
from .models import SqlOrder
from personage_net.utils.jwt.config import verify_jwt_token

router = APIRouter()

@router.get('/fast/getSqlOrder')
async def get_sql_order(conn: Connection = Depends(get_db_conn), user=Depends(verify_jwt_token)):
    try:
        async with conn.cursor() as cursor:
            await cursor.execute("select * from my_project.sql_order")
            result = await cursor.fetchall()
            data = [{** row} for row in result] if result else []
            return response_result(operation='查询sql语句', data=data)
    except Exception as e:
        error_message(e)

@router.post('/fast/saveSqlOrder')
async def save_sql_order(sql_order: SqlOrder, conn: Connection = Depends(get_db_conn), user=Depends(verify_jwt_token)):
    try:
        async with conn.cursor() as cursor:
            sql = "insert into my_project.instruct (title, code) values (%s, %s)"
            await cursor.execute(sql, (sql_order.title, sql_order.code))
            return response_result(operation='增加sql语句')
    except Exception as e:
        error_message(e)

