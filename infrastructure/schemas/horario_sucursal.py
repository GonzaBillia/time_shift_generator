from pydantic import BaseModel
from datetime import time
from typing import Optional

class HorarioSucursalBase(BaseModel):
    sucursal_id: int
    dia_id: int
    hora_apertura: time
    hora_cierre: time

class HorarioSucursalUpdate(BaseModel):
    sucursal_id: Optional[int]
    dia_id: Optional[int]
    hora_apertura: Optional[time]
    hora_cierre: Optional[time]

class HorarioSucursalResponse(HorarioSucursalBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            time: lambda v: v.isoformat()
        }
    }
