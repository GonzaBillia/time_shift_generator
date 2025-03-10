from pydantic import BaseModel
from datetime import time
from typing import Optional

class HorarioPreferidoColaboradorBase(BaseModel):
    colaborador_id: int
    sucursal_id: int  # Nueva FK a sucursales
    hora_inicio: time
    hora_fin: time
    dia_id: int
    horario_corrido: bool = False

class HorarioPreferidoColaboradorUpdate(BaseModel):
    colaborador_id: Optional[int]
    sucursal_id: Optional[int]  # Nueva FK a sucursales
    hora_inicio: Optional[time]
    hora_fin: Optional[time]
    dia_id: Optional[int]
    horario_corrido: Optional[bool]

class HorarioPreferidoColaboradorResponse(HorarioPreferidoColaboradorBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            time: lambda v: v.strftime("%H:%M:%S")
        }
    }
