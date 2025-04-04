from fastapi import HTTPException
from typing import List, Optional
import logging
from sqlalchemy.orm import Session
from application.services.puestos_service import (
    crear_puesto, 
    actualizar_puesto, 
    actualizar_varios_puestos, 
    delete_multiple_puestos, 
    create_multiple_puestos, 
    obtener_puestos_por_sucursal
)
from infrastructure.schemas.puestos import PuestoBase, PuestoUpdate, PuestoResponse
from infrastructure.databases.models.puestos import Puesto
from infrastructure.repositories.horario_repo import HorarioRepository

# Servicio y esquema para la copia histórica
from application.services.copy_historial_service import copy_history_service
from infrastructure.schemas.hostorial import CopyHistoryRequest

logger = logging.getLogger(__name__)

def controlador_py_logger_crear_puesto(puesto_data: dict, db: Session) -> PuestoResponse:
    """
    Crea un puesto nuevo utilizando la lógica del servicio.
    Se espera que 'puesto_data' contenga: sucursal_id, rol_colaborador_id, dia_id, fecha, nombre y opcionalmente colaborador_id.
    """
    try:
        puesto = crear_puesto(
            sucursal_id=puesto_data["sucursal_id"],
            rol_colaborador_id=puesto_data["rol_colaborador_id"],
            dia_id=puesto_data["dia_id"],
            fecha=puesto_data["fecha"],
            nombre=puesto_data["nombre"],
            colaborador_id=puesto_data.get("colaborador_id"),
            db=db
        )
        logger.info("Puesto creado exitosamente con id %s", puesto.id)
        return puesto
    except Exception as error:
        logger.error("Error al crear puesto: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_crear_varios_puestos(puestos_data: List[dict], db: Session) -> List[PuestoResponse]:
    """
    Crea múltiples puestos utilizando la lógica del servicio.
    Se espera que cada diccionario en 'puestos_data' contenga: 
      sucursal_id, rol_colaborador_id, dia_id, fecha, nombre y opcionalmente colaborador_id.
    """
    try:
        # Convertir cada diccionario a una instancia del modelo Puesto.
        puesto_objs = [Puesto(**p) for p in puestos_data]
        puestos = create_multiple_puestos(puesto_objs, db)
        logger.info("Se crearon %d puestos exitosamente", len(puestos))
        return puestos
    except Exception as error:
        logger.error("Error al crear múltiples puestos: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_actualizar_puesto(puesto_data: dict, db: Session) -> PuestoResponse:
    """
    Actualiza un puesto existente. Se espera que 'puesto_data' contenga el 'id' y los campos a modificar.
    """
    try:
        puesto = actualizar_puesto(puesto_data, db)
        logger.info("Puesto actualizado exitosamente con id %s", puesto.id)
        return puesto
    except Exception as error:
        logger.error("Error al actualizar puesto: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_actualizar_varios_puestos(puestos_data: List[dict], db: Session) -> List[PuestoResponse]:
    """
    Actualiza varios puestos existentes. Se espera que cada diccionario en 'puestos_data'
    contenga el 'id' y los campos a modificar.
    """
    try:
        puestos_actualizados = actualizar_varios_puestos(puestos_data, db)
        logger.info("Puestos actualizados exitosamente con ids: %s", [puesto.id for puesto in puestos_actualizados])
        return puestos_actualizados
    except Exception as error:
        logger.error("Error al actualizar los puestos: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_obtener_puestos(sucursal_id: int, db: Session) -> List[PuestoResponse]:
    """
    Retorna la lista de puestos de una sucursal.
    """
    try:
        puestos = obtener_puestos_por_sucursal(sucursal_id, db)
        logger.info("Se obtuvieron %d puestos para sucursal %s", len(puestos), sucursal_id)
        return puestos
    except Exception as error:
        logger.error("Error al obtener puestos: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_eliminar_varios_puestos(puesto_ids: List[int], db: Session) -> None:
    """
    Elimina múltiples puestos y, previamente, elimina los horarios asociados a cada puesto.
    Se espera una lista de IDs de puestos.
    """
    try:
        # Recopilar los IDs de todos los horarios asociados a los puestos a eliminar.
        all_horario_ids = []
        for puesto_id in puesto_ids:
            horarios = HorarioRepository.get_by_puesto(puesto_id, db)
            all_horario_ids.extend([horario.id for horario in horarios])
        
        # Si se encontraron horarios asociados, eliminarlos.
        if all_horario_ids:
            deleted = HorarioRepository.delete_many(all_horario_ids, db)
            logger.info("Se eliminaron %d horarios asociados", len(all_horario_ids))
        else:
            logger.info("No se encontraron horarios asociados a eliminar.")
        
        # Eliminar los puestos.
        delete_multiple_puestos(puesto_ids, db)
        logger.info("Se eliminaron %d puestos", len(puesto_ids))
    except Exception as error:
        logger.error("Error al eliminar puestos y horarios: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_copy_history(copy_history_data: dict, db: Session) -> dict:
    """
    Realiza la copia histórica de puestos y horarios.
    Se espera que 'copy_history_data' contenga:
      - sucursal_id
      - origin_week: {start: date, end: date}
      - destination_weeks: List[{start: date, end: date}]
      - resources: List de puestos (con su id original)
      - events: List de horarios (con su puesto_id original)
    Este controlador llama al servicio copy_history_service, que se encarga de crear las copias
    de forma transaccional, generando nuevos puestos y asociando los eventos correspondientes.
    """
    try:
        request_obj = CopyHistoryRequest.model_validate(copy_history_data)
        result = copy_history_service(request_obj, db)
        num_puestos = len(result.get("puestos", []))
        num_horarios = len(result.get("horarios", []))
        logger.info("Copia histórica completada: %d puestos y %d horarios creados", num_puestos, num_horarios)
        return result
    except Exception as error:
        logger.error("Error en copia histórica: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
