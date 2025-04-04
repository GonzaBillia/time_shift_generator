import logging
from datetime import date, datetime, timedelta
from typing import List, Dict, Any
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from infrastructure.schemas.venta_hora import VentaHoraResponse
from infrastructure.repositories.vta_hora_repo import get_vta_hora
from domain.models.venta_hora import Factura, VentasPorHora, calcular_personas

logger = logging.getLogger(__name__)

def obtener_facturas(sucursal: int, fecha_desde: date, fecha_hasta: date, db: Session) -> List[Any]:
    """
    Obtiene los datos de ventas por hora a través del repository y los valida
    con el esquema VentaHoraResponse. Retorna la lista de objetos validados,
    es decir, los datos que forman parte de la respuesta de ventas.
    """
    try:
        data = get_vta_hora(sucursal, fecha_desde, fecha_hasta, db)
        # Se valida que la data obtenida cumpla con el esquema esperado.
        venta_schema = VentaHoraResponse.model_validate({"data": data})
        return venta_schema.data
    except Exception as e:
        logger.error("Error en obtener_facturas: %s", e)
        raise e

def transformar_resultado(resultado: Dict[Any, Any]) -> Dict[str, Any]:
    """
    Transforma las claves del diccionario, que son tuplas, a strings para
    permitir la serialización a JSON. Cada clave se convierte uniendo sus
    elementos con un guion bajo.
    """
    resultado_transformado = {}
    for key, value in resultado.items():
        nueva_clave = "_".join(str(elem) for elem in key)
        resultado_transformado[nueva_clave] = value
    return resultado_transformado

def obtener_ventas_por_hora(sucursal: int, fecha_desde: date, fecha_hasta: date, db: Session) -> Dict[str, Any]:
    """
    Orquesta la obtención y procesamiento de los datos:
      1. Obtiene y valida los datos de ventas.
      2. Crea instancias de Factura a partir de cada registro.
      3. Agrupa las facturas por sucursal, fecha y hora mediante el objeto VentasPorHora.
      4. Transforma las claves del resultado para que sean cadenas.
    Retorna el diccionario resultante.
    """
    try:
        # 1. Obtener y validar los datos de ventas.
        facturas_data = obtener_facturas(sucursal, fecha_desde, fecha_hasta, db)
        # 2. Crear instancias de Factura a partir de cada registro validado.
        facturas = [Factura(venta) for venta in facturas_data]
        # 3. Procesar las facturas agrupándolas por sucursal, fecha y hora.
        ventas_por_hora = VentasPorHora()
        ventas_por_hora.procesar_facturas(facturas)
        resultado = ventas_por_hora.obtener_ventas()
        # 4. Transformar las claves a strings para la serialización JSON.
        resultado_transformado = transformar_resultado(resultado)
        return resultado_transformado
    except Exception as e:
        logger.error("Error en obtener_ventas_por_hora: %s", e)
        raise e

def obtener_personas_por_hora(sucursal: int, fecha_desde: date, fecha_hasta: date, db: Session, tiempo_promedio: int = 5) -> Dict[str, Any]:
    """
    Obtiene el agrupamiento de ventas por hora y calcula la cantidad de personas
    que realizaron las facturas en cada grupo usando la función calcular_personas.
    Se utiliza math.ceil para redondear hacia arriba.
    Retorna un diccionario con la cantidad de personas, con las claves transformadas a strings.
    """
    try:
        # Obtener el agrupamiento raw de ventas.
        facturas_data = obtener_facturas(sucursal, fecha_desde, fecha_hasta, db)
        facturas = [Factura(venta) for venta in facturas_data]
        ventas_por_hora_obj = VentasPorHora()
        ventas_por_hora_obj.procesar_facturas(facturas)
        agrupamiento = ventas_por_hora_obj.obtener_ventas()
        # Calcular la cantidad de personas por hora utilizando el tiempo promedio.
        personas = calcular_personas(agrupamiento, tiempo_promedio)
        # Transformar las claves para que sean cadenas, adecuadas para JSON.
        personas_transformado = transformar_resultado(personas)
        return personas_transformado
    except Exception as e:
        logger.error("Error en obtener_personas_por_hora: %s", e)
        raise e
