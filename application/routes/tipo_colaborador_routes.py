# ROUTER_PY_SCHEMA_TIPO_EMPLEADO
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from infrastructure.schemas.tipo_empleado import TipoEmpleadoResponse, TipoEmpleadoBase, TipoEmpleadoUpdate
from application.controllers.tipo_colaborador_controller import (
    controlador_py_logger_get_by_id_tipo_empleado,
    controlador_py_logger_get_all_tipo_empleado,
    controlador_py_logger_create_tipo_empleado,
    controlador_py_logger_update_tipo_empleado,
    controlador_py_logger_delete_tipo_empleado,
    controlador_py_logger_get_by_tipo_tipo_empleado
)
from infrastructure.databases.models.tipo_colaborador import TipoEmpleado
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

router = APIRouter(prefix="/tipo_colaboradores", tags=["TipoEmpleado"])
logger = setup_logger(__name__, "logs/tipo_empleado.log")

@router.get("/id/{tipo_empleado_id}", response_model=TipoEmpleadoResponse)
def get_tipo_empleado_by_id(tipo_empleado_id: int):
    """
    Endpoint para obtener un TipoEmpleado por su ID.
    """
    try:
        tipo = controlador_py_logger_get_by_id_tipo_empleado(tipo_empleado_id)
        tipo_schema = TipoEmpleadoResponse.model_validate(tipo)
        return success_response("TipoEmpleado encontrado", data=tipo_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_tipo_empleado_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/", response_model=List[TipoEmpleadoResponse])
def get_all_tipo_empleados():
    """
    Endpoint para obtener todos los tipos de empleados.
    """
    try:
        tipos = controlador_py_logger_get_all_tipo_empleado()
        tipos_schema = [TipoEmpleadoResponse.model_validate(t) for t in tipos]
        data = [ts.model_dump() for ts in tipos_schema]
        return success_response("Tipos de empleados encontrados", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_tipo_empleados: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=TipoEmpleadoResponse)
def create_tipo_empleado(tipo_data: TipoEmpleadoBase):
    """
    Endpoint para crear un nuevo TipoEmpleado.
    """
    try:
        # Convertir la entrada (TipoEmpleadoBase) en una instancia del modelo SQLAlchemy
        nuevo_tipo = TipoEmpleado(**tipo_data.model_dump())
        tipo_creado = controlador_py_logger_create_tipo_empleado(nuevo_tipo)
        tipo_schema = TipoEmpleadoResponse.model_validate(tipo_creado)
        return success_response("TipoEmpleado creado exitosamente", data=tipo_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_tipo_empleado: %s", e)
        return error_response(str(e), status_code=500)

@router.put("/{tipo_empleado_id}", response_model=TipoEmpleadoResponse)
def update_tipo_empleado_partial(tipo_empleado_id: int, tipo_update: TipoEmpleadoUpdate):
    """
    Endpoint para actualizar parcialmente un TipoEmpleado existente.
    Solo se actualizarán los campos que se envíen en el body.
    """
    try:
        # Recuperar el registro actual
        tipo_actual = controlador_py_logger_get_by_id_tipo_empleado(tipo_empleado_id)
        
        # Extraer los datos enviados (excluye los que no se establecieron)
        update_data = tipo_update.dict(exclude_unset=True)
        
        # Convertir el objeto actual a diccionario (excluyendo atributos internos)
        current_data = {
            "id": tipo_actual.id,
            "tipo": tipo_actual.tipo,
            "horas_por_dia_max": tipo_actual.horas_por_dia_max,
            "horas_semanales": tipo_actual.horas_semanales
        }
        
        # Actualizar los datos actuales con los nuevos valores
        current_data.update(update_data)
        
        # Crear una nueva instancia con los datos combinados
        tipo_to_update = TipoEmpleado(**current_data)
        
        # Llamar al controlador para actualizar
        tipo_actualizado = controlador_py_logger_update_tipo_empleado(tipo_to_update)
        
        # Validar y transformar a esquema de respuesta
        tipo_schema = TipoEmpleadoResponse.model_validate(tipo_actualizado)
        return success_response("TipoEmpleado actualizado exitosamente", data=tipo_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_tipo_empleado: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{tipo_empleado_id}")
def delete_tipo_empleado(tipo_empleado_id: int):
    """
    Endpoint para eliminar un TipoEmpleado por su ID.
    """
    try:
        resultado = controlador_py_logger_delete_tipo_empleado(tipo_empleado_id)
        return success_response("TipoEmpleado eliminado exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_tipo_empleado: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/tipo/{tipo}", response_model=TipoEmpleadoResponse)
def get_tipo_empleado_by_tipo(tipo: str):
    """
    Endpoint para obtener un TipoEmpleado por su campo 'tipo' (nombre).
    """
    try:
        tipo_empleado = controlador_py_logger_get_by_tipo_tipo_empleado(tipo)
        tipo_schema = TipoEmpleadoResponse.model_validate(tipo_empleado)
        return success_response("TipoEmpleado encontrado", data=tipo_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_tipo_empleado_by_tipo: %s", e)
        return error_response(str(e), status_code=500)
