from typing import List
from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import text
from infrastructure.databases.config.database import DBConfig as Database

def get_vta_hora(sucursal: int, fecha_desde: date, fecha_hasta: date) -> List[dict]:
    """
    Ejecuta la consulta definida en el archivo get_vta_hora.sql usando los parámetros:
      - sucursal: int
      - fecha_desde: date
      - fecha_hasta: date

    Retorna una lista de diccionarios con los resultados.
    """
    session: Session = Database.get_session("plex")
    # Ruta relativa del archivo SQL; ajusta según la ubicación real.
    with open("infrastructure/databases/queries/get_vta_hora.sql", "r", encoding="utf-8") as f:
        sql_query = f.read()
    
    # Ejecuta la consulta usando parámetros nombrados
    result = session.execute(
        text(sql_query),
        {"sucursal": sucursal, "fecha_desde": fecha_desde, "fecha_hasta": fecha_hasta}
    )
    rows = result.fetchall()
    session.close()
    # Convertir cada fila en un diccionario usando _mapping
    return [dict(row._mapping) for row in rows]

