import logging
from datetime import date
from fastapi import HTTPException
from application.services.venta_hora_service import obtener_ventas_por_hora, obtener_facturas
from infrastructure.schemas.venta_hora import VentaHoraResponse

logger = logging.getLogger(__name__)

def controlador_get_facturas(sucursal: int, fecha_desde: date, fecha_hasta: date) -> VentaHoraResponse:
    """
    Llama al service para obtener las facturas sin procesar y las valida con el esquema.
    """
    try:
        facturas_data = obtener_facturas(sucursal, fecha_desde, fecha_hasta)
        # Como el esquema ya se validó en el service, podemos retornar directamente
        return VentaHoraResponse(data=facturas_data)
    except Exception as e:
        logger.error("Error en controlador_get_facturas: %s", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e

def controlador_get_ventas_por_hora(sucursal: int, fecha_desde: date, fecha_hasta: date) -> dict:
    """
    Llama al service para obtener las ventas agrupadas por hora.
    """
    try:
        return obtener_ventas_por_hora(sucursal, fecha_desde, fecha_hasta)
    except Exception as e:
        logger.error("Error en controlador_get_ventas_por_hora: %s", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e
