import jwt
from personage_net.settings import generate_secret_key
from personage_net.utils.response import system_error, error_message
from ..redis.redis_manager import store_token_redis, get_token_redis
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends

SECRET_KEY = generate_secret_key()
ALGORITHM = 'HS256'

oauth_scheme = OAuth2PasswordBearer(tokenUrl="Authorization")

def generate_jwt_token(data, **kw) -> str:
    """
    生成token的接口
    参数:
    - data: 需要传token中保存的用户信息参数
        id: 用户id
        role: 用户角色 admin or user
        name: 用户名
        claims: 其他参数
    - kw: 其他参数
    返回:
    - 返回token的字符串
    """
    token_info = {
        'sub': data['id'],
        'aud': 'personage_net',
        'iss': 'tung',
        'role': data['role'],
        'name': data['name'],
        'claims': {**kw}
    }
    try:
        token = jwt.encode(token_info, SECRET_KEY, algorithm=ALGORITHM)
        store_token_redis(token, token_info)
        return token
    except Exception as e:
        system_error(e)

def verify_jwt_token(token: str = Depends(oauth_scheme)):
    """
    验证token的接口
    参数:
    - token: token
    返回:
    - 返回token中保存的用户信息
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM], audience='personage_net')
        user_info = get_token_redis(token)
        if payload['sub'] != user_info['sub']:
            error_message('无效的Token', 401)
        return {
            'id': user_info['sub'],
            'role': user_info['role'],
            'name': user_info['name'],
            'claims': user_info['claims']
        }
    except jwt.ExpiredSignatureError:
        error_message('Token已过期', 401)
    except jwt.InvalidTokenError:
        error_message('无效的Token', 401)
    except Exception as e:
        system_error(e)
