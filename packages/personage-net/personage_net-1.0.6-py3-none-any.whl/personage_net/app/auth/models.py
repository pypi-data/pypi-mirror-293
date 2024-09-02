# modelss/routes.py

from pydantic import BaseModel, SecretStr

class User(BaseModel):
    name: str
    username: str
    password: str

class Login(BaseModel):
    username:  str
    password: str
    verification: str
    IV: str
    AES: str

class infoModel(BaseModel):
    info: object

class LoginOutModel(BaseModel):
    id: int

class ResetPsswordModel(BaseModel):
    OPassword: str
    NPassword: str
    IV: str
    AES: str