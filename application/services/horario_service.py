from typing import List
from datetime import time, date, datetime, timedelta
from collections import defaultdict
import os

import pandas as pd

from domain.models.horario import Horario
from infrastructure.schemas.horario import HorarioBase
from infrastructure.databases.models.horario import Horario as HorarioORM
from infrastructure.databases.models.horario_sucursal import HorarioSucursal
from infrastructure.repositories.horario_repo import HorarioRepository
from application.services.horario_sucursal_service import obtener_horarios_sucursal
from infrastructure.repositories.puesto_repo import PuestoRepository  # Si necesitas obtener datos del puesto


def convertir_horario_a_dict(horario: HorarioORM, id_val: int = 0) -> dict:
    """
    Convierte un objeto Horario (que ahora tiene puesto_id) a un diccionario para persistencia.
    """
    return {
        "id": id_val,
        "puesto_id": horario.puesto_id,
        "hora_inicio": horario.hora_inicio.isoformat() if hasattr(horario.hora_inicio, "isoformat") else horario.hora_inicio,
        "hora_fin": horario.hora_fin.isoformat() if hasattr(horario.hora_fin, "isoformat") else horario.hora_fin,
        "horario_corrido": horario.horario_corrido,
    }


def validar_horarios_dentro_sucursal(horarios: List[HorarioORM], horarios_sucursal: List[HorarioSucursal]) -> List[str]:
    """
    Valida que la hora_inicio y hora_fin de cada bloque se encuentren dentro del rango
    de apertura y cierre del horario de la sucursal para el día correspondiente.
    Se asume que 'horarios_sucursal' es la lista completa de HorarioSucursal.
    """
    errores: List[str] = []
    # Se construye un diccionario indexado por día (usando el dia_id del puesto)
    horarios_sucursal_dict = {}
    for hs in horarios_sucursal:
        horarios_sucursal_dict[hs.dia_id] = (hs.hora_apertura, hs.hora_cierre)
    
    for h in horarios:
        # Para obtener el día y la sucursal, se puede intentar acceder a la relación "puesto"
        # Si no está cargada, se puede hacer una consulta (aquí se asume que la relación está configurada).
        dia_id = h.puesto.dia_id if h.puesto and hasattr(h.puesto, "dia_id") else None
        if not dia_id:
            errores.append(f"No se pudo determinar el día del puesto con id {h.puesto_id}.")
            continue

        rango = horarios_sucursal_dict.get(dia_id)
        if not rango:
            errores.append(f"No se encontró horario de sucursal para el día del puesto con id {h.puesto_id}.")
            continue
        apertura, cierre = rango
        if h.hora_inicio < apertura or h.hora_fin > cierre:
            errores.append(
                f"El bloque del puesto {h.puesto_id} tiene hora_inicio {h.hora_inicio} y hora_fin {h.hora_fin}, "
                f"fuera del rango de apertura ({apertura}) y cierre ({cierre})."
            )
    return errores


def crear_horarios(horarios_front: list, db=None) -> List[HorarioORM]:
    """
    Crea en bloque los horarios asociados a puestos ya creados y los valida individualmente.
    """
    if not horarios_front:
        return []

    horarios_instanciados: List[HorarioORM] = []

    # Crear horarios instanciados y obtener puesto_ids únicos
    puestos_ids = set()
    for item in horarios_front:
        item.pop("id", None)  # Elimina 'id' si existe para evitar que se asigne 0
        horario = HorarioORM(
            id=None,
            puesto_id=item["puesto_id"],
            hora_inicio=item["hora_inicio"],
            hora_fin=item["hora_fin"],
            horario_corrido=item.get("horario_corrido", False)
        )
        horarios_instanciados.append(horario)
        puestos_ids.add(item["puesto_id"])

    # Obtener información completa de los puestos involucrados
    puestos = PuestoRepository.get_by_ids(list(puestos_ids))
    puestos_dict = {puesto.id: puesto for puesto in puestos}

    # Agrupar horarios por sucursal_id para validar más eficientemente
    horarios_por_sucursal = defaultdict(list)

    errores_validacion = []

    for horario in horarios_instanciados:
        puesto = puestos_dict.get(horario.puesto_id)
        
        if not puesto:
            errores_validacion.append(f"Puesto con id {horario.puesto_id} no encontrado.")
            continue

        sucursal_id = puesto.sucursal_id
        dia_id = puesto.dia_id

        if not sucursal_id or not dia_id:
            errores_validacion.append(f"Puesto {horario.puesto_id} no tiene sucursal o día definido.")
            continue

        # Asignar temporalmente atributos para validación
        horario.puesto = puesto  # Importante para validación posterior
        horarios_por_sucursal[sucursal_id].append(horario)

    # Validar horarios por sucursal
    for sucursal_id, horarios in horarios_por_sucursal.items():
        horarios_sucursal = obtener_horarios_sucursal(sucursal_id, db)
        errores = validar_horarios_dentro_sucursal(horarios, horarios_sucursal)
        errores_validacion.extend(errores)

    if errores_validacion:
        error_message = "Errores en los siguientes bloques:\n" + "\n".join(errores_validacion)
        raise ValueError(error_message)

    # Guardar horarios si no hay errores
    hrs = HorarioRepository.bulk_crear_horarios(horarios_instanciados)

    return hrs


def actualizar_horarios(horarios_front: list, db=None) -> List[HorarioORM]:
    """
    Actualiza en bloque los bloques horarias existentes.
    Se espera que cada objeto en 'horarios_front' contenga 'id' y 'puesto_id'
    junto con la información de hora_inicio, hora_fin, etc.
    """
    from collections import defaultdict

    horarios_instanciados: List[HorarioORM] = []
    for item in horarios_front:
        if not item.get("id"):
            raise ValueError("El bloque a actualizar debe tener un 'id'.")
        horario = HorarioORM(
            id=item.get("id"),
            puesto_id=item.get("puesto_id"),
            hora_inicio=item.get("hora_inicio"),
            hora_fin=item.get("hora_fin"),
            horario_corrido=item.get("horario_corrido", False)
        )
        # Obtener y asignar el puesto correspondiente
        puesto = PuestoRepository.get_by_id(horario.puesto_id)
        if puesto:
            horario.puesto = puesto
        else:
            raise ValueError(f"Puesto con id {horario.puesto_id} no encontrado.")
        horarios_instanciados.append(horario)

    if not horarios_instanciados:
        return []

    # Agrupar los horarios por sucursal
    horarios_por_sucursal = defaultdict(list)
    for horario in horarios_instanciados:
        if horario.puesto and horario.puesto.sucursal_id:
            horarios_por_sucursal[horario.puesto.sucursal_id].append(horario)
        else:
            raise ValueError(f"No se encontró la sucursal para el puesto con id {horario.puesto_id}.")

    errores_validacion = []
    # Validar cada grupo de horarios según el rango de horarios de su sucursal
    for sucursal_id, horarios in horarios_por_sucursal.items():
        horarios_sucursal = obtener_horarios_sucursal(sucursal_id, db)
        errores = validar_horarios_dentro_sucursal(horarios, horarios_sucursal)
        errores_validacion.extend(errores)

    if errores_validacion:
        error_message = "Errores en los siguientes bloques:\n" + "\n".join(errores_validacion)
        raise ValueError(error_message)

    HorarioRepository.bulk_actualizar_horarios(horarios_instanciados)
    return horarios_instanciados


def crear_horario_preferido(
    sucursal_id: int,
    colaborador_id: int,
    dia_id: int,
    hora_inicio: time,
    hora_fin: time,
    horario_corrido: bool
) -> Horario:
    bloques = [(hora_inicio, hora_fin)]
    return Horario(
        sucursal_id=sucursal_id,
        colaborador_id=colaborador_id,
        dia_id=dia_id,
        fecha=None,  # Horario preferido sin fecha específica.
        bloques=bloques,
        horario_corrido=horario_corrido
    )


def crear_horario(
    sucursal_id: int,
    colaborador_id: int,
    dia_id: int,
    fecha: date,
    hora_inicio: time,
    hora_fin: time,
    horario_corrido: bool
) -> Horario:
    bloques = [(hora_inicio, hora_fin)]
    return Horario(
        sucursal_id=sucursal_id,
        colaborador_id=colaborador_id,
        dia_id=dia_id,
        fecha=fecha,
        bloques=bloques,
        horario_corrido=horario_corrido
    )


# -------------------------------
# Funciones para la generación de Excel
# -------------------------------

# Mapeo de dia_id a nombre de día (1: Lunes, 2: Martes, …, 7: Domingo)
DIA_NOMBRES = {
    1: "Lunes",
    2: "Martes",
    3: "Miércoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sábado",
    7: "Domingo"
}


def _dividir_por_semanas(fecha_inicio: datetime, fecha_fin: datetime) -> List[tuple]:
    """
    Divide el rango [fecha_inicio, fecha_fin] en tuplas (inicio, fin) de semanas completas (Lunes a Domingo).
    Se asume que la fecha de inicio es lunes y la fecha de fin es domingo para simplificar.
    """
    semanas = []
    current_start = fecha_inicio
    while current_start <= fecha_fin:
        current_end = current_start + timedelta(days=6)
        if current_end > fecha_fin:
            current_end = fecha_fin
        semanas.append((current_start, current_end))
        current_start = current_end + timedelta(days=1)
    return semanas


def _formatear_horarios(horarios: List[dict]) -> str:
    """
    Dado una lista de diccionarios con 'hora_inicio' y 'hora_fin',
    retorna una cadena con el formato "hora_inicio, hora_fin; hora_inicio, hora_fin".
    """
    return "; ".join([f"{h['hora_inicio']}, {h['hora_fin']}" for h in horarios])


def _generar_dataframe(colaboradores: List[dict]) -> pd.DataFrame:
    """
    Genera un DataFrame a partir de la lista de colaboradores, cada uno con su email y puestos.
    Se crea la columna 'Usuario' y una columna para cada día de la semana.
    """
    rows = []
    for col in colaboradores:
        # Se inicia cada fila con el email del colaborador
        row = {"Usuario": col["email"]}
        # Se inicializan las columnas para cada día de la semana
        for nombre in DIA_NOMBRES.values():
            row[nombre] = ""
        # Se recorren los puestos para agregar la información horaria en el día correspondiente
        for puesto in col.get("puestos", []):
            dia = DIA_NOMBRES.get(puesto.get("dia_id"))
            if dia:
                horarios_str = _formatear_horarios(puesto.get("horarios", []))
                if row[dia]:
                    row[dia] += "; " + horarios_str
                else:
                    row[dia] = horarios_str
        rows.append(row)
    return pd.DataFrame(rows)


def generar_excel_horarios(
    sucursal_ids: List[int],
    fecha_inicio: str,
    fecha_fin: str,
    separar_por_sucursal: bool = False,
    output_dir: str = None
) -> None:
    """
    Genera archivos Excel con la información de horarios obtenida del repositorio.

    - Se crea un archivo Excel por semana (el rango se debe dar en semanas completas: lunes a domingo).
    - Si 'separar_por_sucursal' es True, se crea un archivo por cada sucursal para cada semana.
    - El archivo contiene la primera columna "Usuario" (email del colaborador) y columnas
      para cada día de la semana (Lunes a Domingo) con los horarios formateados.
    - El rango de fechas se pasa como cadena en formato YYYY-MM-DD.
    """
    # Convertir las fechas de cadena a objetos date
    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
    fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d").date()

    # Dividir el rango en semanas; se asume que la fecha de inicio es lunes y la fecha de fin es domingo.
    semanas = _dividir_por_semanas(
        datetime.combine(fecha_inicio_dt, datetime.min.time()),
        datetime.combine(fecha_fin_dt, datetime.min.time())
    )

    # Directorio de salida: si no se pasa, se utiliza el directorio actual; de lo contrario, se crea si no existe.
    if output_dir is None:
        output_dir = os.getcwd()
    else:
        os.makedirs(output_dir, exist_ok=True)

    # Obtener los datos de horarios mediante el repositorio
    data = HorarioRepository.get_horarios_por_sucursales(sucursal_ids, fecha_inicio_dt, fecha_fin_dt)

    # Se organiza la información por sucursal
    sucursales_data = {}
    for sucursal in data.get("sucursales", []):
        sucursal_data = sucursal
        sucursales_data[sucursal_data["id"]] = sucursal_data

    # Para cada semana, generar el archivo Excel correspondiente
    for semana_idx, (sem_inicio, sem_fin) in enumerate(semanas, start=1):
        semana_str = f"{sem_inicio.date()}_al_{sem_fin.date()}"
        if separar_por_sucursal:
            # Se genera un archivo por sucursal para esta semana
            for sucursal in sucursales_data.values():
                colaboradores_filtrados = []
                for cs in sucursal.get("colaboradores", []):
                    colaborador_copy = cs.copy()
                    # Filtrar los puestos del colaborador que correspondan a la semana actual
                    puestos_semana = [
                        puesto for puesto in cs.get("puestos", [])
                        if sem_inicio.date() <= datetime.strptime(puesto["fecha"], "%Y-%m-%d").date() <= sem_fin.date()
                    ]
                    if puestos_semana:
                        colaborador_copy["puestos"] = puestos_semana
                        colaboradores_filtrados.append(colaborador_copy)
                df = _generar_dataframe(colaboradores_filtrados)
                file_name = f"sucursal_{sucursal['id']}_semana_{semana_str}.xlsx"
                file_path = os.path.join(output_dir, file_name)
                df.to_excel(file_path, index=False)
                print(f"Archivo generado: {file_path}")
        else:
            # Se genera un solo archivo consolidado para todas las sucursales en la semana actual
            colaboradores_totales = []
            for sucursal in sucursales_data.values():
                for cs in sucursal.get("colaboradores", []):
                    colaborador_copy = cs.copy()
                    puestos_semana = [
                        puesto for puesto in cs.get("puestos", [])
                        if sem_inicio.date() <= datetime.strptime(puesto["fecha"], "%Y-%m-%d").date() <= sem_fin.date()
                    ]
                    if puestos_semana:
                        colaborador_copy["puestos"] = puestos_semana
                        colaboradores_totales.append(colaborador_copy)
            df = _generar_dataframe(colaboradores_totales)
            file_name = f"horarios_semana_{semana_str}.xlsx"
            file_path = os.path.join(output_dir, file_name)
            df.to_excel(file_path, index=False)
            print(f"Archivo generado: {file_path}")
