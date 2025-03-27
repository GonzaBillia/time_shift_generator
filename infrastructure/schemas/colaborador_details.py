# schemas/colaborador_detail_schema.py
from pydantic import BaseModel, ConfigDict
from typing import List, Tuple, Dict, Optional
from datetime import date, time
from .sucursal import SucursalResponse
from .horario import HorarioResponse
from .tipo_empleado import TipoEmpleadoResponse
from .rol import RolResponse
from .empresa import EmpresaResponse
from .colaborador import ColaboradorUpdate
from .horario_preferido_colaborador import HorarioPreferidoColaboradorResponse

class ColaboradorDetailSchema(BaseModel):
    id: int
    nombre: str
    legajo: Optional[int]
    email: Optional[str]
    telefono: Optional[str]
    dni: str
    empresa: EmpresaResponse
    sucursales: List[SucursalResponse]
    roles: List[RolResponse]
    horario_preferido: List[HorarioPreferidoColaboradorResponse]
    dias_preferidos: List[int]
    tipo_empleado: TipoEmpleadoResponse
    horario_asignado: Optional[List[HorarioResponse]] = None
    hs_extra: Dict[str, int]
    vacaciones: List[date]
    horario_corrido: bool

    model_config = ConfigDict(from_attributes=True)

class ColaboradorFullUpdate(BaseModel):
    colaborador: ColaboradorUpdate
    horario_preferido: Optional[List[HorarioPreferidoColaboradorResponse]] = []
    roles: Optional[List[RolResponse]]        # Lista de IDs de roles, ordenada
    sucursales: Optional[List[SucursalResponse]]
