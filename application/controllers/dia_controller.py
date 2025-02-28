# CONTROLLER_PY_LOGGER_DIA
from application.config.logger_config import setup_logger
from typing import List, Optional
from fastapi import HTTPException
from infrastructure.databases.models.dia import Dia
from infrastructure.repositories.dia_repo import DiaRepository

logger = setup_logger(__name__, "logs/dia.log")

def controlador_py_logger_get_by_id_dia(dia_id: int) -> Dia:
    """
    Obtiene un Día por su ID.
    """
    try:
        dia = DiaRepository.get_by_id(dia_id)
    except Exception as error:
        logger.error("Error al obtener Día con id %s: %s", dia_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not dia:
        logger.warning("Día no encontrado con id %s", dia_id)
        raise HTTPException(status_code=404, detail="Día no encontrado")

    return dia

def controlador_py_logger_get_by_nombre_dia(nombre: str) -> Dia:
    """
    Obtiene un Día por su nombre.
    """
    try:
        dia = DiaRepository.get_by_nombre(nombre)
    except Exception as error:
        logger.error("Error al obtener Día con nombre %s: %s", nombre, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not dia:
        logger.warning("Día no encontrado con nombre %s", nombre)
        raise HTTPException(status_code=404, detail="Día no encontrado")

    return dia

def controlador_py_logger_get_all_dias() -> List[Dia]:
    """
    Obtiene todos los Días.
    """
    try:
        dias = DiaRepository.get_all()
    except Exception as error:
        logger.error("Error al obtener todos los Días: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    return dias

def controlador_py_logger_create_dia(dia: Dia) -> Dia:
    """
    Crea un nuevo Día en la base de datos.
    """
    try:
        dia_creado = DiaRepository.create(dia)
        logger.info("Día creado exitosamente con id %s", dia_creado.id)
        return dia_creado
    except Exception as error:
        logger.error("Error al crear Día: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_update_dia(dia: Dia) -> Dia:
    """
    Actualiza un Día existente en la base de datos.
    """
    try:
        dia_actualizado = DiaRepository.update(dia)
    except Exception as error:
        logger.error("Error al actualizar Día con id %s: %s", dia.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not dia_actualizado:
        logger.warning("Día no encontrado para actualizar con id %s", dia.id)
        raise HTTPException(status_code=404, detail="Día no encontrado")

    logger.info("Día actualizado exitosamente con id %s", dia_actualizado.id)
    return dia_actualizado

def controlador_py_logger_delete_dia(dia_id: int) -> bool:
    """
    Elimina un Día por su ID.
    """
    try:
        resultado = DiaRepository.delete(dia_id)
    except Exception as error:
        logger.error("Error al eliminar Día con id %s: %s", dia_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not resultado:
        logger.warning("Día no encontrado para eliminar con id %s", dia_id)
        raise HTTPException(status_code=404, detail="Día no encontrado")

    logger.info("Día eliminado exitosamente con id %s", dia_id)
    return resultado
