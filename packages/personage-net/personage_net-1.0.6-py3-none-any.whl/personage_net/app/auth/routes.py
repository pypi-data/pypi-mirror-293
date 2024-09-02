# coding = utf-8
# app/auth/routes.py
from fastapi import APIRouter, Depends
from aiomysql import Connection
from personage_net.db.connection import get_db_conn
from .models import User, Login, LoginOutModel, ResetPsswordModel
from personage_net.utils.response import response_result, error_message
from personage_net.utils.crypto.rsa import encrypted_decode_key
from personage_net.utils.crypto.aes import aes_decrypt
from personage_net.utils.crypto.bcrypt import check_password, hashed_password
from personage_net.utils.jwt.config import generate_jwt_token, verify_jwt_token
router = APIRouter()

@router.get('/fast/getUserlist')
async def read_user_list(conn=Depends(get_db_conn), user=Depends(verify_jwt_token)):
    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM my_project.userinfo")
        result = await cursor.fetchall()
        if not result:
            return response_result(operation='查询用户列表')
        data = [{**row} for row in result]
        return response_result(operation='查询用户列表', data=data)

@router.post('/fast/createUser')
async def save_user_info(user_info: User, conn: Connection = Depends(get_db_conn), user=Depends(verify_jwt_token)):
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(f"SELECT * from my_projct.useringo where username = {user_info.username}")
            result = await cursor.fetchall()
            if not result:
                await cursor.execute("INSERT INTO my_project.userinfo (name, username, password) VALUES (%s, %s, %s)",
                                     (user_info.name, user_info.username, user_info.password))
                return response_result(operation='创建用户')
            return response_result(code=10005, operation='创建用户')
    except Exception as e:
        error_message(e)

@router.post('/fast/login')
async def user_login(LoginInfo: Login, conn: Connection = Depends(get_db_conn) ):
    # rsa私钥进行解密aes私钥
    aes_private_key = encrypted_decode_key(LoginInfo.AES)

    # aes跟IV反解密码跟账户
    aes_dispose_password = aes_decrypt(LoginInfo.password, aes_private_key, LoginInfo.IV)
    username = aes_decrypt(LoginInfo.username, aes_private_key, LoginInfo.IV)

    async with conn.cursor() as cursor:
        await cursor.execute("SELECT * FROM my_project.userinfo u where username = %s", username)
        result = await cursor.fetchone()
        if not result:
            return response_result(code=10002, operation='用户登录')
        if check_password(result['password'], aes_dispose_password):
            info = {'id': result['id'], 'role': result['role'], 'name': result['username']}
            token = generate_jwt_token(info)
            return response_result(operation='用户登录', userInfo=info, token=token)
        else:
            return response_result(code=10001, operation='用户登录')

@router.post('/fast/logout')
async def user_login_out(userId: LoginOutModel, user=Depends(verify_jwt_token)):
    return response_result(operation='退出登录')


@router.post('/fast/resetPassword')
async def user_reset_password(info: ResetPsswordModel, conn: Connection = Depends(get_db_conn), user=Depends(verify_jwt_token)):
    try:
        aes_private_key = encrypted_decode_key(info.AES)
        old_password = aes_decrypt(info.OPassword, aes_private_key, info.IV)
        new_password = aes_decrypt(info.NPassword, aes_private_key, info.IV)
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM my_project.userinfo u where id = %s", user['id'])
            result = await cursor.fetchone()
            if not check_password(result['password'], old_password):
                return response_result(code=10004)
            hash_password = hashed_password(new_password)
            await cursor.execute("UPDATE my_project.userinfo SET password = %s WHERE id = %s",
                                 (hash_password, user['id']))
            return response_result(operation='重置密码')
    except Exception as e:
        error_message(e)

