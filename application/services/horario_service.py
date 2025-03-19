# src/application/services/horarios_service.py
from typing import List
from datetime import time, date
from collections import defaultdict
from domain.models.horario import Horario
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
        horario = HorarioORM(
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
    HorarioRepository.bulk_crear_horarios(horarios_instanciados)

    return horarios_instanciados

def actualizar_horarios(horarios_front: list, db=None) -> List[HorarioORM]:
    """
    Actualiza en bloque los bloques horarias existentes.
    Se espera que cada objeto en 'horarios_front' contenga 'id' y 'puesto_id' junto con la información de hora_inicio, hora_fin, etc.
    """
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
        horarios_instanciados.append(horario)

    if not horarios_instanciados:
        return []

    # Validación similar: obtener la sucursal desde el puesto
    puesto = PuestoRepository.get_by_id(horarios_instanciados[0].puesto_id)
    sucursal_id = puesto.sucursal_id if puesto else None
    if sucursal_id:
        horarios_sucursal = obtener_horarios_sucursal(sucursal_id, db)
        errores_validacion = validar_horarios_dentro_sucursal(horarios_instanciados, horarios_sucursal)
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