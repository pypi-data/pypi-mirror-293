# modelss/routes.py

from pydantic import BaseModel

class GetInstruct(BaseModel):
    type: str

class SaveInstruct(BaseModel):
    type: str
    title: str
    code: str

class DeleteInstruct(BaseModel):
    id: int

class BatchInstruct(BaseModel):
    instructs: list[SaveInstruct]
