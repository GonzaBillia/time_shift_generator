from application.config.logger_config import setup_logger
from typing import List, Optional
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from infrastructure.databases.models.formato_rol import FormatosRoles
from infrastructure.databases.models.rol import Rol
from infrastructure.repositories.formatos_roles_repo import FormatosRolesRepository

logger = setup_logger(__name__, "logs/formato_rol.log")

def controlador_py_logger_get_by_ids(rol_colaborador_id: int, formato_id: int, db: Session) -> FormatosRoles:
    """
    Obtiene un registro de FormatosRoles por su clave compuesta.
    """
    try:
        mapping = FormatosRolesRepository.get_by_ids(rol_colaborador_id, formato_id, db)
    except Exception as error:
        logger.error("Error al obtener FormatosRoles para rol %s y formato %s: %s", rol_colaborador_id, formato_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not mapping:
        logger.warning("FormatosRoles no encontrado para rol %s y formato %s", rol_colaborador_id, formato_id)
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    return mapping

def controlador_py_logger_get_all_formatos_roles(db: Session) -> List[FormatosRoles]:
    """
    Obtiene todos los registros de FormatosRoles.
    """
    try:
        mappings = FormatosRolesRepository.get_all(db)
    except Exception as error:
        logger.error("Error al obtener todos los registros de FormatosRoles: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    return mappings

def controlador_py_logger_get_by_formatos(formato_id: int, db: Session) -> List[FormatosRoles]:
    """
    Obtiene todos los registros de FormatosRoles para un Formato dado.
    """
    try:
        mappings = FormatosRolesRepository.get_by_formatos(formato_id, db)
    except Exception as error:
        logger.error("Error al obtener los registros de FormatosRoles para formato %s: %s", formato_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    return mappings

def controlador_py_logger_get_roles_by_formato(formato_id: int, db: Session) -> List[Rol]:
    """
    Obtiene todos los Roles asociados a un Formato.
    """
    try:
        roles = FormatosRolesRepository.get_roles_by_formato(formato_id, db)
        # Convertir a un formato serializable (lista de diccionarios)
        roles_serialized = jsonable_encoder(roles)
        return roles_serialized
    except Exception as error:
        logger.error("Error al obtener roles para FormatosRoles para formato %s: %s", formato_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_create_formatos_roles(mapping: FormatosRoles, db: Session) -> FormatosRoles:
    """
    Crea un nuevo registro en FormatosRoles.
    """
    try:
        nuevo_mapping = FormatosRolesRepository.create(mapping, db)
        logger.info("Registro de FormatosRoles creado exitosamente: rol %s, formato %s", nuevo_mapping.rol_colaborador_id, nuevo_mapping.formato_id)
        return nuevo_mapping
    except Exception as error:
        logger.error("Error al crear registro en FormatosRoles: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_delete_formatos_roles(rol_colaborador_id: int, formato_id: int, db: Session) -> bool:
    """
    Elimina un registro de FormatosRoles por su clave compuesta.
    """
    try:
        eliminado = FormatosRolesRepository.delete(rol_colaborador_id, formato_id, db)
    except Exception as error:
        logger.error("Error al eliminar FormatosRoles para rol %s y formato %s: %s", rol_colaborador_id, formato_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("Registro de FormatosRoles no encontrado para rol %s y formato %s", rol_colaborador_id, formato_id)
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    logger.info("Registro de FormatosRoles eliminado exitosamente para rol %s y formato %s", rol_colaborador_id, formato_id)
    return eliminado
