from typing import List
from fastapi import HTTPException
from application.config.logger_config import setup_logger
from infrastructure.databases.models.horario import Horario as HorarioORM
from infrastructure.repositories.horario_repo import HorarioRepository
from application.services.horario_service import crear_horarios, actualizar_horarios
from application.services.horario_service import generar_excel_horarios  # Se importa la función de Excel

logger = setup_logger(__name__, "logs/horario.log")


def controlador_py_logger_crear_horarios(horarios_front: List[dict], db=None) -> List[HorarioORM]:
    """
    Controlador para crear en bloque los bloques horarias (Horarios).
    Se espera una lista de diccionarios que contengan 'puesto_id', 'hora_inicio', 'hora_fin'
    y 'horario_corrido'.
    """
    try:
        resultados = crear_horarios(horarios_front, db)
        logger.info("Bloques horarias creados exitosamente.")
        return resultados
    except Exception as error:
        logger.error("Error al crear bloques horarias: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error


def controlador_py_logger_actualizar_horarios(horarios_front: List[dict], db=None) -> List[HorarioORM]:
    """
    Controlador para actualizar en bloque los bloques horarias existentes.
    Se espera que cada objeto incluya 'id' y 'puesto_id' junto con la información de hora_inicio, hora_fin y horario_corrido.
    """
    try:
        resultados = actualizar_horarios(horarios_front, db)
        logger.info("Bloques horarias actualizados exitosamente.")
        return resultados
    except Exception as error:
        logger.error("Error al actualizar bloques horarias: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error


def controlador_py_logger_get_by_puesto(puesto_id: int) -> List[HorarioORM]:
    """
    Devuelve todos los bloques horarias asociados a un puesto específico.
    """
    try:
        horarios = HorarioRepository.get_by_puesto(puesto_id)
    except Exception as error:
        logger.error("Error al obtener horarios para el puesto %s: %s", puesto_id, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not horarios:
        logger.warning("No se encontraron bloques horarias para el puesto %s", puesto_id)
        return []
    return horarios


def controlador_py_logger_get_by_puestos(puesto_ids: List[int]) -> List[HorarioORM]:
    """
    Devuelve todos los bloques horarias asociados a un conjunto de puestos.
    """
    try:
        horarios = HorarioRepository.get_by_puestos(puesto_ids)
    except Exception as error:
        logger.error("Error al obtener horarios para los puestos %s: %s", puesto_ids, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not horarios:
        return []
    return horarios


def controlador_py_logger_delete_horarios(horario_ids: list[int]) -> bool:
    """
    Elimina múltiples horarios según una lista de IDs proporcionados.
    Devuelve True si al menos un horario fue eliminado.
    """
    try:
        eliminado = HorarioRepository.delete_many(horario_ids)
    except Exception as error:
        logger.error("Error al eliminar horarios con IDs %s: %s", horario_ids, error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

    if not eliminado:
        logger.warning("No se encontraron horarios para eliminar con IDs %s", horario_ids)
        return False

    logger.info("Horarios eliminados correctamente con IDs %s", horario_ids)
    return True


def controlador_py_logger_generar_excel_horarios(
    sucursal_ids: List[int],
    fecha_inicio: str,
    fecha_fin: str,
    separar_por_sucursal: bool = False,
    output_dir: str = None
) -> dict:
    """
    Controlador para generar archivos Excel con la información de horarios.
    
    Parámetros:
      - sucursal_ids: Lista de IDs de sucursales.
      - fecha_inicio y fecha_fin: Rango de fechas en formato 'YYYY-MM-DD' (se espera un rango de lunes a domingo).
      - separar_por_sucursal: Flag para generar un archivo por sucursal por semana.
      - output_dir: Directorio de salida donde se guardarán los archivos.
    
    Retorna un diccionario con un mensaje de éxito.
    """
    try:
        generar_excel_horarios(sucursal_ids, fecha_inicio, fecha_fin, separar_por_sucursal, output_dir)
        logger.info("Archivos Excel generados exitosamente.")
        return {"message": "Archivos Excel generados exitosamente."}
    except Exception as error:
        logger.error("Error al generar archivos Excel: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error
