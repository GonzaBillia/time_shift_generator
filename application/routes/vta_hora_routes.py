from fastapi import APIRouter, HTTPException, Query
from datetime import date
from fastapi.encoders import jsonable_encoder
from domain.models.venta_hora import Factura, VentasPorHora
from application.controllers.vta_hora_controller import controlador_py_logger_get_vta_hora
from infrastructure.schemas.venta_hora import VentaHoraResponse
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

router = APIRouter(prefix="/vta_hora", tags=["Vta Hora"])
logger = setup_logger(__name__, "logs/vta_hora.log")

def transformar_resultado(resultado: dict) -> dict:
    """
    Transforma las claves del diccionario (que son tuplas) a strings.
    """
    resultado_transformado = {}
    for key, value in resultado.items():
        # Convertir cada elemento de la tupla a string y unirlos con un guión o algún separador
        nueva_clave = "_".join(str(elem) for elem in key)
        resultado_transformado[nueva_clave] = value
    return resultado_transformado


@router.get("/facturas", response_model=VentaHoraResponse)
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
        # Validamos y convertimos la respuesta al esquema definido
        venta_schema = VentaHoraResponse.model_validate({"data": data})
        # venta_schema.data es la lista de objetos validados
        data_json = jsonable_encoder(venta_schema.data)
        return success_response("Datos obtenidos exitosamente", data=data_json)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_vta_hora: %s", e)
        return error_response(str(e), status_code=500)


@router.get("/", response_model=dict)
def get_ventas_por_hora(
    sucursal: int = Query(..., description="ID de la sucursal"),
    fecha_desde: date = Query(..., description="Fecha de inicio (YYYY-MM-DD)"),
    fecha_hasta: date = Query(..., description="Fecha de fin (YYYY-MM-DD)")
):
    try:
        data = controlador_py_logger_get_vta_hora(sucursal, fecha_desde, fecha_hasta)
        venta_schema = VentaHoraResponse.model_validate({"data": data})
        facturas = [Factura(venta) for venta in venta_schema.data]
        ventas_por_hora = VentasPorHora()
        ventas_por_hora.procesar_facturas(facturas)
        resultado = ventas_por_hora.obtener_ventas()
        
        # Transforma las claves a string para que sean serializables en JSON
        resultado_transformado = transformar_resultado(resultado)
        
        resultado_json = jsonable_encoder(resultado_transformado)
        return success_response("Ventas por hora obtenidas exitosamente", data=resultado_json)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_ventas_por_hora: %s", e)
        return error_response(str(e), status_code=500)
