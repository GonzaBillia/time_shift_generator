from pydantic import BaseModel
from datetime import time
from typing import Optional, List

class HorarioBase(BaseModel):
    puesto_id: int
    hora_inicio: time
    hora_fin: time
    horario_corrido: bool

class HorarioUpdate(BaseModel):
    id: int
    # Opcionalmente se puede actualizar la referencia al puesto si fuera necesario
    puesto_id: Optional[int] = None
    hora_inicio: Optional[time] = None
    hora_fin: Optional[time] = None
    horario_corrido: Optional[bool] = None

class HorarioDeleteRequest(BaseModel):
    ids: List[int]

class HorarioResponse(HorarioBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            time: lambda v: v.strftime("%H:%M:%S")
        }
    }
