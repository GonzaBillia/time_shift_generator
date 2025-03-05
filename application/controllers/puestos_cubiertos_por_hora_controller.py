# application/controllers/puestos_cubiertos_controller.py

import logging
from typing import List, Optional
from datetime import time
from fastapi import HTTPException
from infrastructure.databases.models.puestos_cubiertos_por_hora import PuestosCubiertosPorHora
from infrastructure.repositories.puestos_cubiertos_por_hora_repo import PuestosCubiertosPorHoraRepository
from application.config.logger_config import setup_logger

logger = setup_logger(__name__, "logs/puestos_cubiertos.log")

def controlador_get_by_sucursal_puestos(sucursal_id: int) -> List[PuestosCubiertosPorHora]:
    try:
        registros = PuestosCubiertosPorHoraRepository.get_by_sucursal(sucursal_id)
        return registros
    except Exception as error:
        logger.error("Error al obtener puestos cubiertos para sucursal %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_get_by_rol_puestos(sucursal_id: int, rol_colaborador_id: int) -> List[PuestosCubiertosPorHora]:
    try:
        registros = PuestosCubiertosPorHoraRepository.get_by_rol(sucursal_id, rol_colaborador_id)
        return registros
    except Exception as error:
        logger.error("Error al obtener puestos cubiertos para sucursal %s y rol %s: %s", 
                     sucursal_id, rol_colaborador_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_get_by_horario_puestos(sucursal_id: int, dia_id: int, hora: time) -> Optional[PuestosCubiertosPorHora]:
    try:
        registro = PuestosCubiertosPorHoraRepository.get_by_horario(sucursal_id, dia_id, hora)
    except Exception as error:
        logger.error("Error al obtener registro para sucursal %s, día %s y hora %s: %s", 
                     sucursal_id, dia_id, hora, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not registro:
        logger.warning("No se encontró registro para sucursal %s, día %s y hora %s", sucursal_id, dia_id, hora)
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    return registro

def controlador_create_puestos(registro: PuestosCubiertosPorHora) -> PuestosCubiertosPorHora:
    try:
        nuevo = PuestosCubiertosPorHoraRepository.create(registro)
        logger.info("Registro creado exitosamente con id %s", nuevo.id)
        return nuevo
    except Exception as error:
        logger.error("Error al crear registro de puestos cubiertos: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_update_puestos(registro: PuestosCubiertosPorHora) -> PuestosCubiertosPorHora:
    try:
        actualizado = PuestosCubiertosPorHoraRepository.update(registro)
    except Exception as error:
        logger.error("Error al actualizar registro con id %s: %s", registro.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not actualizado:
        logger.warning("Registro no encontrado para actualizar con id %s", registro.id)
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    logger.info("Registro actualizado exitosamente con id %s", actualizado.id)
    return actualizado

def controlador_delete_puestos(registro_id: int) -> bool:
    try:
        eliminado = PuestosCubiertosPorHoraRepository.delete(registro_id)
    except Exception as error:
        logger.error("Error al eliminar registro con id %s: %s", registro_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("Registro no encontrado para eliminar con id %s", registro_id)
        raise HTTPException(status_code=404, detail="Registro no encontrado")
    
    logger.info("Registro eliminado exitosamente con id %s", registro_id)
    return eliminado
