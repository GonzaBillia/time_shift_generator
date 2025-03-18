from typing import List, Optional
from infrastructure.databases.models.horario_sucursal import HorarioSucursal
from infrastructure.repositories.horario_sucursal_repo import HorarioSucursalRepository


def obtener_horarios_sucursal(sucursal_id: int, db=None) -> List[HorarioSucursal]:
    horarios_sucursal = HorarioSucursalRepository.get_by_sucursal(sucursal_id, db)
    horarios: List[HorarioSucursal] = []

    for hs in horarios_sucursal:
        horario = HorarioSucursal(
            sucursal_id=hs.sucursal_id,
            dia_id=hs.dia_id,
            hora_apertura=hs.hora_apertura,
            hora_cierre=hs.hora_cierre,
        )
        horarios.append(horario)

    return horarios
