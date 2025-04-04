from datetime import date, time
from fastapi import HTTPException, status
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from infrastructure.repositories import (
    colaborador_repo,
    colaborador_sucursal_repo,
    horario_preferido_colaborador_repo,
    empresas_repo,
    horario_repo,
    horas_extra_colaborador_repo,
    vacacion_colaborador_repo,
    tipo_colaborador_repo,
    rol_repo,
    puesto_repo
)
from application.controllers.sucursal_controller import controlador_py_logger_get_by_id_sucursal
from infrastructure.schemas.colaborador import ColaboradorBase
from infrastructure.schemas.colaborador_details import ColaboradorFullUpdate
from infrastructure.schemas.colaborador_sucursal import ColaboradorSucursalBase
from infrastructure.schemas.horario_preferido_colaborador import HorarioPreferidoColaboradorBase
from infrastructure.schemas.horario_preferido_colaborador import HorarioPreferidoColaboradorResponse

from domain.models.colaborador import Colaborador
from domain.models.tipo_colaborador import TipoEmpleado
from domain.models.rol import Rol
from application.services.horario_service import crear_horario_preferido

colaborador_repo = colaborador_repo.ColaboradorRepository()
colaborador_sucursal_repo = colaborador_sucursal_repo.ColaboradorSucursalRepository()
horario_preferido_colaborador_repo = horario_preferido_colaborador_repo.HorarioPreferidoColaboradorRepository()
horario_repo = horario_repo.HorarioRepository()
horas_extra_colaborador_repo = horas_extra_colaborador_repo.HorasExtraColaboradorRepository()
vacacion_colaborador_repo = vacacion_colaborador_repo.VacacionColaboradorRepository()
tipo_colaborador_repo = tipo_colaborador_repo.TipoEmpleadoRepository()
rol_repo = rol_repo.RolRepository()
puesto_repo = puesto_repo.PuestoRepository()
empresas_repo = empresas_repo.EmpresaRepository()

# Configuración del logger
from application.config.logger_config import setup_logger
logger = setup_logger(__name__)

def get_colaborador_details(colaborador_id: int, db: Session) -> Colaborador:
    # Obtener datos básicos del colaborador.
    colaborador_data = colaborador_repo.get_by_id(colaborador_id, db)
    if not colaborador_data:
        raise ValueError("Colaborador no encontrado")
    
    # Obtener sucursales y roles asociados.
    colaborador_sucursales = colaborador_sucursal_repo.get_by_colaborador(colaborador_id, db)
    sucursales = [controlador_py_logger_get_by_id_sucursal(cs.sucursal_id, db) for cs in colaborador_sucursales]
    roles = [rol_repo.get_by_id(cs.rol_colaborador_id, db) for cs in colaborador_sucursales]
    empresa = empresas_repo.get_by_id(colaborador_data.empresa_id, db)

    # --- Procesar horarios preferidos ---
    horario_preferido_data = horario_preferido_colaborador_repo.get_by_colaborador(colaborador_id, db)
    # Se construye una lista de HorarioPreferidoColaboradorResponse
    horario_preferido_response: List[HorarioPreferidoColaboradorResponse] = []
    for hp in horario_preferido_data:
        try:
            # Crear el objeto Horario para el horario preferido (sin fecha)
            h = crear_horario_preferido(
                sucursal_id=hp.sucursal_id,  # Usar el valor real de la DB
                colaborador_id=colaborador_id,
                dia_id=hp.dia_id,
                hora_inicio=hp.hora_inicio,
                hora_fin=hp.hora_fin,
                horario_corrido=hp.horario_corrido
            )
            # Extraer el primer bloque y construir el diccionario requerido.
            hora_inicio_obj, hora_fin_obj = h.bloques[0]
            h_dict = {
                "id": hp.id,
                "colaborador_id": h.colaborador_id,
                "sucursal_id": h.sucursal_id,
                "hora_inicio": hora_inicio_obj.isoformat() if hasattr(hora_inicio_obj, "isoformat") else hora_inicio_obj,
                "hora_fin": hora_fin_obj.isoformat() if hasattr(hora_fin_obj, "isoformat") else hora_fin_obj,
                "dia_id": h.dia_id,
                "horario_corrido": h.horario_corrido,
            }
            # Validar y transformar el diccionario al modelo de respuesta.
            h_response = HorarioPreferidoColaboradorResponse.model_validate(h_dict)
        except ValueError as e:
            raise ValueError(f"Error en horario preferido: {e}")
        horario_preferido_response.append(h_response)
    
    # Generar la lista de días preferidos a partir de los horarios preferidos
    dias_preferidos = [hp.dia_id for hp in horario_preferido_response]
    
    # --- Procesar horas extra ---
    hs_extra_data = horas_extra_colaborador_repo.get_by_colaborador(colaborador_id, db)
    hs_extra: Dict[str, int] = {}
    for he in hs_extra_data:
        hs_extra[he.tipo] = hs_extra.get(he.tipo, 0) + he.cantidad

    # --- Procesar vacaciones ---
    vacaciones_data = vacacion_colaborador_repo.get_by_colaborador(colaborador_id, db)
    vacaciones = [v.fecha for v in vacaciones_data]

    # --- Procesar tipo de empleado ---
    tipo_empleado_data = tipo_colaborador_repo.get_by_id(colaborador_data.tipo_empleado_id, db)
    tipo_empleado = TipoEmpleado(
        id=tipo_empleado_data.id,
        tipo=tipo_empleado_data.tipo,
        horas_por_dia_max=tipo_empleado_data.horas_por_dia_max,
        horas_semanales=tipo_empleado_data.horas_semanales
    )

    # Construir y retornar la instancia del modelo Colaborador (dominio).
    return Colaborador(
        id=colaborador_data.id,
        nombre=colaborador_data.nombre,
        legajo=colaborador_data.legajo,
        email=colaborador_data.email,
        telefono=colaborador_data.telefono,
        dni=str(colaborador_data.dni),
        empresa=empresa,
        sucursales=sucursales,
        roles=[Rol(id=r.id, nombre=r.nombre, principal=r.principal) for r in roles if r],
        horario_preferido=horario_preferido_response,  # Lista de HorarioPreferidoColaboradorResponse
        dias_preferidos=dias_preferidos,
        horario_asignado=None,
        tipo_empleado=tipo_empleado,
        hs_extra=hs_extra,
        vacaciones=vacaciones,
        horario_corrido=colaborador_data.horario_corrido
    )

def default_custom_encoder(obj):
    if isinstance(obj, time):
        return obj.isoformat()
    if isinstance(obj, tuple):
        return list(obj)
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def convertir_recursivamente(obj):
    """
    Recorre recursivamente la estructura de datos para convertir:
      - time -> isoformat()
      - tuple -> list (u otra estructura serializable)
    """
    if isinstance(obj, dict):
        return {k: convertir_recursivamente(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_recursivamente(item) for item in obj]
    elif isinstance(obj, tuple):
        return [convertir_recursivamente(item) for item in obj]
    elif isinstance(obj, time):
        return obj.isoformat()
    else:
        return obj

def obtener_horarios_asignados(colaborador_id: int, fecha_desde: date, fecha_hasta: date, db: Optional[Session] = None):
    """
    Retorna los puestos asignados a un colaborador en un rango de fechas, incluyendo para cada puesto 
    la lista de horarios asociados.
    """
    # Validar que el colaborador exista
    colaborador = colaborador_repo.get_by_id(colaborador_id, db)
    if not colaborador:
        raise Exception("El colaborador no existe.")

    # Obtener puestos asignados en el rango de fechas
    puestos = puesto_repo.get_by_colaborador_date(colaborador_id, fecha_desde, fecha_hasta, db)
    if not puestos:
        return []  # O se puede retornar un mensaje indicando que no hay puestos asignados

    # Obtener los IDs de los puestos
    puestos_ids = [puesto.id for puesto in puestos]

    # Obtener los horarios asociados a esos puestos
    horarios = horario_repo.get_by_puestos(puestos_ids, db)

    # Agrupar los horarios por puesto_id
    horarios_grouped = {}
    for horario in horarios:
        horario_dict = {
            "id": horario.id,
            "puesto_id": horario.puesto_id,
            "hora_inicio": horario.hora_inicio.strftime("%H:%M:%S"),
            "hora_fin": horario.hora_fin.strftime("%H:%M:%S"),
            "horario_corrido": horario.horario_corrido
        }
        if horario.puesto_id not in horarios_grouped:
            horarios_grouped[horario.puesto_id] = []
        horarios_grouped[horario.puesto_id].append(horario_dict)

    # Formatear la respuesta: cada puesto incluye sus horarios correspondientes
    respuesta = []
    for puesto in puestos:
        puesto_dict = {
            "id": puesto.id,
            "fecha": puesto.fecha.isoformat() if puesto.fecha else None,
            "nombre": puesto.nombre,
            "dia_id": puesto.dia_id,
            "horarios": horarios_grouped.get(puesto.id, [])
        }
        respuesta.append(puesto_dict)

    return respuesta

def update_full_colaborador_service(
    colaborador_id: int, 
    colaborador_full_update: ColaboradorFullUpdate,  # Tipo: ColaboradorFullUpdate
    db: Session
):
    """
    Actualiza completamente un colaborador, incluyendo:
      - Datos básicos.
      - Horarios preferidos (actualizar, crear o eliminar).
      - Relaciones colaborador_sucursal (actualizar, crear o eliminar).
    Toda la operación se ejecuta en una transacción.
    """
    with db.begin():
        # Recuperar el colaborador actual
        colaborador_actual = colaborador_repo.get_by_id(colaborador_id, db)
        if not colaborador_actual:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Colaborador no encontrado")
        
        # Actualizar los datos básicos
        update_data = colaborador_full_update.colaborador.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(colaborador_actual, key, value)
        
        # 1. Actualizar los horarios preferidos
        current_horarios = horario_preferido_colaborador_repo.get_by_colaborador(colaborador_actual.id, db)
        current_horario_ids = {h.id for h in current_horarios if h.id is not None}
        payload_horario_ids = {h.id for h in colaborador_full_update.horario_preferido if h.id}
        
        # Eliminar horarios que ya no vienen en el payload
        to_delete_horarios = current_horario_ids - payload_horario_ids
        for del_id in to_delete_horarios:
            horario_preferido_colaborador_repo.delete(del_id, db)
        
        # Procesar cada horario preferido enviado
        for horario_data in colaborador_full_update.horario_preferido:
            if horario_data.id:  # Si se envía un id, se intenta actualizar
                horario_actual = horario_preferido_colaborador_repo.get_by_id(horario_data.id, db)
                if horario_actual:
                    update_horario = horario_data.model_dump(exclude_unset=True)
                    for key, value in update_horario.items():
                        setattr(horario_actual, key, value)
                    horario_preferido_colaborador_repo.update(horario_actual, db)
                else:
                    nuevo_horario = HorarioPreferidoColaboradorBase(**horario_data.model_dump())
                    horario_preferido_colaborador_repo.create(nuevo_horario, db)
            else:
                nuevo_horario = HorarioPreferidoColaboradorBase(**horario_data.model_dump())
                horario_preferido_colaborador_repo.create(nuevo_horario, db)
        
        # 2. Actualizar las relaciones colaborador_sucursal
        if colaborador_full_update.colaboradorSucursales is not None:
            payload_relaciones = {(rel.rol_colaborador_id, rel.sucursal_id) for rel in colaborador_full_update.colaboradorSucursales}
            relaciones_actuales = colaborador_sucursal_repo.get_by_colaborador(colaborador_actual.id, db)
            current_set = {(rel.rol_colaborador_id, rel.sucursal_id) for rel in relaciones_actuales}
            relaciones_to_delete = current_set - payload_relaciones
            for rel in relaciones_actuales:
                if (rel.rol_colaborador_id, rel.sucursal_id) in relaciones_to_delete:
                    colaborador_sucursal_repo.delete(rel.id, db)
            relaciones_to_add = payload_relaciones - current_set
            for role_id, sucursal_id in relaciones_to_add:
                nueva_relacion_data = ColaboradorSucursalBase(
                    colaborador_id=colaborador_actual.id,
                    rol_colaborador_id=role_id,
                    sucursal_id=sucursal_id
                )
                colaborador_sucursal_repo.create(nueva_relacion_data, db)
        
        # 3. Actualizar el colaborador en la BD
        actualizado = colaborador_repo.update(colaborador_actual, db)
        return actualizado
