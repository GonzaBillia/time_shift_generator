from application.config.logger_config import setup_logger
from typing import List
from fastapi import HTTPException
from infrastructure.databases.models.espacio_disponible_sucursal import EspacioDisponibleSucursal
from infrastructure.repositories.espacio_disponible_sucursal_repo import EspacioDisponibleSucursalRepository

logger = setup_logger(__name__, "logs/espacio_disponible_sucursal.log")

def controlador_py_logger_get_by_id_espacio(espacio_id: int) -> EspacioDisponibleSucursal:
    try:
        espacio = EspacioDisponibleSucursalRepository.get_by_id(espacio_id)
    except Exception as error:
        logger.error("Error al obtener EspacioDisponibleSucursal con id %s: %s", espacio_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not espacio:
        logger.warning("EspacioDisponibleSucursal no encontrado con id %s", espacio_id)
        raise HTTPException(status_code=404, detail="EspacioDisponibleSucursal no encontrado")
    return espacio

def controlador_py_logger_get_all_espacios() -> List[EspacioDisponibleSucursal]:
    try:
        espacios = EspacioDisponibleSucursalRepository.get_all()
    except Exception as error:
        logger.error("Error al obtener todos los espacios disponibles: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return espacios

def controlador_py_logger_get_by_sucursal(sucursal_id: int) -> List[EspacioDisponibleSucursal]:
    try:
        espacios = EspacioDisponibleSucursalRepository.get_by_sucursal(sucursal_id)
    except Exception as error:
        logger.error("Error al obtener espacios disponibles para sucursal %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return espacios

def controlador_py_logger_get_by_rol(sucursal_id: int, rol_colaborador_id: int) -> EspacioDisponibleSucursal:
    try:
        espacio = EspacioDisponibleSucursalRepository.get_by_rol(sucursal_id, rol_colaborador_id)
    except Exception as error:
        logger.error("Error al obtener espacio disponible para sucursal %s y rol %s: %s", 
                     sucursal_id, rol_colaborador_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not espacio:
        logger.warning("EspacioDisponibleSucursal no encontrado para sucursal %s y rol %s",
                       sucursal_id, rol_colaborador_id)
        raise HTTPException(status_code=404, detail="EspacioDisponibleSucursal no encontrado")
    return espacio

def controlador_py_logger_create_espacio(espacio: EspacioDisponibleSucursal) -> EspacioDisponibleSucursal:
    try:
        nuevo_espacio = EspacioDisponibleSucursalRepository.create(espacio)
        logger.info("EspacioDisponibleSucursal creado exitosamente con id %s", nuevo_espacio.id)
        return nuevo_espacio
    except Exception as error:
        logger.error("Error al crear EspacioDisponibleSucursal: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_update_espacio(espacio: EspacioDisponibleSucursal) -> EspacioDisponibleSucursal:
    try:
        actualizado = EspacioDisponibleSucursalRepository.update(espacio)
    except Exception as error:
        logger.error("Error al actualizar EspacioDisponibleSucursal con id %s: %s", espacio.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not actualizado:
        logger.warning("EspacioDisponibleSucursal no encontrado para actualizar con id %s", espacio.id)
        raise HTTPException(status_code=404, detail="EspacioDisponibleSucursal no encontrado")
    
    logger.info("EspacioDisponibleSucursal actualizado exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_py_logger_delete_espacio(espacio_id: int) -> bool:
    try:
        eliminado = EspacioDisponibleSucursalRepository.delete(espacio_id)
    except Exception as error:
        logger.error("Error al eliminar EspacioDisponibleSucursal con id %s: %s", espacio_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("EspacioDisponibleSucursal no encontrado para eliminar con id %s", espacio_id)
        raise HTTPException(status_code=404, detail="EspacioDisponibleSucursal no encontrado")
    
    logger.info("EspacioDisponibleSucursal eliminado exitosamente con id %s", espacio_id)
    return eliminado
