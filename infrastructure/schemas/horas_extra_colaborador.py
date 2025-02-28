from pydantic import BaseModel
from typing import Optional

class HorasExtraColaboradorBase(BaseModel):
    colaborador_id: int
    tipo: str
    cantidad: int

class HorasExtraColaboradorUpdate(BaseModel):
    colaborador_id: Optional[int]
    tipo: Optional[str]
    cantidad: Optional[int]

class HorasExtraColaboradorResponse(HorasExtraColaboradorBase):
    id: int

    model_config = {"from_attributes": True}
