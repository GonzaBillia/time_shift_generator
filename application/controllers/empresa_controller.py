from application.config.logger_config import setup_logger
from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from infrastructure.databases.models import Empresa
from infrastructure.repositories.empresas_repo import EmpresaRepository

logger = setup_logger(__name__, "logs/empresa.log")

def controlador_py_logger_get_by_id_empresa(empresa_id: int, db: Session) -> Empresa:
    """
    Obtiene una Empresa por su ID.
    """
    try:
        empresa = EmpresaRepository.get_by_id(empresa_id, db)
    except Exception as error:
        logger.error("Error al obtener Empresa con id %s: %s", empresa_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not empresa:
        logger.warning("Empresa no encontrada con id %s", empresa_id)
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    return empresa

def controlador_py_logger_get_by_cuit(cuit: str, db: Session) -> Empresa:
    """
    Obtiene una Empresa por su CUIT.
    """
    try:
        empresa = EmpresaRepository.get_by_cuit(cuit, db)
    except Exception as error:
        logger.error("Error al obtener empresa con CUIT %s: %s", cuit, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not empresa:
        logger.warning("Empresa no encontrada con CUIT %s", cuit)
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    return empresa

def controlador_py_logger_get_by_razon_social(razon_social: str, db: Session) -> Empresa:
    """
    Obtiene una Empresa por su razón social.
    """
    try:
        empresa = EmpresaRepository.get_by_razon_social(razon_social, db)
    except Exception as error:
        logger.error("Error al obtener empresa con razón social '%s': %s", razon_social, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not empresa:
        logger.warning("Empresa no encontrada con razón social '%s'", razon_social)
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    return empresa

def controlador_py_logger_get_all_empresas(db: Session) -> List[Empresa]:
    """
    Obtiene todas las Empresas.
    """
    try:
        empresas = EmpresaRepository.get_all(db)
    except Exception as error:
        logger.error("Error al obtener todas las empresas: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    return empresas

def controlador_py_logger_create_empresa(empresa: Empresa, db: Session) -> Empresa:
    """
    Crea una nueva Empresa en la base de datos.
    """
    try:
        empresa_creada = EmpresaRepository.create(empresa, db)
        logger.info("Empresa creada exitosamente con id %s", empresa_creada.id)
        return empresa_creada
    except Exception as error:
        logger.error("Error al crear la empresa: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    
def controlador_py_logger_update_empresa(empresa: Empresa, db: Session) -> Empresa:
    """
    Actualiza una Empresa existente en la base de datos.
    """
    try:
        empresa_actualizada = EmpresaRepository.update(empresa, db)
    except Exception as error:
        logger.error("Error al actualizar empresa con id %s: %s", empresa.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not empresa_actualizada:
        logger.warning("Empresa no encontrada para actualizar con id %s", empresa.id)
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    logger.info("Empresa actualizada exitosamente con id %s", empresa_actualizada.id)
    return empresa_actualizada

def controlador_py_logger_delete_empresa(empresa_id: int, db: Session) -> bool:
    """
    Elimina una Empresa por su ID.
    """
    try:
        resultado = EmpresaRepository.delete(empresa_id, db)
    except Exception as error:
        logger.error("Error al eliminar empresa con id %s: %s", empresa_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not resultado:
        logger.warning("Empresa no encontrada para eliminar con id %s", empresa_id)
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    logger.info("Empresa eliminada exitosamente con id %s", empresa_id)
    return resultado
