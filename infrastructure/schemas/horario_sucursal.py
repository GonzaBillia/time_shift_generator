from pydantic import BaseModel
from datetime import time

class HorarioSucursalBase(BaseModel):
    sucursal_id: int
    dia_id: int
    hora_apertura: time
    hora_cierre: time

class HorarioSucursalResponse(HorarioSucursalBase):
    id: int

    class Config:
        orm_mode = True
