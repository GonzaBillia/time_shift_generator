from datetime import timedelta
from sqlalchemy.orm import Session
from typing import Dict, Tuple, List
from infrastructure.databases.models.puestos import Puesto
from infrastructure.databases.models.horario import Horario
from infrastructure.schemas.hostorial import CopyHistoryRequest
from infrastructure.repositories.puesto_repo import PuestoRepository
from infrastructure.repositories.horario_repo import HorarioRepository

def copy_history_service(request: CopyHistoryRequest, db: Session):
    # Mapeo para relacionar: clave = (original_resource.id, dest_week.start.isoformat()) -> new_resource.id
    resource_mapping: Dict[Tuple[int, str], int] = {}
    new_puestos_batch: List[Puesto] = []
    
    # Para cada semana destino se crea la copia de todos los recursos de la semana origen
    for dest in request.destination_weeks:
        # Calculamos la diferencia en semanas (suponiendo que ambas fechas son lunes)
        diff = (dest.start - request.origin_week.start).days // 7
        for resource in request.resources:
            new_fecha = resource.fecha + timedelta(weeks=diff)
            new_puesto = Puesto(
                sucursal_id=request.sucursal_id,
                rol_colaborador_id=resource.rol_colaborador_id,
                dia_id=resource.dia_id,
                fecha=new_fecha,
                nombre=f"{resource.nombre}",
                colaborador_id=resource.colaborador_id
            )
            new_puestos_batch.append(new_puesto)
            # Inicialmente, la clave se asocia a None; se actualizará tras guardar
            resource_mapping[(resource.id, dest.start.isoformat())] = None

    # Crear en batch los nuevos puestos usando el repositorio y la sesión explícita
    try:
        created_puestos = PuestoRepository.create_many(new_puestos_batch, db)
    except Exception as e:
        db.rollback()
        raise e

    # Construir el mapeo: se asume que el orden de created_puestos corresponde a:
    #   [dest1: resource1, resource2, ...; dest2: resource1, resource2, ...; ...]
    index = 0
    for dest in request.destination_weeks:
        for resource in request.resources:
            key = (resource.id, dest.start.isoformat())
            resource_mapping[key] = created_puestos[index].id
            index += 1

    # Procesar la copia de eventos
    new_horarios_batch: List[Horario] = []
    for dest in request.destination_weeks:
        diff = (dest.start - request.origin_week.start).days // 7
        for event in request.events:
            # Utilizar el ID original del puesto para formar la clave de mapeo
            key = (event.puesto_id, dest.start.isoformat())
            new_puesto_id = resource_mapping.get(key)
            if new_puesto_id is None:
                # Si no se encuentra el recurso copiado, se puede omitir o registrar un error
                continue
            # Ajustar, si fuera necesario, las fechas del evento. En este ejemplo asumimos que no cambian.
            new_event = Horario(
                puesto_id=new_puesto_id,
                hora_inicio=event.hora_inicio,
                hora_fin=event.hora_fin,
                horario_corrido=event.horario_corrido
            )
            new_horarios_batch.append(new_event)

    try:
        # Crear en batch los nuevos eventos usando el repositorio y la sesión explícita
        created_horarios = HorarioRepository.bulk_crear_horarios_session(new_horarios_batch, db)
    except Exception as e:
        db.rollback()
        raise e

    db.commit()
    return {"puestos": created_puestos, "horarios": created_horarios}
