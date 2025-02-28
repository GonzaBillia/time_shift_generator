from pydantic import BaseModel
from typing import List
from .rol import RolResponse

class FormatoBase(BaseModel):
    nombre: str

class FormatoResponse(FormatoBase):
    id: int
    roles: List[RolResponse]

    model_config = {"from_attributes": True}