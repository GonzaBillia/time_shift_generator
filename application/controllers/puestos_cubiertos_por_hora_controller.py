from application.config.logger_config import setup_logger
from typing import List, Optional
from datetime import time
from fastapi import HTTPException
from sqlalchemy.orm import Session
from infrastructure.databases.models.puestos_cubiertos_por_hora import PuestosCubiertosPorHora
from infrastructure.repositories.puestos_cubiertos_por_hora_repo import PuestosCubiertosPorHoraRepository

logger = setup_logger(__name__, "logs/puestos_cubiertos.log")

def controlador_get_by_sucursal_puestos(sucursal_id: int, db: Session) -> List[PuestosCubiertosPorHora]:
    try:
        registros = PuestosCubiertosPorHoraRepository.get_by_sucursal(sucursal_id, db)
        return registros
    except Exception as error:
        logger.error("Error al obtener puestos cubiertos para sucursal %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_get_by_rol_puestos(sucursal_id: int, rol_colaborador_id: int, db: Session) -> List[PuestosCubiertosPorHora]:
    try:
        registros = PuestosCubiertosPorHoraRepository.get_by_rol(sucursal_id, rol_colaborador_id, db)
        return registros
    except Exception as error:
        logger.error("Error al obtener puestos cubiertos para sucursal %s y rol %s: %s", 
                     sucursal_id, rol_colaborador_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_get_by_horario_puestos(sucursal_id: int, dia_id: int, hora: time, db: Session) -> Optional[PuestosCubiertosPorHora]:
    try:
        registro = PuestosCubiertosPorHoraRepository.get_by_horario(sucursal_id, dia_id, hora, db)
    except Exception as error:
        logger.error("Error al obtener registro para sucursal %s, día %s y hora %s: %s", 
                     sucursal_id, dia_id, hora, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not registro:
        logger.warning("No se encontró registro para sucursal %s, día %s y hora %s", sucursal_id, dia_id, hora)
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

def controlador_create_puestos(registro: PuestosCubiertosPorHora, db: Session) -> PuestosCubiertosPorHora:
    try:
        nuevo = PuestosCubiertosPorHoraRepository.create(registro, db)
        logger.info("Registro creado exitosamente con id %s", nuevo.id)
        return nuevo
    except Exception as error:
        logger.error("Error al crear registro de puestos cubiertos: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_update_puestos(registro: PuestosCubiertosPorHora, db: Session) -> PuestosCubiertosPorHora:
    try:
        actualizado = PuestosCubiertosPorHoraRepository.update(registro, db)
    except Exception as error:
        logger.error("Error al actualizar registro con id %s: %s", registro.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not actualizado:
        logger.warning("Registro no encontrado para actualizar con id %s", registro.id)
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    logger.info("Registro actualizado exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_delete_puestos(registro_id: int, db: Session) -> bool:
    try:
        eliminado = PuestosCubiertosPorHoraRepository.delete(registro_id, db)
    except Exception as error:
        logger.error("Error al eliminar registro con id %s: %s", registro_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("Registro no encontrado para eliminar con id %s", registro_id)
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    logger.info("Registro eliminado exitosamente con id %s", registro_id)
    return eliminado
