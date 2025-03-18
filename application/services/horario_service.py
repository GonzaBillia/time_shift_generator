# src/application/services/horarios_service.py
from typing import List
from datetime import time, date
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
    Crea en bloque los bloques horarias asociados a puestos ya creados.
    Se espera que cada objeto del front contenga 'puesto_id', 'hora_inicio', 'hora_fin' y 'horario_corrido'.
    """
    horarios_instanciados: List[HorarioORM] = []
    for item in horarios_front:
        horario = HorarioORM(
            puesto_id=item.get("puesto_id"),
            hora_inicio=item.get("hora_inicio"),
            hora_fin=item.get("hora_fin"),
            horario_corrido=item.get("horario_corrido", False)
        )
        horarios_instanciados.append(horario)

    if not horarios_instanciados:
        return []

    # Se determina la sucursal a partir del puesto.
    # Aquí podemos obtener el puesto del primer horario (asumiendo que la relación está cargada)
    # O alternativamente, hacer una consulta:
    puesto_id = horarios_instanciados[0].puesto_id
    puesto = PuestoRepository.get_by_id(puesto_id)
    sucursal_id = puesto.sucursal_id if puesto else None

    if sucursal_id:
        horarios_sucursal = obtener_horarios_sucursal(sucursal_id, db)
        errores_validacion = validar_horarios_dentro_sucursal(horarios_instanciados, horarios_sucursal)
        if errores_validacion:
            error_message = "Errores en los siguientes bloques:\n" + "\n".join(errores_validacion)
            raise ValueError(error_message)
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