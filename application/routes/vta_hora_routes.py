from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
from datetime import date
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
import logging

from application.helpers.response_handler import success_response, error_response
from application.controllers.vta_hora_controller import (
    controlador_get_facturas,
    controlador_get_ventas_por_hora,
    controlador_get_personas_por_hora
)
from application.config.logger_config import setup_logger
from infrastructure.schemas.venta_hora import VentaHoraResponse

# Dependencias para la sesión, autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles

router = APIRouter(prefix="/vta_hora", tags=["Vta Hora"])
logger = setup_logger(__name__, "logs/vta_hora.log")

@router.get("/facturas", response_model=VentaHoraResponse)
def get_vta_hora(
    sucursal: int = Query(..., description="ID de la sucursal"),
    fecha_desde: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_hasta: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db_factory("plex")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    """
    Endpoint para obtener la información de facturas sin procesar.
    """
    try:
        factura_response = controlador_get_facturas(sucursal, fecha_desde, fecha_hasta, db)
        data_json = jsonable_encoder(factura_response.data)
        return success_response("Facturas obtenidas exitosamente", data=data_json)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_vta_hora: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/", response_model=dict)
def get_ventas_por_hora(
    sucursal: int = Query(..., description="ID de la sucursal"),
    fecha_desde: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_hasta: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    db: Session = Depends(get_db_factory("plex")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    """
    Endpoint que obtiene las ventas agrupadas por hora.
    """
    try:
        resultado = controlador_get_ventas_por_hora(sucursal, fecha_desde, fecha_hasta, db)
        resultado_json = jsonable_encoder(resultado)
        return success_response("Ventas por hora obtenidas exitosamente", data=resultado_json)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_ventas_por_hora: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/personas", response_model=dict)
def get_personas_por_hora(
    sucursal: int = Query(..., description="ID de la sucursal"),
    fecha_desde: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_hasta: date = Query(..., description="Fecha de fin (YYYY-MM-DD)"),
    tiempo_promedio: int = Query(5, description="Tiempo promedio (en minutos) que tarda una factura"),
    db: Session = Depends(get_db_factory("plex")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin"))
):
    """
    Endpoint que calcula, a partir del agrupamiento de ventas por hora, la cantidad de personas
    que realizaron las facturas. Se utiliza math.ceil para redondear hacia arriba.
    """
    try:
        resultado = controlador_get_personas_por_hora(sucursal, fecha_desde, fecha_hasta, db, tiempo_promedio)
        resultado_json = jsonable_encoder(resultado)
        return success_response("Cantidad de personas obtenida exitosamente", data=resultado_json)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_personas_por_hora: %s", e)
        return error_response(str(e), status_code=500)
