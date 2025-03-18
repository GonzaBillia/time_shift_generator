from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from typing import List
from infrastructure.schemas.horario import (
    HorarioResponse, 
    HorarioBase, 
    HorarioUpdate, 
    HorarioDeleteRequest
)
from application.controllers.horario_controller import (
    controlador_py_logger_crear_horarios,
    controlador_py_logger_actualizar_horarios,
    controlador_py_logger_get_by_puesto
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

router = APIRouter(prefix="/horarios", tags=["Horarios"])
logger = setup_logger(__name__, "logs/horario.log")

@router.post("/crear", response_model=List[HorarioResponse])
def crear_horarios_endpoint(horarios_data: List[HorarioBase] = Body(...)):
    """
    Endpoint para crear en bloque los bloques horarias asociados a un puesto.
    Se espera una lista de HorarioBase (que contenga 'puesto_id', 'hora_inicio', 'hora_fin' y 'horario_corrido').
    """
    try:
        # Convertir cada esquema a diccionario
        horarios_front = [
            (horario.model_dump() if hasattr(horario, "model_dump") else horario.dict())
            for horario in horarios_data
        ]
        resultados = controlador_py_logger_crear_horarios(horarios_front)
        resultados_encoded = jsonable_encoder(resultados)
        return success_response("Bloques horarias creados exitosamente", data=resultados_encoded)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en crear_horarios_endpoint: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/actualizar", response_model=List[HorarioResponse])
def actualizar_horarios_endpoint(horarios_data: List[HorarioUpdate] = Body(...)):
    """
    Endpoint para actualizar en bloque los bloques horarias existentes.
    Se espera una lista de HorarioUpdate que incluya 'id' y 'puesto_id' junto con la información horaria.
    """
    try:
        horarios_front = [
            (horario.model_dump() if hasattr(horario, "model_dump") else horario.dict())
            for horario in horarios_data
        ]
        resultados = controlador_py_logger_actualizar_horarios(horarios_front)
        resultados_encoded = jsonable_encoder(resultados)
        return success_response("Bloques horarias actualizados exitosamente", data=resultados_encoded)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en actualizar_horarios_endpoint: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/", response_model=dict)
def delete_horarios_endpoint(request: HorarioDeleteRequest = Body(...)):
    """
    Endpoint para eliminar en bloque los bloques horarias.
    Se espera un objeto con la lista de IDs a eliminar.
    """
    try:
        # Asumimos que existe la función delete_many en el repositorio de horarios
        from application.controllers.horario_controller import controlador_py_logger_delete_horarios
        resultado = controlador_py_logger_delete_horarios(request.ids)
        return success_response("Bloques horarias eliminados exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_horarios_endpoint: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/puesto/{puesto_id}", response_model=List[HorarioResponse])
def get_horarios_by_puesto_id(puesto_id: int):
    """
    Endpoint para obtener todos los bloques horarias asociados a un puesto específico.
    """
    try:
        horarios = controlador_py_logger_get_by_puesto(puesto_id)
        # Convertir cada objeto a esquema de respuesta
        horarios_schema = [HorarioResponse.model_validate(h) for h in horarios]
        data = [hs.model_dump() for hs in horarios_schema]
        return success_response("Bloques horarias para el puesto encontrados", data=jsonable_encoder(data))
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_puesto_id: %s", e)
        return error_response(str(e), status_code=500)
