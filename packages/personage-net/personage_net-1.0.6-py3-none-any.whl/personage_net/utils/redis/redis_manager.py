# redis-server.exe redis.windows.conf
import json
import redis
from personage_net.utils.response import error_message, system_error

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def store_token_redis(token,  user_info, expire_time=14400):
    redis_client.setex(token, expire_time, json.dumps(user_info))


def get_token_redis(token):
    try:
        ttl = redis_client.ttl(token)
        redis_info_json = redis_client.get(token)
        if ttl == -1 or ttl == -2 or not redis_info_json:
            error_message('无效的Token', 401)
        user_info = json.loads(redis_info_json)
        redis_client.expire(token, 3600)
        return user_info
    except Exception as e:
        system_error(e)

def delete_token_redis(token):
    redis_client.delete(token)


def expire_token_redis(token):
    redis_client.expire(token, 14400)