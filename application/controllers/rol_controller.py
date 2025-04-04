from application.config.logger_config import setup_logger
from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from infrastructure.databases.models.rol import Rol
from infrastructure.repositories.rol_repo import RolRepository
from application.services.rol_service import get_available_roles_service

logger = setup_logger(__name__, "logs/rol.log")

def controlador_py_logger_get_by_id_rol(rol_id: int, db: Session) -> Rol:
    """
    Obtiene un Rol por su ID.
    """
    try:
        rol = RolRepository.get_by_id(rol_id, db)
    except Exception as error:
        logger.error("Error al obtener Rol con id %s: %s", rol_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    if not rol:
        logger.warning("Rol no encontrado con id %s", rol_id)
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

def controlador_py_logger_get_all_roles(db: Session) -> List[Rol]:
    """
    Obtiene todos los Roles.
    """
    try:
        roles = RolRepository.get_all(db)
    except Exception as error:
        logger.error("Error al obtener roles: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return roles

def controlador_py_logger_create_rol(rol: Rol, db: Session) -> Rol:
    """
    Crea un nuevo Rol en la base de datos.
    """
    try:
        nuevo_rol = RolRepository.create(rol, db)
        logger.info("Rol creado exitosamente con id %s", nuevo_rol.id)
        return nuevo_rol
    except Exception as error:
        logger.error("Error al crear Rol: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_update_rol(rol: Rol, db: Session) -> Rol:
    """
    Actualiza un Rol existente.
    """
    try:
        actualizado = RolRepository.update(rol, db)
    except Exception as error:
        logger.error("Error al actualizar Rol con id %s: %s", rol.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    if not actualizado:
        logger.warning("Rol no encontrado para actualizar con id %s", rol.id)
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    logger.info("Rol actualizado exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_py_logger_delete_rol(rol_id: int, db: Session) -> bool:
    """
    Elimina un Rol por su ID.
    """
    try:
        eliminado = RolRepository.delete(rol_id, db)
    except Exception as error:
        logger.error("Error al eliminar Rol con id %s: %s", rol_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    if not eliminado:
        logger.warning("Rol no encontrado para eliminar con id %s", rol_id)
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    logger.info("Rol eliminado exitosamente con id %s", rol_id)
    return eliminado

def controlador_py_logger_get_by_nombre_rol(nombre: str, db: Session) -> Rol:
    """
    Obtiene un Rol por su nombre.
    """
    try:
        rol = RolRepository.get_by_nombre(nombre, db)
    except Exception as error:
        logger.error("Error al obtener Rol por nombre '%s': %s", nombre, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    if not rol:
        logger.warning("Rol no encontrado con nombre '%s'", nombre)
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return rol

def controlador_py_logger_get_principales(db: Session) -> List[Rol]:
    """
    Obtiene todos los Roles marcados como 'principal=True'.
    """
    try:
        roles = RolRepository.get_principales(db)
    except Exception as error:
        logger.error("Error al obtener roles principales: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return roles

def controlador_get_available_roles(sucursal_id: int, db: Session):
    """
    Controlador que invoca el servicio para obtener los roles disponibles para una sucursal.
    
    Args:
        sucursal_id (int): ID de la sucursal.
    
    Returns:
        List[Rol]: Lista de roles disponibles.
    
    Raises:
        HTTPException: Con código 500 si ocurre un error interno.
    """
    try:
        roles = get_available_roles_service(sucursal_id, db)
        return roles
    except Exception as error:
        logger.error("Error en el controlador al obtener roles para la sucursal %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
