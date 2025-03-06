from fastapi import APIRouter, HTTPException
from typing import List
from fastapi.encoders import jsonable_encoder
from infrastructure.schemas.horario_preferido_colaborador import (
    HorarioPreferidoColaboradorResponse,
    HorarioPreferidoColaboradorBase,
    HorarioPreferidoColaboradorUpdate
)
from infrastructure.databases.models.horario_preferido_colaborador import HorarioPreferidoColaborador
from application.controllers.horario_preferido_colaborador_controller import (
    controlador_py_logger_get_by_id_horario_preferido_colaborador,
    controlador_py_logger_get_by_colaborador,
    controlador_py_logger_get_by_dia,
    controlador_py_logger_create_horario_preferido_colaborador,
    controlador_py_logger_update_horario_preferido_colaborador,
    controlador_py_logger_delete_horario_preferido_colaborador
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

router = APIRouter(prefix="/horarios_preferido_colaborador", tags=["Horarios Preferido Colaborador"])
logger = setup_logger(__name__, "logs/horario_preferido_colaborador.log")

@router.get("/id/{horario_id}", response_model=HorarioPreferidoColaboradorResponse)
def get_horario_preferido_colaborador_by_id(horario_id: int):
    """
    Endpoint para obtener un HorarioPreferidoColaborador por su ID.
    """
    try:
        horario = controlador_py_logger_get_by_id_horario_preferido_colaborador(horario_id)
        horario_schema = HorarioPreferidoColaboradorResponse.model_validate(horario)
        data = jsonable_encoder(horario_schema.model_dump())
        return success_response("HorarioPreferidoColaborador encontrado", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horario_preferido_colaborador_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/colaborador/{colaborador_id}", response_model=List[HorarioPreferidoColaboradorResponse])
def get_horarios_by_colaborador(colaborador_id: int):
    """
    Endpoint para obtener todos los HorarioPreferidoColaborador asociados a un colaborador.
    """
    try:
        horarios = controlador_py_logger_get_by_colaborador(colaborador_id)
        horarios_schema = [HorarioPreferidoColaboradorResponse.model_validate(h) for h in horarios]
        data = jsonable_encoder([hs.model_dump() for hs in horarios_schema])
        return success_response("Horarios preferidos encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_colaborador: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/dia/{dia_id}", response_model=List[HorarioPreferidoColaboradorResponse])
def get_horarios_by_dia(dia_id: int):
    """
    Endpoint para obtener todos los HorarioPreferidoColaborador para un día específico.
    """
    try:
        horarios = controlador_py_logger_get_by_dia(dia_id)
        horarios_schema = [HorarioPreferidoColaboradorResponse.model_validate(h) for h in horarios]
        data = jsonable_encoder([hs.model_dump() for hs in horarios_schema])
        return success_response("Horarios para el día encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_dia: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=HorarioPreferidoColaboradorResponse)
def create_horario_preferido_colaborador(horario_data: HorarioPreferidoColaboradorBase):
    """
    Endpoint para crear un nuevo HorarioPreferidoColaborador.
    """
    try:
        nuevo_horario = HorarioPreferidoColaborador(**horario_data.model_dump())
        creado = controlador_py_logger_create_horario_preferido_colaborador(nuevo_horario)
        horario_schema = HorarioPreferidoColaboradorResponse.model_validate(creado)
        data = jsonable_encoder(horario_schema.model_dump())
        return success_response("HorarioPreferidoColaborador creado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_horario_preferido_colaborador: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{horario_id}", response_model=HorarioPreferidoColaboradorResponse)
def update_horario_preferido_colaborador_partial(horario_id: int, horario_update: HorarioPreferidoColaboradorUpdate):
    """
    Endpoint para actualizar parcialmente un HorarioPreferidoColaborador.
    Solo se actualizarán los campos enviados.
    """
    try:
        # Recuperar la instancia actual para actualizar
        horario_actual = controlador_py_logger_get_by_id_horario_preferido_colaborador(horario_id)
        update_data = horario_update.dict(exclude_unset=True)
        
        for key, value in update_data.items():
            setattr(horario_actual, key, value)
        
        actualizado = controlador_py_logger_update_horario_preferido_colaborador(horario_actual)
        horario_schema = HorarioPreferidoColaboradorResponse.model_validate(actualizado)
        data = jsonable_encoder(horario_schema.model_dump())
        return success_response("HorarioPreferidoColaborador actualizado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_horario_preferido_colaborador_partial: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{horario_id}")
def delete_horario_preferido_colaborador(horario_id: int):
    """
    Endpoint para eliminar un HorarioPreferidoColaborador por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_horario_preferido_colaborador(horario_id)
        data = jsonable_encoder({"deleted": resultado})
        return success_response("HorarioPreferidoColaborador eliminado exitosamente", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_horario_preferido_colaborador: %s", e)
        return error_response(str(e), status_code=500)
