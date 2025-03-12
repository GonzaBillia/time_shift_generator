from pydantic import BaseModel
from datetime import time
from typing import Optional

class HorarioSucursalBase(BaseModel):
    sucursal_id: int
    dia_id: int
    hora_apertura: time
    hora_cierre: time

class HorarioSucursalUpdate(BaseModel):
    id: Optional[int] = None
    sucursal_id: Optional[int] = None
    dia_id: Optional[int] = None
    hora_apertura: Optional[time] = None
    hora_cierre: Optional[time] = None

class HorarioSucursalResponse(HorarioSucursalBase):
    id: int

    model_config = {
        "from_attributes": True,
        "json_encoders": {
            time: lambda v: v.isoformat()
        }
    }
