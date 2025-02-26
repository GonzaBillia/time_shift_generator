from pydantic import BaseModel
from datetime import time

class MinimoPuestosRequeridosBase(BaseModel):
    sucursal_id: int
    rol_colaborador_id: int
    dia_id: int
    hora: time
    cantidad_minima: int

class MinimoPuestosRequeridosResponse(MinimoPuestosRequeridosBase):
    id: int

    class Config:
        orm_mode = True
