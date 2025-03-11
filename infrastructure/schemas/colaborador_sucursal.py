from pydantic import BaseModel
from typing import Optional
from .rol import RolResponse
from . colaborador import ColaboradorResponse

class ColaboradorSucursalUpdate(BaseModel):
    colaborador_id: Optional[int]
    sucursal_id: Optional[int]
    rol_colaborador_id: Optional[int]

class ColaboradorSucursalBase(BaseModel):
    colaborador_id: int
    sucursal_id: int
    rol_colaborador_id: int

class ColaboradorSucursalDetail(BaseModel):
    colaborador: ColaboradorResponse
    rol: RolResponse

    model_config = {"from_attributes": True}

class ColaboradorSucursalResponse(ColaboradorSucursalBase):
    id: int

    model_config = {"from_attributes": True}
