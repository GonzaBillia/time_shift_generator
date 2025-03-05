# ROUTER_PY_SCHEMA_VTA_HORA
from fastapi import APIRouter, HTTPException, Query
from typing import List
from datetime import date
from fastapi.encoders import jsonable_encoder
from application.controllers.vta_hora_controller import controlador_py_logger_get_vta_hora
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

router = APIRouter(prefix="/vta_hora", tags=["Vta Hora"])
logger = setup_logger(__name__, "logs/vta_hora.log")

@router.get("/", response_model=List[dict])
def get_vta_hora(
    sucursal: int = Query(..., description="ID de la sucursal"),
    fecha_desde: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_hasta: date = Query(..., description="Fecha de fin (YYYY-MM-DD)")
):
    """
    Endpoint para obtener la información de ventas/hora usando el archivo get_vta_hora.sql.
    Recibe como parámetros:
      - sucursal: int
      - fecha_desde: date
      - fecha_hasta: date
    """
    try:
        data = controlador_py_logger_get_vta_hora(sucursal, fecha_desde, fecha_hasta)
        # Serializa la salida para asegurar que fechas se conviertan a ISO strings, etc.
        return success_response("Datos obtenidos exitosamente", data=jsonable_encoder(data))
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_vta_hora: %s", e)
        return error_response(str(e), status_code=500)
