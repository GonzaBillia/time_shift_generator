from pydantic import BaseModel
from typing import Optional, List
from .rol import RolResponse
from .colaborador_sucursal import ColaboradorSucursalDetail
from .horario_sucursal import HorarioSucursalUpdate, HorarioSucursalResponse  # Con campos opcionales
from .espacio_disponible_sucursal import EspacioDisponibleSucursalUpdate, EspacioDisponibleSucursalResponse  # Con campos opcionales

class SucursalBase(BaseModel):
    nombre: str
    direccion: str
    telefono: Optional[str] = None
    empresa_id: int
    formato_id: int

class SucursalUpdate(BaseModel):
    nombre: Optional[str]
    direccion: Optional[str]
    telefono: Optional[str] = None
    empresa_id: Optional[int]
    formato_id: Optional[int]

class SucursalFullUpdate(BaseModel):
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    empresa_id: Optional[int] = None
    formato_id: Optional[int] = None
    formato: Optional[str] = None
    empresa: Optional[str] = None
    roles: Optional[List[RolResponse]] = None
    colaboradores: Optional[List[ColaboradorSucursalDetail]] = None
    countColabs: Optional[int] = None
    horarios: Optional[List[HorarioSucursalUpdate]] = None
    espacio: Optional[List[EspacioDisponibleSucursalUpdate]] = None


class SucursalResponse(SucursalBase):
    id: int

    model_config = {"from_attributes": True}

class SucursalEditResponse(BaseModel):
    id: int
    nombre: str
    direccion: str
    telefono: Optional[str] = None
    empresa_id: int
    formato_id: int
    formato: Optional[str] = None
    empresa: Optional[str] = None
    roles: Optional[List[RolResponse]] = None
    colaboradores: Optional[List[ColaboradorSucursalDetail]] = None
    countColabs: Optional[int] = None
    horarios: Optional[List[HorarioSucursalResponse]] = None
    espacio: Optional[List[EspacioDisponibleSucursalResponse]] = None

    model_config = {"from_attributes": True}