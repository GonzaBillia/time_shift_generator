from infrastructure.schemas.venta_hora import VentaHora, VentaHoraResponse
import math
from datetime import date

class Factura:
    def __init__(self, venta: VentaHora):
        self.sucursal = self._extract_value(venta.Sucursal, int)
        self.doc = venta.Doc
        self.documento = venta.Documento
        self.fecha = self._extract_value(venta.Fecha, date)
        # Ahora, venta.Hora ya es un objeto time gracias al validator; no es necesario extraer nada
        self.hora = venta.Hora  
        self.usuario = venta.Usuario
        self.efectivo = venta.Efectivo
        self.cta_cte = venta.CtaCte
        self.o_social = venta.OSocial
        self.obra_social_detalle = venta.obra_social_detalle
        self.tarjeta = venta.Tarjeta
        self.otros_mp = venta.OtrosMP
        self.total = venta.Total
        self.nombre = venta.apellido_y_nombre
        self.dni = venta.DNI
        self.cuit = venta.CUIT
        self.categoria = self.determinar_categoria()

    def _extract_value(self, value, expected_type):
        """
        Si el valor es una lista, extrae y retorna el primer elemento; de lo contrario, lo retorna tal cual.
        Además, se intenta convertir el valor al tipo esperado.
        """
        if isinstance(value, list):
            if len(value) > 0:
                value = value[0]
            else:
                return None
        try:
            if not isinstance(value, expected_type):
                return expected_type(value)
            return value
        except Exception:
            # Si falla la conversión, se retorna el valor tal cual
            return value

    def determinar_categoria(self):
        if self.obra_social_detalle:
            if self.obra_social_detalle.startswith("PAMI"):
                return "PAMI"
            else:
                return "Obra Social"
        else:
            return "Particular"

class VentasPorHora:
    def __init__(self):
        # Diccionario con claves: (sucursal, fecha, hora) y valores de conteo
        self.ventas = {}
    
    def agregar_factura(self, factura: Factura):
        # Usamos factura.hora.hour (ya que factura.hora es un objeto time)
        hora_factura = factura.hora.hour

        # Nos aseguramos de que sucursal y fecha sean de tipo inmutable (int y date, respectivamente)
        key = (factura.sucursal, factura.fecha, hora_factura)
        if key not in self.ventas:
            self.ventas[key] = {"PAMI": 0, "Obra Social": 0, "Particular": 0, "Total": 0}
        self.ventas[key][factura.categoria] += 1
        self.ventas[key]["Total"] += 1

    def procesar_facturas(self, facturas: list):
        for factura in facturas:
            self.agregar_factura(factura)

    def obtener_ventas(self):
        return self.ventas

def calcular_personas(ventas: dict, tiempo_promedio: int = 5) -> dict:
    """
    Calcula la cantidad de personas que habrían realizado las facturas en cada grupo
    (por sucursal, fecha y hora) dividiendo el total de facturas por la cantidad máxima 
    de facturas que una persona puede realizar en una hora.
    """
    personas_por_hora = {}
    facturas_por_persona = 60 / tiempo_promedio  # máximo de facturas por persona en una hora
    for key, data in ventas.items():
        total_facturas = data["Total"]
        personas = math.ceil(total_facturas / facturas_por_persona) if total_facturas > 0 else 0
        personas_por_hora[key] = personas
    return personas_por_hora
