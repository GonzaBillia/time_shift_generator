# services/colaborador_service.py
from datetime import date
from typing import List, Dict, Tuple
from infrastructure.repositories import (
    colaborador_repo,
    colaborador_sucursal_repo,
    horario_preferido_colaborador_repo,
    horario_repo,
    horas_extra_colaborador_repo,
    vacacion_colaborador_repo,
    tipo_colaborador_repo,
    rol_repo
)
from domain.models.colaborador import Colaborador
from domain.models.tipo_colaborador import TipoEmpleado
from domain.models.rol import Rol
from application.services.horario_service import crear_horario
from infrastructure.utils.date_utils import get_next_date_for_dia

colaborador_repo = colaborador_repo.ColaboradorRepository()
colaborador_sucursal_repo = colaborador_sucursal_repo.ColaboradorSucursalRepository()
horario_preferido_colaborador_repo = horario_preferido_colaborador_repo.HorarioPreferidoColaboradorRepository()
horario_repo = horario_repo.HorarioRepository()
horas_extra_colaborador_repo = horas_extra_colaborador_repo.HorasExtraColaboradorRepository()
vacacion_colaborador_repo = vacacion_colaborador_repo.VacacionColaboradorRepository()
tipo_colaborador_repo = tipo_colaborador_repo.TipoEmpleadoRepository()
rol_repo = rol_repo.RolRepository()

def get_colaborador_details(colaborador_id: int) -> Colaborador:
    # Obtener datos básicos del colaborador.
    colaborador_data = colaborador_repo.get_by_id(colaborador_id)
    if not colaborador_data:
        raise ValueError("Colaborador no encontrado")
    
    # Obtener sucursales y roles asociados.
    colaborador_sucursales = colaborador_sucursal_repo.get_by_colaborador(colaborador_id)
    sucursales = [cs.sucursal_id for cs in colaborador_sucursales]
    roles = [rol_repo.get_by_id(cs.rol_colaborador_id) for cs in colaborador_sucursales]

    # Procesar horarios preferidos:
    horario_preferido_data = horario_preferido_colaborador_repo.get_by_colaborador(colaborador_id)
    horario_preferido: List[Tuple[int, object]] = []  # Se usará el modelo Horario
    for hp in horario_preferido_data:
        # Asignar la próxima fecha que corresponde al día indicado (hp.dia_id).
        fecha_asignada = get_next_date_for_dia(hp.dia_id)
        try:
            h = crear_horario(
                sucursal_id=0,  # Se usa 0 o un valor por defecto si no se asocia a una sucursal.
                colaborador_id=colaborador_id,
                dia_id=hp.dia_id,
                fecha=fecha_asignada,
                hora_inicio=hp.fecha_inicio,
                hora_fin=hp.fecha_fin,
                horario_corrido=hp.horario_corrido
            )
        except ValueError as e:
            raise ValueError(f"Error en horario preferido: {e}")
        horario_preferido.append((0, h))

    # Procesar horarios asignados:
    horario_asignado_data = horario_repo.get_by_colaborador(colaborador_id)
    horario_asignado: List[Tuple[int, object]] = []
    for ha in horario_asignado_data:
        try:
            h = crear_horario(
                sucursal_id=ha.sucursal_id,
                colaborador_id=colaborador_id,
                dia_id=ha.dia_id,
                fecha=ha.fecha,
                hora_inicio=ha.hora_inicio,
                hora_fin=ha.hora_fin,
                horario_corrido=ha.horario_corrido
            )
        except ValueError as e:
            raise ValueError(f"Error en horario asignado: {e}")
        horario_asignado.append((ha.sucursal_id, h))

    # Procesar horas extra.
    hs_extra_data = horas_extra_colaborador_repo.get_by_colaborador(colaborador_id)
    hs_extra: Dict[str, int] = {}
    for he in hs_extra_data:
        hs_extra[he.tipo] = hs_extra.get(he.tipo, 0) + he.cantidad

    # Procesar vacaciones.
    vacaciones_data = vacacion_colaborador_repo.get_by_colaborador(colaborador_id)
    vacaciones = [v.fecha for v in vacaciones_data]

    # Procesar tipo de empleado.
    tipo_empleado_data = tipo_colaborador_repo.get_by_id(colaborador_data.tipo_empleado_id)
    tipo_empleado = TipoEmpleado(
        id=tipo_empleado_data.id,
        tipo=tipo_empleado_data.tipo,
        horas_por_dia_max=tipo_empleado_data.horas_por_dia_max,
        horas_semanales=tipo_empleado_data.horas_semanales
    )

    # Días preferidos (puede obtenerse de otra tabla o definirse según la lógica de negocio).
    dias_preferidos: List[int] = []  

    # Construir y retornar la instancia del modelo Colaborador.
    return Colaborador(
        id=colaborador_data.id,
        nombre=colaborador_data.nombre,
        legajo=colaborador_data.legajo,
        email=colaborador_data.email,
        telefono=colaborador_data.telefono,
        dni=str(colaborador_data.dni),
        sucursales=sucursales,
        roles=[Rol(id=r.id, nombre=r.nombre, principal=r.principal) for r in roles],
        horario_preferido=horario_preferido,
        dias_preferidos=dias_preferidos,
        tipo_empleado=tipo_empleado,
        horario_asignado=horario_asignado,
        hs_extra=hs_extra,
        vacaciones=vacaciones,
        horario_corrido=colaborador_data.horario_corrido
    )
