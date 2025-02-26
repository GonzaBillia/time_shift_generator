from pydantic import BaseModel
from datetime import time

class PuestosCubiertosPorHoraBase(BaseModel):
    sucursal_id: int
    rol_colaborador_id: int
    dia_id: int
    hora: time
    cantidad_cubierta: int

class PuestosCubiertosPorHoraResponse(PuestosCubiertosPorHoraBase):
    id: int

    class Config:
        orm_mode = True
