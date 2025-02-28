# CONTROLLER_PY_LOGGER_TIPO_EMPLEADO
from application.config.logger_config import setup_logger
from typing import List, Optional
from fastapi import HTTPException
from infrastructure.databases.models.tipo_colaborador import TipoEmpleado
from infrastructure.repositories.tipo_colaborador_repo import TipoEmpleadoRepository

logger = setup_logger(__name__, "logs/tipo_colaborador.log")

def controlador_py_logger_get_by_id_tipo_empleado(tipo_empleado_id: int) -> TipoEmpleado:
    """
    Obtiene un TipoEmpleado por su ID.
    """
    try:
        tipo = TipoEmpleadoRepository.get_by_id(tipo_empleado_id)
    except Exception as error:
        logger.error("Error al obtener TipoEmpleado con id %s: %s", tipo_empleado_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not tipo:
        logger.warning("TipoEmpleado no encontrado con id %s", tipo_empleado_id)
        raise HTTPException(status_code=404, detail="TipoEmpleado no encontrado")

    return tipo

def controlador_py_logger_get_all_tipo_empleado() -> List[TipoEmpleado]:
    """
    Obtiene todos los tipos de empleados.
    """
    try:
        tipos = TipoEmpleadoRepository.get_all()
    except Exception as error:
        logger.error("Error al obtener todos los tipos de empleados: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    return tipos

def controlador_py_logger_get_by_tipo_tipo_empleado(tipo: str) -> TipoEmpleado:
    """
    Obtiene un TipoEmpleado por su campo 'tipo' (nombre).
    """
    try:
        tipo_empleado = TipoEmpleadoRepository.get_by_tipo(tipo)
    except Exception as error:
        logger.error("Error al obtener TipoEmpleado por tipo %s: %s", tipo, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not tipo_empleado:
        logger.warning("TipoEmpleado no encontrado con tipo %s", tipo)
        raise HTTPException(status_code=404, detail="TipoEmpleado no encontrado")

    return tipo_empleado

def controlador_py_logger_create_tipo_empleado(tipo: TipoEmpleado) -> TipoEmpleado:
    """
    Crea un nuevo TipoEmpleado en la base de datos.
    """
    try:
        nuevo_tipo = TipoEmpleadoRepository.create(tipo)
        logger.info("TipoEmpleado creado exitosamente con id %s", nuevo_tipo.id)
        return nuevo_tipo
    except Exception as error:
        logger.error("Error al crear TipoEmpleado: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_update_tipo_empleado(tipo: TipoEmpleado) -> TipoEmpleado:
    """
    Actualiza un TipoEmpleado existente en la base de datos.
    """
    try:
        actualizado = TipoEmpleadoRepository.update(tipo)
    except Exception as error:
        logger.error("Error al actualizar TipoEmpleado con id %s: %s", tipo.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not actualizado:
        logger.warning("TipoEmpleado no encontrado para actualizar con id %s", tipo.id)
        raise HTTPException(status_code=404, detail="TipoEmpleado no encontrado")

    logger.info("TipoEmpleado actualizado exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_py_logger_delete_tipo_empleado(tipo_empleado_id: int) -> bool:
    """
    Elimina un TipoEmpleado por su ID.
    """
    try:
        eliminado = TipoEmpleadoRepository.delete(tipo_empleado_id)
    except Exception as error:
        logger.error("Error al eliminar TipoEmpleado con id %s: %s", tipo_empleado_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("TipoEmpleado no encontrado para eliminar con id %s", tipo_empleado_id)
        raise HTTPException(status_code=404, detail="TipoEmpleado no encontrado")

    logger.info("TipoEmpleado eliminado exitosamente con id %s", tipo_empleado_id)
    return eliminado


