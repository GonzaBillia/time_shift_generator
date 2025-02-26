from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from application.config.logger_config import setup_logger
from application.controllers.colaborador_controller import controlador_py_logger_get_all, controlador_py_logger_get_filtered, controlador_py_logger_get_by_id, controlador_py_logger_get_by_legajo
from application.helpers.response_handler import error_response, success_response
from infrastructure.schemas.colaborador import ColaboradorResponse

logger = setup_logger(__name__, "logs/colaboradores.log")
router = APIRouter(prefix="/colaboradores", tags=["Colaboradores"])

@router.get("/all", response_model=List[ColaboradorResponse])
def get_all_colaboradores():
    """
    Endpoint para obtener todos los colaboradores.
    """
    try:
        colaboradores = controlador_py_logger_get_all()
        colaboradores_schema = [ColaboradorResponse.model_validate(c) for c in colaboradores]
        data = [cs.model_dump() for cs in colaboradores_schema]
        return success_response("Colaboradores encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=500)

@router.get("/filters", response_model=List[ColaboradorResponse])
def search_colaboradores(
    dni: Optional[int] = Query(None, description="DNI del colaborador"),
    empresa_id: Optional[int] = Query(None, description="ID de la empresa"),
    tipo_empleado_id: Optional[int] = Query(None, description="ID del tipo de empleado"),
    horario_corrido: Optional[bool] = Query(None, description="Indica si el colaborador tiene horario corrido")
):
    """
    Endpoint para obtener colaboradores filtrados por DNI, empresa, tipo de empleado y horario corrido.
    Todos los parámetros son opcionales y se combinan para filtrar los resultados.
    """
    logger.info("Endpoint /filters accedido con parámetros: dni=%s, empresa_id=%s, tipo_empleado_id=%s, horario_corrido=%s", 
        dni, empresa_id, tipo_empleado_id, horario_corrido)
    try:
        colaboradores = controlador_py_logger_get_filtered(
            dni=dni,
            empresa_id=empresa_id,
            tipo_empleado_id=tipo_empleado_id,
            horario_corrido=horario_corrido,
        )
        colaboradores_schema = [ColaboradorResponse.model_validate(c) for c in colaboradores]
        data = [cs.model_dump() for cs in colaboradores_schema]
        return success_response("Colaboradores filtrados encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=500)

@router.get("/id/{colaborador_id}", response_model=ColaboradorResponse)
def get_colaborador(colaborador_id: int):
    """
    Endpoint para obtener la información de un colaborador por ID.
    
    Se utiliza el controlador 'controlador_py_logger_get_by_id' para recuperar
    el colaborador, se valida y se transforma en un esquema Pydantic y se retorna
    en un formato de respuesta estandarizado.
    """
    try:
        # Recupera el colaborador usando el controlador con logging
        colaborador = controlador_py_logger_get_by_id(colaborador_id)
        # Valida y transforma la instancia en un esquema Pydantic usando model_validate (Pydantic v2)
        colaborador_schema = ColaboradorResponse.model_validate(colaborador)
        # Convierte el esquema a dict y retorna la respuesta exitosa
        return success_response("Colaborador encontrado", data=colaborador_schema.model_dump())
    except HTTPException as he:
        # Propaga las excepciones HTTP (404, 500, etc.) generadas en el controlador
        raise he
    except Exception as e:
        # Para otras excepciones inesperadas, retorna una respuesta de error con status 500
        return error_response(str(e), status_code=500)


@router.get("/legajo/{colaborador_legajo}", response_model=ColaboradorResponse)
def get_colaborador_by_legajo(colaborador_legajo: int):
    """
    Endpoint para obtener un colaborador por legajo.
    """
    try:
        colaborador = controlador_py_logger_get_by_legajo(colaborador_legajo)
        colaborador_schema = ColaboradorResponse.model_validate(colaborador)
        return success_response("Colaborador encontrado", data=colaborador_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=500)

