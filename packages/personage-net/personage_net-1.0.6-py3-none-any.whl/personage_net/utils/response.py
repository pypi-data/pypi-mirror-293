# -*- coding: utf-8 -*-
# coding = utf-8
# 接口请求统一返回处理
from fastapi import HTTPException, status
from typing import Any, Dict, List, Union
from ..settings import logger

msg = {
    200: '操作成功',
    500: '操作失败',
    10001: '密码或用户名有误，请检查后重新输入',
    10002: '用户不存在',
    10003: '删除的数据不存在',
    10004: '旧密码不正确',
    10005: '用户名存在',
}

def response_result(data: Union[List[Any], Dict[str, Any], None] = None,  code: int = 200, operation: str = '默认操作', **kw) -> Dict[str, Any]:
    """
       封装统一返回结果的函数
       参数:
       data: 返回的数据, 默认是空列表
       msg: 返回的消息, 默认是 '操作成功'
       code: 自定义状态码, 默认是 200
       operation: 操作名称
       返回:
       一个包含 state, data 和 msg 的字典
       """
    if code == 200:
        logger.info(f'操作信息：{operation}，操作结果：{msg}’')
    else:
        logger.error(f'code: {code} 。错误信息：{operation} 。错误提示：{msg}')

    return {
        'state': 200,
        'data': {
            'code': code,
            'result': data or None,
            'msg': msg[code] or '操作失败',
            **kw,
        }
    }

def error_message( e: Exception = None, code=500):
    """
    操作异常，接口返回错误信息
    参数:
    - 描述参数1
    - 描述参数2
    返回:
    - 描述返回值
    """
    logger.error(f'code: {code} 。错误信息：{status.HTTP_500_INTERNAL_SERVER_ERROR} 。错误提示：{str(e)}')
    raise HTTPException(status_code=code, detail=str(e))

def system_error(e = status.HTTP_500_INTERNAL_SERVER_ERROR):
    """记录系统错误并抛出 HTTP 错误异常。
     Args:
         message: 错误信息
     """
    error_message = f"错误信息：{500} 。错误提示：{str(e)}"
    logger.error(error_message)
    raise HTTPException(status_code=500, detail=str(e))


