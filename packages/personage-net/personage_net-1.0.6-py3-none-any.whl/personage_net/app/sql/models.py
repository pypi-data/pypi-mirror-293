# models/models.py

from pydantic import BaseModel

class SqlOrder(BaseModel):
    title: str
    code: str