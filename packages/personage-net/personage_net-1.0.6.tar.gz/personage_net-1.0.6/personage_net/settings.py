import logging
import secrets
import base64
import os


def setup_logging():
    #  ��������־��¼��
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)

    # ������־д��error.log �ļ�
    error_handler = logging.FileHandler('logs/error.log')
    error_handler.setLevel(logging.ERROR)
    error_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    error_handler.setFormatter(error_formatter)

    # ������־ д��operation.log �ļ�
    operation_handler = logging.FileHandler('logs/operation.log')
    operation_handler.setLevel(logging.INFO)
    operation_formatter = logging.Formatter('%(asctime)s %(levelname)s:%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    operation_handler.setFormatter(operation_formatter)

    root_logger.addHandler(error_handler)
    root_logger.addHandler(operation_handler)


# ��ʼ����־����
setup_logging()

logger = logging.getLogger(__name__)




def generate_secret_key():
    """
    生成随机的jwt需要的秘钥,环境变量中如果存在则使用环境变量中的秘钥，不存在则使用随机秘钥生成并保存在环境变量中
    参数:
     - None

    返回:
     - key字符串
    """

    key = os.getenv('SECRET_KEY')
    if(key):
        return key
    else:
        key_string = secrets.token_bytes(32)
        key = base64.urlsafe_b64encode(key_string).decode('utf-8')
        save_secret_key_to_env(key)
        return key

def save_secret_key_to_env(key):
    os.environ['SECRET_KEY'] = key
    if os.name == 'net':
        os.system(f'setx SECRET_KEY {key}')