from application.config.logger_config import setup_logger
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from infrastructure.databases.models.sucursal import Sucursal
from infrastructure.schemas.sucursal import SucursalFullUpdate
from infrastructure.repositories.sucursal_repo import SucursalRepository
from application.services.sucursal_service import update_full_sucursal
# Importamos los controladores para validar las FK
from application.controllers.empresa_controller import controlador_py_logger_get_by_id_empresa
from application.controllers.formato_controller import controlador_py_logger_get_by_id_formato

logger = setup_logger(__name__, "logs/sucursal.log")

def controlador_py_logger_get_by_id_sucursal(sucursal_id: int, db: Session) -> Sucursal:
    """
    Obtiene una Sucursal por su ID.
    """
    try:
        sucursal = SucursalRepository.get_by_id(sucursal_id, db)
    except Exception as error:
        logger.error("Error al obtener Sucursal con id %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not sucursal:
        logger.warning("Sucursal no encontrada con id %s", sucursal_id)
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal

def controlador_py_logger_get_all_sucursales(db: Session) -> List[Sucursal]:
    """
    Obtiene todas las Sucursales.
    """
    try:
        sucursales = SucursalRepository.get_all(db)
    except Exception as error:
        logger.error("Error al obtener todas las Sucursales: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return sucursales

def controlador_py_logger_create_sucursal(sucursal: Sucursal, db: Session) -> Sucursal:
    """
    Crea una nueva Sucursal en la base de datos.
    Valida que la Empresa y el Formato existan.
    """
    try:
        # Validar las FK: empresa_id y formato_id usando la sesión
        controlador_py_logger_get_by_id_empresa(sucursal.empresa_id, db)
        controlador_py_logger_get_by_id_formato(sucursal.formato_id, db)
        
        nueva = SucursalRepository.create(sucursal, db)
        logger.info("Sucursal creada exitosamente con id %s", nueva.id)
        return nueva
    except HTTPException as he:
        raise he
    except Exception as error:
        logger.error("Error al crear Sucursal: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_update_sucursal_partial(sucursal_id: int, update_data: Dict[str, Any], db: Session) -> Sucursal:
    """
    Actualiza parcialmente una Sucursal.
    Se recupera la instancia actual, se validan las FK (si se envían) y se actualizan
    solo los campos presentes en 'update_data'.

    Args:
        sucursal_id (int): ID de la Sucursal a actualizar.
        update_data (dict): Diccionario con los campos a actualizar.

    Returns:
        Sucursal: La instancia actualizada.

    Raises:
        HTTPException: Si ocurre algún error o no se encuentra la Sucursal.
    """
    try:
        # Recupera la sucursal actual
        sucursal_actual = controlador_py_logger_get_by_id_sucursal(sucursal_id, db)
        
        # Validar FK si se están actualizando
        if "empresa_id" in update_data and update_data["empresa_id"] is not None:
            controlador_py_logger_get_by_id_empresa(update_data["empresa_id"], db)
        if "formato_id" in update_data and update_data["formato_id"] is not None:
            controlador_py_logger_get_by_id_formato(update_data["formato_id"], db)
        
        # Actualiza solo los campos enviados
        for key, value in update_data.items():
            setattr(sucursal_actual, key, value)
        
        actualizado = SucursalRepository.update(sucursal_actual, db)
    except Exception as error:
        logger.error("Error al actualizar Sucursal con id %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not actualizado:
        logger.warning("Sucursal no encontrada para actualizar con id %s", sucursal_id)
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    
    logger.info("Sucursal actualizada exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_py_logger_delete_sucursal(sucursal_id: int, db: Session) -> bool:
    """
    Elimina una Sucursal por su ID.
    """
    try:
        resultado = SucursalRepository.delete(sucursal_id, db)
    except Exception as error:
        logger.error("Error al eliminar Sucursal con id %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not resultado:
        logger.warning("Sucursal no encontrada para eliminar con id %s", sucursal_id)
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    logger.info("Sucursal eliminada exitosamente con id %s", sucursal_id)
    return resultado

def controlador_py_logger_get_by_nombre_sucursal(nombre: str, db: Session) -> Sucursal:
    """
    Obtiene una Sucursal por su nombre.
    """
    try:
        sucursal = SucursalRepository.get_by_nombre(nombre, db)
    except Exception as error:
        logger.error("Error al obtener Sucursal con nombre '%s': %s", nombre, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not sucursal:
        logger.warning("Sucursal no encontrada con nombre '%s'", nombre)
        raise HTTPException(status_code=404, detail="Sucursal no encontrada")
    return sucursal

def controlador_py_logger_get_by_empresa(empresa_id: int, db: Session) -> List[Sucursal]:
    """
    Obtiene todas las Sucursales asociadas a una Empresa específica.
    """
    try:
        sucursales = SucursalRepository.get_by_empresa(empresa_id, db)
    except Exception as error:
        logger.error("Error al obtener Sucursales de la Empresa con id %s: %s", empresa_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return sucursales

def controlador_py_logger_get_horarios(sucursal_id: int, db: Session) -> List:
    """
    Obtiene la lista de horarios asignados a una Sucursal.
    """
    try:
        horarios = SucursalRepository.get_horarios(sucursal_id, db)
    except Exception as error:
        logger.error("Error al obtener horarios para Sucursal con id %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horarios

def controlador_update_full_sucursal(sucursal_id: int, data: SucursalFullUpdate, db: Session) -> Sucursal:
    """
    Llama al servicio para actualizar completamente una sucursal y sus objetos asociados.
    """
    try:
        updated_sucursal = update_full_sucursal(sucursal_id, data, db)
        return updated_sucursal
    except Exception as e:
        logger.error("Error en controlador_update_full_sucursal: %s", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e
