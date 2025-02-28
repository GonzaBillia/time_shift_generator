from pydantic import BaseModel
from datetime import time
from typing import Optional

class MinimoPuestosRequeridosUpdate(BaseModel):
    sucursal_id: Optional[int]
    rol_colaborador_id: Optional[int]
    dia_id: Optional[int]
    hora: Optional[time]
    cantidad_minima: Optional[int]

class MinimoPuestosRequeridosBase(BaseModel):
    sucursal_id: int
    rol_colaborador_id: int
    dia_id: int
    hora: time
    cantidad_minima: int

class MinimoPuestosRequeridosResponse(MinimoPuestosRequeridosBase):
    id: int

    model_config = {"from_attributes": True}
