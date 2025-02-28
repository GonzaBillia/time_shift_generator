from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class HorarioBase(BaseModel):
    colaborador_id: Optional[int] = None 
    sucursal_id: int
    dia_id: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    horario_corrido: bool

class HorarioUpdate(BaseModel):
    colaborador_id: Optional[int] = None  # Puede ser None para horarios generales
    sucursal_id: Optional[int]
    dia_id: Optional[int]
    fecha: Optional[date]
    hora_inicio: Optional[time]
    hora_fin: Optional[time]
    horario_corrido: Optional[bool]

class HorarioResponse(HorarioBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            date: lambda v: v.isoformat(),
            time: lambda v: v.strftime("%H:%M:%S")
        }
    }
