import logging
from datetime import date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from application.services.venta_hora_service import (
    obtener_ventas_por_hora, 
    obtener_facturas, 
    obtener_personas_por_hora
)
from infrastructure.schemas.venta_hora import VentaHoraResponse

logger = logging.getLogger(__name__)

def controlador_get_facturas(sucursal: int, fecha_desde: date, fecha_hasta: date, db: Session) -> VentaHoraResponse:
    """
    Llama al service para obtener las facturas sin procesar y las valida con el esquema.
    """
    try:
        facturas_data = obtener_facturas(sucursal, fecha_desde, fecha_hasta, db)
        # Como el esquema ya se validó en el service, se retorna directamente.
        return VentaHoraResponse(data=facturas_data)
    except Exception as e:
        logger.error("Error en controlador_get_facturas: %s", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e

def controlador_get_ventas_por_hora(sucursal: int, fecha_desde: date, fecha_hasta: date, db: Session) -> dict:
    """
    Llama al service para obtener las ventas agrupadas por hora.
    """
    try:
        return obtener_ventas_por_hora(sucursal, fecha_desde, fecha_hasta, db)
    except Exception as e:
        logger.error("Error en controlador_get_ventas_por_hora: %s", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e

def controlador_get_personas_por_hora(sucursal: int, fecha_desde: date, fecha_hasta: date, db: Session, tiempo_promedio: int = 5) -> dict:
    """
    Obtiene el agrupamiento de ventas por hora y calcula la cantidad de personas
    que realizaron las facturas en cada grupo usando la función calcular_personas.
    Se utiliza math.ceil para redondear hacia arriba.
    Retorna un diccionario con la cantidad de personas, con las claves transformadas a strings.
    """
    try:
        return obtener_personas_por_hora(sucursal, fecha_desde, fecha_hasta, db, tiempo_promedio)
    except Exception as e:
        logger.error("Error en controlador_get_personas_por_hora: %s", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e
