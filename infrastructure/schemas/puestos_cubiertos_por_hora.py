from pydantic import BaseModel
from typing import Optional
from datetime import time

class PuestosCubiertosPorHoraBase(BaseModel):
    sucursal_id: int
    rol_colaborador_id: int
    dia_id: int
    hora: time
    cantidad_cubierta: int

class PuestosCubiertosPorHoraUpdate(BaseModel):
    sucursal_id: Optional[int]
    rol_colaborador_id: Optional[int]
    dia_id: Optional[int]
    hora: Optional[time]
    cantidad_cubierta: Optional[int]

class PuestosCubiertosPorHoraResponse(PuestosCubiertosPorHoraBase):
    id: int

    model_config = {"from_attributes": True}
