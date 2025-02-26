from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class HorarioBase(BaseModel):
    colaborador_id: Optional[int] = None  # Puede ser None para horarios generales
    sucursal_id: int
    dia_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    horario_corrido: bool

class HorarioResponse(HorarioBase):
    id: int

    class Config:
        orm_mode = True
