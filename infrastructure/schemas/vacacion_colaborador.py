from pydantic import BaseModel
from datetime import date

class VacacionColaboradorBase(BaseModel):
    colaborador_id: int
    fecha: date

class VacacionColaboradorResponse(VacacionColaboradorBase):
    id: int

    class Config:
        orm_mode = True
