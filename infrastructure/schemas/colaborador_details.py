# schemas/colaborador_detail_schema.py
from pydantic import BaseModel, ConfigDict
from typing import List, Tuple, Dict, Optional
from datetime import date, time

class BloqueSchema(BaseModel):
    inicio: time
    fin: time

    model_config = ConfigDict(json_schema_extra={"example": {"inicio": "08:00", "fin": "12:00"}})

class HorarioSchema(BaseModel):
    sucursal_id: int
    colaborador_id: Optional[int]
    dia_id: int
    fecha: date
    horario_corrido: bool
    bloques: List[BloqueSchema]

    model_config = ConfigDict(from_attributes=True)

class TipoEmpleadoSchema(BaseModel):
    id: int
    tipo: str
    horas_por_dia_max: int
    horas_semanales: int

    model_config = ConfigDict(from_attributes=True)

class RolSchema(BaseModel):
    id: int
    nombre: str
    principal: bool

    model_config = ConfigDict(from_attributes=True)

class ColaboradorDetailSchema(BaseModel):
    id: int
    nombre: str
    legajo: int
    email: str
    telefono: str
    dni: str
    sucursales: List[int]
    roles: List[RolSchema]
    # Se define cada horario como una tupla: (sucursal_id, HorarioSchema)
    horario_preferido: List[Tuple[int, HorarioSchema]]
    dias_preferidos: List[int]
    tipo_empleado: TipoEmpleadoSchema
    horario_asignado: List[Tuple[int, HorarioSchema]]
    hs_extra: Dict[str, int]
    vacaciones: List[date]
    horario_corrido: bool

    model_config = ConfigDict(from_attributes=True)
