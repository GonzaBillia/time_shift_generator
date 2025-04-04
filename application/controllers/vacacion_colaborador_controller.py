import logging
from typing import List
from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from infrastructure.databases.models.vacacion_colaborador import VacacionColaborador
from infrastructure.repositories.vacacion_colaborador_repo import VacacionColaboradorRepository
from application.config.logger_config import setup_logger

logger = setup_logger(__name__, "logs/vacacion_colaborador.log")

def controlador_get_by_colaborador_vacacion(colaborador_id: int, db: Session) -> List[VacacionColaborador]:
    """
    Devuelve todas las vacaciónes para un colaborador específico.
    """
    try:
        vacaciones = VacacionColaboradorRepository.get_by_colaborador(colaborador_id, db)
        return vacaciones
    except Exception as error:
        logger.error("Error al obtener vacaciones para colaborador %s: %s", colaborador_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_get_by_fecha_vacacion(fecha: date, db: Session) -> List[VacacionColaborador]:
    """
    Devuelve todas las vacaciónes registradas para una fecha específica.
    """
    try:
        vacaciones = VacacionColaboradorRepository.get_by_fecha(fecha, db)
        return vacaciones
    except Exception as error:
        logger.error("Error al obtener vacaciones para fecha %s: %s", fecha, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_create_vacacion(vacacion: VacacionColaborador, db: Session) -> VacacionColaborador:
    """
    Crea un nuevo registro de vacación para un colaborador.
    """
    try:
        nuevo = VacacionColaboradorRepository.create(vacacion, db)
        return nuevo
    except Exception as error:
        logger.error("Error al crear vacación: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_delete_vacacion(vacacion_id: int, db: Session) -> bool:
    """
    Elimina un registro de vacación por su ID.
    """
    try:
        eliminado = VacacionColaboradorRepository.delete(vacacion_id, db)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return eliminado
    except Exception as error:
        logger.error("Error al eliminar vacación con id %s: %s", vacacion_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_update_vacacion(vacacion: VacacionColaborador, db: Session) -> VacacionColaborador:
    """
    Actualiza un registro de vacación. Se asume que en el repository existe un método update.
    Si no existe, se implementa una lógica similar a otros módulos.
    """
    try:
        actualizado = VacacionColaboradorRepository.update(vacacion, db)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return actualizado
    except Exception as error:
        logger.error("Error al actualizar vacación con id %s: %s", vacacion.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
