from pydantic import BaseModel
from datetime import date
from typing import Optional

class VacacionColaboradorBase(BaseModel):
    colaborador_id: int
    fecha: date

class VacacionColaboradorUpdate(BaseModel):
    colaborador_id: Optional[int]
    fecha: Optional[date]

class VacacionColaboradorResponse(VacacionColaboradorBase):
    id: int

    model_config = {"from_attributes": True}
