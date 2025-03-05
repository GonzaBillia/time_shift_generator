import logging
from datetime import date
from infrastructure.schemas.venta_hora import VentaHoraResponse
from infrastructure.repositories.vta_hora_repo import get_vta_hora
from domain.models.venta_hora import Factura, VentasPorHora, calcular_personas  # Asegúrate de que estos modelos estén en domain/models/venta_hora.py

logger = logging.getLogger(__name__)

def obtener_facturas(sucursal: int, fecha_desde: date, fecha_hasta: date) -> list:
    """
    Obtiene los datos a través del repository y los valida con el esquema VentaHoraResponse.
    Retorna la lista de objetos validados (instancias de VentaHora).
    """
    data = get_vta_hora(sucursal, fecha_desde, fecha_hasta)
    venta_schema = VentaHoraResponse.model_validate({"data": data})
    return venta_schema.data

def transformar_resultado(resultado: dict) -> dict:
    """
    Transforma las claves del diccionario (que son tuplas) a strings para serialización JSON.
    """
    resultado_transformado = {}
    for key, value in resultado.items():
        nueva_clave = "_".join(str(elem) for elem in key)
        resultado_transformado[nueva_clave] = value
    return resultado_transformado

def obtener_ventas_por_hora(sucursal: int, fecha_desde: date, fecha_hasta: date) -> dict:
    """
    Orquesta la obtención y procesamiento de los datos:
      1. Obtiene y valida los datos.
      2. Crea instancias de Factura.
      3. Agrupa las facturas por sucursal, fecha y hora.
      4. Transforma las claves para serialización JSON.
    Retorna el diccionario resultante.
    """
    try:
        facturas_data = obtener_facturas(sucursal, fecha_desde, fecha_hasta)
        # Crear instancias de Factura a partir de cada registro validado
        facturas = [Factura(venta) for venta in facturas_data]
        
        # Agrupar las facturas
        ventas_por_hora = VentasPorHora()
        ventas_por_hora.procesar_facturas(facturas)
        resultado = ventas_por_hora.obtener_ventas()
        
        # Transformar las claves a strings
        resultado_transformado = transformar_resultado(resultado)
        return resultado_transformado
    except Exception as e:
        logger.error("Error en obtener_ventas_por_hora: %s", e)
        raise e


def obtener_personas_por_hora(sucursal: int, fecha_desde: date, fecha_hasta: date, tiempo_promedio: int = 5) -> dict:
    """
    Obtiene el agrupamiento de ventas por hora y calcula la cantidad de personas
    que realizaron las facturas en cada grupo, usando la función calcular_personas.
    Se redondea siempre hacia arriba (usando math.ceil).
    Retorna el diccionario con la cantidad de personas, con claves transformadas a strings.
    """
    # Primero, obtenemos el agrupamiento "raw" sin transformar las claves
    facturas_data = obtener_facturas(sucursal, fecha_desde, fecha_hasta)
    facturas = [Factura(venta) for venta in facturas_data]
    ventas_por_hora_obj = VentasPorHora()
    ventas_por_hora_obj.procesar_facturas(facturas)
    agrupamiento = ventas_por_hora_obj.obtener_ventas()
    # Calcular la cantidad de personas usando la función calcular_personas
    personas = calcular_personas(agrupamiento, tiempo_promedio)
    # Transformamos las claves para serialización JSON
    personas_transformado = transformar_resultado(personas)
    return personas_transformado