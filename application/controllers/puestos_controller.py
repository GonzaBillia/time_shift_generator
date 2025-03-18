from fastapi import HTTPException
from typing import List, Optional
import logging
from sqlalchemy.orm import Session
from application.services.puestos_service import crear_puesto, actualizar_puesto, delete_multiple_puestos, create_multiple_puestos, obtener_puestos_por_sucursal
from infrastructure.schemas.puestos import PuestoBase, PuestoUpdate, PuestoResponse
from infrastructure.databases.models.puestos import Puesto
from infrastructure.repositories.horario_repo import HorarioRepository

logger = logging.getLogger(__name__)

def controlador_py_logger_crear_puesto(puesto_data: dict) -> PuestoResponse:
    """
    Crea un puesto nuevo utilizando la lógica del servicio.
    Se espera que 'puesto_data' contenga: sucursal_id, rol_colaborador_id, dia_id, fecha, nombre y opcionalmente colaborador_id.
    """
    try:
        puesto = crear_puesto(
            sucursal_id=puesto_data["sucursal_id"],
            rol_colaborador_id=puesto_data["rol_colaborador_id"],
            dia_id=puesto_data["dia_id"],
            fecha=puesto_data["fecha"],
            nombre=puesto_data["nombre"],
            colaborador_id=puesto_data.get("colaborador_id")
        )
        logger.info("Puesto creado exitosamente con id %s", puesto.id)
        return puesto
    except Exception as error:
        logger.error("Error al crear puesto: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_crear_varios_puestos(puestos_data: List[dict], db: Optional[Session] = None) -> List[PuestoResponse]:
    """
    Crea múltiples puestos utilizando la lógica del servicio.
    Se espera que cada diccionario en 'puestos_data' contenga: 
    sucursal_id, rol_colaborador_id, dia_id, fecha, nombre y opcionalmente colaborador_id.
    """
    try:
        # Convertir cada diccionario a una instancia del modelo Puesto
        puesto_objs = [Puesto(**p) for p in puestos_data]
        puestos = create_multiple_puestos(puesto_objs, db)  # Asumiendo que este service espera modelos
        logger.info("Se crearon %d puestos exitosamente", len(puestos))
        return puestos
    except Exception as error:
        logger.error("Error al crear múltiples puestos: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_actualizar_puesto(puesto_data: dict) -> PuestoResponse:
    """
    Actualiza un puesto existente. Se espera que 'puesto_data' contenga el 'id' y los campos a modificar.
    """
    try:
        puesto = actualizar_puesto(puesto_data)
        logger.info("Puesto actualizado exitosamente con id %s", puesto.id)
        return puesto
    except Exception as error:
        logger.error("Error al actualizar puesto: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_obtener_puestos(sucursal_id: int) -> List[PuestoResponse]:
    """
    Retorna la lista de puestos de una sucursal.
    """
    try:
        puestos = obtener_puestos_por_sucursal(sucursal_id)
        logger.info("Se obtuvieron %d puestos para sucursal %s", len(puestos), sucursal_id)
        return puestos
    except Exception as error:
        logger.error("Error al obtener puestos: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error

def controlador_py_logger_eliminar_varios_puestos(puesto_ids: List[int], db: Session) -> None:
    """
    Elimina múltiples puestos y, previamente, elimina los horarios asociados a cada puesto.
    Se espera una lista de IDs de puestos.
    """
    try:
        # Recopilar los IDs de todos los horarios asociados a los puestos a eliminar.
        all_horario_ids = []
        for puesto_id in puesto_ids:
            horarios = HorarioRepository.get_by_puesto(puesto_id, db)
            all_horario_ids.extend([horario.id for horario in horarios])
        
        # Si se encontraron horarios asociados, eliminarlos.
        if all_horario_ids:
            deleted = HorarioRepository.delete_many(all_horario_ids)
            logger.info("Se eliminaron %d horarios asociados", len(all_horario_ids))
        else:
            logger.info("No se encontraron horarios asociados a eliminar.")
        
        # Eliminar los puestos
        delete_multiple_puestos(puesto_ids, db)
        logger.info("Se eliminaron %d puestos", len(puesto_ids))
    except Exception as error:
        logger.error("Error al eliminar puestos y horarios: %s", error)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from error