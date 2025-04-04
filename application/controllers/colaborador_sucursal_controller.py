import logging
from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder

from infrastructure.databases.models.colaborador_sucursal import ColaboradorSucursal
from infrastructure.repositories.colaborador_sucursal_repo import ColaboradorSucursalRepository
from application.config.logger_config import setup_logger
from application.services.colaborador_sucursal_service import (
    get_sucursales_by_colaborador,
    get_colaboradores_by_sucursal
)

logger = setup_logger(__name__)

def controlador_get_by_id(relacion_id: int, db: Session) -> Optional[ColaboradorSucursal]:
    try:
        relacion = ColaboradorSucursalRepository.get_by_id(relacion_id, db)
        if not relacion:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return relacion
    except Exception as error:
        logger.error("Error al obtener ColaboradorSucursal con id %s: %s", relacion_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_get_by_colaborador(colaborador_id: int, db: Session) -> List[ColaboradorSucursal]:
    try:
        relaciones = ColaboradorSucursalRepository.get_by_colaborador(colaborador_id, db)
        return relaciones
    except Exception as error:
        logger.error("Error al obtener ColaboradorSucursal para colaborador %s: %s", colaborador_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_get_by_sucursal(sucursal_id: int, db: Session) -> List[ColaboradorSucursal]:
    try:
        relaciones = ColaboradorSucursalRepository.get_by_sucursal(sucursal_id, db)
        return relaciones
    except Exception as error:
        logger.error("Error al obtener ColaboradorSucursal para sucursal %s: %s", sucursal_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_create_colaborador_sucursal(relacion: ColaboradorSucursal, db: Session) -> ColaboradorSucursal:
    try:
        nuevo = ColaboradorSucursalRepository.create(relacion, db)
        logger.info("Relación creada: %s", nuevo)
        return nuevo
    except Exception as error:
        logger.error("Error al crear ColaboradorSucursal: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_update_colaborador_sucursal(relacion: ColaboradorSucursal, db: Session) -> ColaboradorSucursal:
    try:
        actualizado = ColaboradorSucursalRepository.update(relacion, db)
        if not actualizado:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return actualizado
    except Exception as error:
        logger.error("Error al actualizar ColaboradorSucursal con id %s: %s", relacion.id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_delete_colaborador_sucursal(relacion_id: int, db: Session) -> bool:
    try:
        eliminado = ColaboradorSucursalRepository.delete(relacion_id, db)
        if not eliminado:
            raise HTTPException(status_code=404, detail="Registro no encontrado")
        return eliminado
    except Exception as error:
        logger.error("Error al eliminar ColaboradorSucursal con id %s: %s", relacion_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_get_sucursales_by_colaborador(colaborador_id: int, db: Session):
    """
    Llama al servicio que obtiene la lista de sucursales (objetos Sucursal)
    a partir de las relaciones ColaboradorSucursal para un colaborador.
    """
    try:
        sucursales = get_sucursales_by_colaborador(colaborador_id, db)
        return sucursales
    except Exception as e:
        logger.error("Error en controlador_get_sucursales_by_colaborador: %s", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e

def controlador_get_colaboradores_by_sucursal(sucursal_id: int, db: Session):
    """
    Llama al servicio que obtiene la lista de colaboradores (objetos Colaborador)
    a partir de las relaciones ColaboradorSucursal para una sucursal.
    """
    try:
        colaboradores = get_colaboradores_by_sucursal(sucursal_id, db)
        colaboradores = jsonable_encoder(colaboradores)
        return colaboradores
    except Exception as e:
        logger.error("Error en controlador_get_colaboradores_by_sucursal: %s", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e
