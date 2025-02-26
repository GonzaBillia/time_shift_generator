from pydantic import BaseModel
from typing import List
from .rol import RolResponse

class FormatoBase(BaseModel):
    nombre: str

class FormatoResponse(FormatoBase):
    id: int
    roles: List[RolResponse]

    class Config:
        orm_mode = True
