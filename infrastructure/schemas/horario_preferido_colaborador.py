from pydantic import BaseModel
from datetime import time
from typing import Optional

class HorarioPreferidoColaboradorBase(BaseModel):
    colaborador_id: int
    fecha_inicio: time
    fecha_fin: time
    dia_id: int
    horario_corrido: bool = False

class HorarioPreferidoColaboradorUpdate(BaseModel):
    colaborador_id: Optional[int]
    fecha_inicio: Optional[time]
    fecha_fin: Optional[time]
    dia_id: Optional[int]
    horario_corrido: Optional[bool]

class HorarioPreferidoColaboradorResponse(HorarioPreferidoColaboradorBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            time: lambda v: v.isoformat()
        }
    }
