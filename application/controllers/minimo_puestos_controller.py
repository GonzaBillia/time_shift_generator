from typing import List
from datetime import time
from fastapi import HTTPException
from infrastructure.databases.models.minimo_puestos_requeridos import MinimoPuestosRequeridos
from infrastructure.repositories.minimo_puestos_requeridos_repo import MinimoPuestosRequeridosRepository
from application.config.logger_config import setup_logger
from sqlalchemy.orm import Session

logger = setup_logger(__name__, "logs/minimo_puestos.log")

def controlador_py_logger_get_by_sucursal_minimo(sucursal_id: int, db: Session) -> List[MinimoPuestosRequeridos]:
    """
    Obtiene todos los registros de mínimos de puestos requeridos para una sucursal.
    """
    try:
        minimos = MinimoPuestosRequeridosRepository.get_by_sucursal(sucursal_id, db)
    except Exception as error:
        logger.error("Error al obtener mínimos para sucursal %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return minimos

def controlador_py_logger_get_by_rol_minimo(sucursal_id: int, rol_colaborador_id: int, db: Session) -> List[MinimoPuestosRequeridos]:
    """
    Obtiene los registros de mínimos de puestos para una sucursal y rol específico.
    """
    try:
        minimos = MinimoPuestosRequeridosRepository.get_by_rol(sucursal_id, rol_colaborador_id, db)
    except Exception as error:
        logger.error("Error al obtener mínimos para sucursal %s y rol %s: %s", sucursal_id, rol_colaborador_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return minimos

def controlador_py_logger_get_by_horario_minimo(sucursal_id: int, dia_id: int, hora: time, db: Session) -> MinimoPuestosRequeridos:
    """
    Obtiene el mínimo de puestos requeridos para una sucursal en un día y hora específicos.
    """
    try:
        minimo = MinimoPuestosRequeridosRepository.get_by_horario(sucursal_id, dia_id, hora, db)
    except Exception as error:
        logger.error("Error al obtener mínimo para sucursal %s, día %s y hora %s: %s", 
                     sucursal_id, dia_id, hora, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not minimo:
        logger.warning("No se encontró mínimo para sucursal %s, día %s y hora %s", sucursal_id, dia_id, hora)
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return minimo

def controlador_py_logger_create_minimo(minimo: MinimoPuestosRequeridos, db: Session) -> MinimoPuestosRequeridos:
    """
    Crea un nuevo registro de mínimos de puestos requeridos.
    """
    try:
        nuevo = MinimoPuestosRequeridosRepository.create(minimo, db)
        logger.info("Mínimo de puestos creado exitosamente con id %s", nuevo.id)
        return nuevo
    except Exception as error:
        logger.error("Error al crear mínimo de puestos: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_update_minimo(minimo: MinimoPuestosRequeridos, db: Session) -> MinimoPuestosRequeridos:
    """
    Actualiza un registro de mínimos de puestos requeridos.
    """
    try:
        # Se puede comprobar la existencia usando otro criterio si fuera necesario.
        actualizado = MinimoPuestosRequeridosRepository.update(minimo, db)
    except Exception as error:
        logger.error("Error al actualizar mínimo de puestos con id %s: %s", minimo.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not actualizado:
        logger.warning("Mínimo de puestos no encontrado para actualizar con id %s", minimo.id)
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    logger.info("Mínimo de puestos actualizado exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_py_logger_delete_minimo(minimo_id: int, db: Session) -> bool:
    """
    Elimina un registro de mínimos de puestos requeridos por su ID.
    """
    try:
        eliminado = MinimoPuestosRequeridosRepository.delete(minimo_id, db)
    except Exception as error:
        logger.error("Error al eliminar mínimo de puestos con id %s: %s", minimo_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("Mínimo de puestos no encontrado para eliminar con id %s", minimo_id)
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    logger.info("Mínimo de puestos eliminado exitosamente con id %s", minimo_id)
    return eliminado
