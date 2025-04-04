from application.config.logger_config import setup_logger
from typing import List, Optional
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from infrastructure.databases.models.horario_sucursal import HorarioSucursal
from infrastructure.repositories.horario_sucursal_repo import HorarioSucursalRepository

logger = setup_logger(__name__, "logs/horario_sucursal.log")

def controlador_py_logger_get_by_id_horario_sucursal(horario_id: int, db: Session) -> HorarioSucursal:
    """
    Obtiene un HorarioSucursal por su ID.
    """
    try:
        horario = HorarioSucursalRepository.get_by_id(horario_id, db)
    except Exception as error:
        logger.error("Error al obtener HorarioSucursal con id %s: %s", horario_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not horario:
        logger.warning("HorarioSucursal no encontrado con id %s", horario_id)
        raise HTTPException(status_code=404, detail="HorarioSucursal no encontrado")

    return horario

def controlador_py_logger_get_by_sucursal(sucursal_id: int, db: Session) -> List[HorarioSucursal]:
    """
    Obtiene todos los HorarioSucursal asociados a una Sucursal.
    """
    try:
        horarios = HorarioSucursalRepository.get_by_sucursal(sucursal_id, db)
        horarios = jsonable_encoder(horarios)
        return horarios
    except Exception as error:
        logger.error("Error al obtener HorarioSucursal para sucursal %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_get_by_dia(dia_id: int, db: Session) -> List[HorarioSucursal]:
    """
    Obtiene todos los HorarioSucursal para un día específico.
    """
    try:
        horarios = HorarioSucursalRepository.get_by_dia(dia_id, db)
    except Exception as error:
        logger.error("Error al obtener HorarioSucursal para día %s: %s", dia_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horarios

def controlador_py_logger_create_horario_sucursal(horario: HorarioSucursal, db: Session) -> HorarioSucursal:
    """
    Crea un nuevo HorarioSucursal en la base de datos.
    """
    try:
        nuevo = HorarioSucursalRepository.create(horario, db)
        logger.info("HorarioSucursal creado exitosamente con id %s", nuevo.id)
        return nuevo
    except Exception as error:
        logger.error("Error al crear HorarioSucursal: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_update_horario_sucursal(horario: HorarioSucursal, db: Session) -> HorarioSucursal:
    """
    Actualiza un HorarioSucursal existente.
    Retorna el objeto actualizado o levanta error si no existe.
    """
    try:
        existente = HorarioSucursalRepository.get_by_id(horario.id, db)
        if not existente:
            logger.warning("HorarioSucursal no encontrado para actualizar con id %s", horario.id)
            raise HTTPException(status_code=404, detail="HorarioSucursal no encontrado")
        
        actualizado = HorarioSucursalRepository.update(horario, db)
    except Exception as error:
        logger.error("Error al actualizar HorarioSucursal con id %s: %s", horario.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not actualizado:
        logger.warning("HorarioSucursal no encontrado tras actualización con id %s", horario.id)
        raise HTTPException(status_code=404, detail="HorarioSucursal no encontrado")
    
    logger.info("HorarioSucursal actualizado exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_py_logger_delete_horario_sucursal(horario_id: int, db: Session) -> bool:
    """
    Elimina un HorarioSucursal por su ID.
    """
    try:
        eliminado = HorarioSucursalRepository.delete(horario_id, db)
    except Exception as error:
        logger.error("Error al eliminar HorarioSucursal con id %s: %s", horario_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("HorarioSucursal no encontrado para eliminar con id %s", horario_id)
        raise HTTPException(status_code=404, detail="HorarioSucursal no encontrado")
    
    logger.info("HorarioSucursal eliminado exitosamente con id %s", horario_id)
    return eliminado
