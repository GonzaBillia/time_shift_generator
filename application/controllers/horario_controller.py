# CONTROLLER_PY_LOGGER_HORARIO
from application.config.logger_config import setup_logger
from datetime import date, time
from typing import List
from fastapi import HTTPException
from infrastructure.databases.models.horario import Horario
from infrastructure.repositories.horario_repo import HorarioRepository

logger = setup_logger(__name__, "logs/horario.log")

def controlador_py_logger_get_by_id_horario(horario_id: int) -> Horario:
    """
    Obtiene un Horario por su ID.
    """
    try:
        horario = HorarioRepository.get_by_id(horario_id)
    except Exception as error:
        logger.error("Error al obtener Horario con id %s: %s", horario_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not horario:
        logger.warning("Horario no encontrado con id %s", horario_id)
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    return horario

def controlador_py_logger_get_all_horarios() -> List[Horario]:
    """
    Obtiene todos los Horarios.
    """
    try:
        horarios = HorarioRepository.get_all()
    except Exception as error:
        logger.error("Error al obtener todos los Horarios: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horarios

def controlador_py_logger_create_horario(horario: Horario) -> Horario:
    """
    Crea un nuevo Horario y lo persiste en la base de datos.
    """
    try:
        nuevo = HorarioRepository.create(horario)
        logger.info("Horario creado exitosamente con id %s", nuevo.id)
        return nuevo
    except Exception as error:
        logger.error("Error al crear Horario: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_update_horario(horario: Horario) -> Horario:
    """
    Actualiza un Horario existente.
    Permite actualización parcial: se espera que la instancia 'horario'
    ya tenga los campos modificados.
    """
    try:
        # Verifica que exista el Horario
        existente = HorarioRepository.get_by_id(horario.id)
        if not existente:
            logger.warning("Horario no encontrado para actualizar con id %s", horario.id)
            raise HTTPException(status_code=404, detail="Horario no encontrado")
        
        actualizado = HorarioRepository.update(horario)
    except Exception as error:
        logger.error("Error al actualizar Horario con id %s: %s", horario.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not actualizado:
        logger.warning("Horario no encontrado tras actualización con id %s", horario.id)
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    logger.info("Horario actualizado exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_py_logger_delete_horario(horario_id: int) -> bool:
    """
    Elimina un Horario por su ID.
    """
    try:
        eliminado = HorarioRepository.delete(horario_id)
    except Exception as error:
        logger.error("Error al eliminar Horario con id %s: %s", horario_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("Horario no encontrado para eliminar con id %s", horario_id)
        raise HTTPException(status_code=404, detail="Horario no encontrado")
    
    logger.info("Horario eliminado exitosamente con id %s", horario_id)
    return eliminado

def controlador_py_logger_get_by_sucursal(sucursal_id: int) -> List[Horario]:
    """
    Devuelve todos los Horarios asociados a una Sucursal.
    """
    try:
        horarios = HorarioRepository.get_by_sucursal(sucursal_id)
    except Exception as error:
        logger.error("Error al obtener Horarios para Sucursal %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horarios

def controlador_py_logger_get_by_colaborador(colaborador_id: int) -> List[Horario]:
    """
    Devuelve todos los Horarios asociados a un Colaborador.
    """
    try:
        horarios = HorarioRepository.get_by_colaborador(colaborador_id)
    except Exception as error:
        logger.error("Error al obtener Horarios para Colaborador %s: %s", colaborador_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horarios

def controlador_py_logger_get_by_fecha(fecha: date) -> List[Horario]:
    """
    Devuelve todos los Horarios para una fecha específica.
    """
    try:
        horarios = HorarioRepository.get_by_fecha(fecha)
    except Exception as error:
        logger.error("Error al obtener Horarios para fecha %s: %s", fecha, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horarios

def controlador_py_logger_verificar_superposicion(
    sucursal_id: int, fecha: date, hora_inicio: time, hora_fin: time
) -> bool:
    """
    Verifica si existe al menos un Horario en la misma sucursal y fecha
    que se superponga con el rango [hora_inicio, hora_fin].
    """
    try:
        superpone = HorarioRepository.verificar_superposicion(sucursal_id, fecha, hora_inicio, hora_fin)
    except Exception as error:
        logger.error("Error al verificar superposición en Sucursal %s, fecha %s: %s", sucursal_id, fecha, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return superpone

def controlador_py_logger_get_horarios_por_dia(sucursal_id: int, dia_id: int) -> List[Horario]:
    """
    Devuelve la lista de Horarios de una Sucursal en un día específico.
    """
    try:
        horarios = HorarioRepository.get_horarios_por_dia(sucursal_id, dia_id)
    except Exception as error:
        logger.error("Error al obtener Horarios para Sucursal %s en día %s: %s", sucursal_id, dia_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
    return horarios
