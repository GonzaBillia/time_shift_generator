from application.config.logger_config import setup_logger
from typing import Optional, List
from fastapi import HTTPException
from infrastructure.databases.models import Empresa
from infrastructure.repositories.empresas_repo import EmpresaRepository

logger = setup_logger(__name__, "logs/empresa.log")

def controlador_py_logger_get_by_id_empresa(empresa_id: int) -> Empresa:
    """
    Obtiene una Empresa por su ID.

    Args:
        empresa_id (int): Identificador de la empresa.

    Returns:
        Empresa: Objeto Empresa obtenido.

    Raises:
        HTTPException: Con código 404 si la empresa no existe o 500 en caso de error interno.
    """
    try:
        empresa = EmpresaRepository.get_by_id(empresa_id)
    except Exception as error:
        logger.error("Error al obtener Empresa con id %s: %s", empresa_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not empresa:
        logger.warning("Empresa no encontrada con id %s", empresa_id)
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    return empresa

def controlador_py_logger_get_by_cuit(cuit: str) -> Empresa:
    """
    Obtiene una Empresa por su CUIT.

    Args:
        cuit (str): CUIT de la empresa.

    Returns:
        Empresa: Objeto Empresa obtenido.

    Raises:
        HTTPException: Si ocurre un error interno o si no se encuentra la empresa.
    """
    try:
        empresa = EmpresaRepository.get_by_cuit(cuit)
    except Exception as error:
        logger.error("Error al obtener empresa con CUIT %s: %s", cuit, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not empresa:
        logger.warning("Empresa no encontrada con CUIT %s", cuit)
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    return empresa

def controlador_py_logger_get_by_razon_social(razon_social: str) -> Empresa:
    """
    Obtiene una Empresa por su razón social.

    Args:
        razon_social (str): Razón social de la empresa.

    Returns:
        Empresa: Objeto Empresa obtenido.

    Raises:
        HTTPException: Si ocurre un error interno o si no se encuentra la empresa.
    """
    try:
        empresa = EmpresaRepository.get_by_razon_social(razon_social)
    except Exception as error:
        logger.error("Error al obtener empresa con razón social '%s': %s", razon_social, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not empresa:
        logger.warning("Empresa no encontrada con razón social '%s'", razon_social)
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    return empresa

def controlador_py_logger_get_all_empresas() -> List[Empresa]:
    """
    Obtiene todas las Empresas.

    Returns:
        List[Empresa]: Lista de empresas.

    Raises:
        HTTPException: Si ocurre un error interno.
    """
    try:
        empresas = EmpresaRepository.get_all()
    except Exception as error:
        logger.error("Error al obtener todas las empresas: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    return empresas

def controlador_py_logger_create_empresa(empresa: Empresa) -> Empresa:
    """
    Crea una nueva Empresa en la base de datos.

    Args:
        empresa (Empresa): Objeto Empresa a crear.

    Returns:
        Empresa: Objeto Empresa creado con los datos actualizados.

    Raises:
        HTTPException: Con código 500 si ocurre un error interno.
    """
    try:
        empresa_creada = EmpresaRepository.create(empresa)
        logger.info("Empresa creada exitosamente con id %s", empresa_creada.id)
        return empresa_creada
    except Exception as error:
        logger.error("Error al crear la empresa: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    
def controlador_py_logger_update_empresa(empresa: Empresa) -> Empresa:
    """
    Actualiza una Empresa existente en la base de datos.

    Args:
        empresa (Empresa): Objeto Empresa con los datos a actualizar (debe incluir el id).

    Returns:
        Empresa: Objeto Empresa actualizado.

    Raises:
        HTTPException: Si ocurre un error interno o si la empresa no existe.
    """
    try:
        empresa_actualizada = EmpresaRepository.update(empresa)
    except Exception as error:
        logger.error("Error al actualizar empresa con id %s: %s", empresa.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not empresa_actualizada:
        logger.warning("Empresa no encontrada para actualizar con id %s", empresa.id)
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    logger.info("Empresa actualizada exitosamente con id %s", empresa_actualizada.id)
    return empresa_actualizada

def controlador_py_logger_delete_empresa(empresa_id: int) -> bool:
    """
    Elimina una Empresa por su ID.

    Args:
        empresa_id (int): ID de la empresa a eliminar.

    Returns:
        bool: True si la eliminación fue exitosa.

    Raises:
        HTTPException: Si ocurre un error interno o si no se encuentra la empresa.
    """
    try:
        resultado = EmpresaRepository.delete(empresa_id)
    except Exception as error:
        logger.error("Error al eliminar empresa con id %s: %s", empresa_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not resultado:
        logger.warning("Empresa no encontrada para eliminar con id %s", empresa_id)
        raise HTTPException(status_code=404, detail="Empresa no encontrada")

    logger.info("Empresa eliminada exitosamente con id %s", empresa_id)
    return resultado