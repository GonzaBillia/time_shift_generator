from application.config.logger_config import setup_logger
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from infrastructure.databases.models.formato import Formato
from infrastructure.repositories.formato_repo import FormatoRepository

logger = setup_logger(__name__, "logs/formato.log")

def controlador_py_logger_get_by_id_formato(formato_id: int, db: Session) -> Formato:
    """
    Obtiene un Formato por su ID.
    """
    try:
        formato = FormatoRepository.get_by_id(formato_id, db)
    except Exception as error:
        logger.error("Error al obtener Formato con id %s: %s", formato_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    if not formato:
        logger.warning("Formato no encontrado con id %s", formato_id)
        raise HTTPException(status_code=404, detail="Formato no encontrado")
    return formato

def controlador_py_logger_get_all_formatos(db: Session) -> List[Formato]:
    """
    Obtiene todos los Formatos.
    """
    try:
        formatos = FormatoRepository.get_all(db)
    except Exception as error:
        logger.error("Error al obtener todos los Formatos: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return formatos

def controlador_py_logger_create_formato(formato: Formato, db: Session) -> Formato:
    """
    Crea un nuevo Formato.
    """
    try:
        nuevo_formato = FormatoRepository.create(formato, db)
        logger.info("Formato creado exitosamente con id %s", nuevo_formato.id)
        return nuevo_formato
    except Exception as error:
        logger.error("Error al crear Formato: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_update_formato(formato: Formato, db: Session) -> Formato:
    """
    Actualiza un Formato existente.
    """
    try:
        actualizado = FormatoRepository.update(formato, db)
    except Exception as error:
        logger.error("Error al actualizar Formato con id %s: %s", formato.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    if not actualizado:
        logger.warning("Formato no encontrado para actualizar con id %s", formato.id)
        raise HTTPException(status_code=404, detail="Formato no encontrado")
    logger.info("Formato actualizado exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_py_logger_delete_formato(formato_id: int, db: Session) -> bool:
    """
    Elimina un Formato por su ID.
    """
    try:
        eliminado = FormatoRepository.delete(formato_id, db)
    except Exception as error:
        logger.error("Error al eliminar Formato con id %s: %s", formato_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    if not eliminado:
        logger.warning("Formato no encontrado para eliminar con id %s", formato_id)
        raise HTTPException(status_code=404, detail="Formato no encontrado")
    logger.info("Formato eliminado exitosamente con id %s", formato_id)
    return eliminado

def controlador_py_logger_get_by_nombre_formato(nombre: str, db: Session) -> Formato:
    """
    Obtiene un Formato por su nombre.
    """
    try:
        formato = FormatoRepository.get_by_nombre(nombre, db)
    except Exception as error:
        logger.error("Error al obtener Formato con nombre '%s': %s", nombre, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    if not formato:
        logger.warning("Formato no encontrado con nombre '%s'", nombre)
        raise HTTPException(status_code=404, detail="Formato no encontrado")
    return formato

def controlador_py_logger_get_roles_by_formato(formato_id: int, db: Session) -> List:
    """
    Obtiene la lista de roles asociados a un Formato.
    """
    try:
        roles = FormatoRepository.get_roles_by_formato(formato_id, db)
    except Exception as error:
        logger.error("Error al obtener roles para Formato con id %s: %s", formato_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return roles
