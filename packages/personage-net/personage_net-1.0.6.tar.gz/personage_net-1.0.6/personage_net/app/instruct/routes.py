# coding = utf-8
# app/utils/routes.py
from fastapi import APIRouter, Depends
from personage_net.db.connection import get_db_conn
from personage_net.utils.response import response_result, error_message
from .models import GetInstruct, BatchInstruct, DeleteInstruct
from aiomysql import Connection
from personage_net.utils.jwt.config import verify_jwt_token
router = APIRouter()

# 获取py的指令级列表
@router.post('/fast/getInstruct')
async def get_instruct(info: GetInstruct, conn: Connection = Depends(get_db_conn), user=Depends(verify_jwt_token)):
    try:
        async with conn.cursor() as cursor:
            sql = "SELECT id, title, code, type FROM my_project.instruct WHERE (%s = '' OR type = %s)"
            await cursor.execute(sql, (info.type, info.type))
            result = await cursor.fetchall()
            data = [{**row} for row in result] if result else []
            return response_result(operation='查询指令集', data=data)
    except Exception as e:
        # 捕获所有异常并处理
        error_message(e)

# 批量/单独 存储py的指令级
@router.post('/fast/saveInstruct')
async def save_instruct(info: BatchInstruct, conn: Connection=Depends(get_db_conn), user=Depends(verify_jwt_token)):
    try:
        async with conn.cursor() as cursor:
            values = [(instr.type, instr.title, instr.code) for instr in info.instructs]
            sql = "insert into my_project.instruct (type, title, code) values (%s, %s, %s)"
            await cursor.executemany(sql, values)
            return response_result(operation='增加指令')
    except Exception as e:
        error_message(e)

# 删除py的指令级
@router.delete('/fast/delInstruct')
async def del_instruct(info: DeleteInstruct, conn: Connection=Depends(get_db_conn), user=Depends(verify_jwt_token)):
    try:
        async with conn.cursor() as cursor:
            await cursor.execute('delete from my_project.instruct where id = %s', (info.id,))
            if cursor.rowcount == 0:
                return response_result(code=10003, operation='删除指令')
            else:
                return response_result(operation='删除指令')
    except Exception as e:
        error_message(e)