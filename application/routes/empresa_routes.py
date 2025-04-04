from fastapi import APIRouter, HTTPException, Depends
from typing import List

from infrastructure.schemas.empresa import EmpresaResponse, EmpresaBase, EmpresaUpdate
from infrastructure.databases.models.empresa import Empresa
from application.controllers.empresa_controller import (
    controlador_py_logger_get_by_cuit,
    controlador_py_logger_get_by_id_empresa,
    controlador_py_logger_get_by_razon_social,
    controlador_py_logger_get_all_empresas,
    controlador_py_logger_create_empresa,
    controlador_py_logger_update_empresa,
    controlador_py_logger_delete_empresa
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles
from sqlalchemy.orm import Session

router = APIRouter(prefix="/empresas", tags=["Empresas"])
logger = setup_logger(__name__, "logs/empresa.log")

@router.get("/", response_model=List[EmpresaResponse])
def get_all_empresas(
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todas las empresas.
    """
    try:
        empresas = controlador_py_logger_get_all_empresas(db)
        empresas_schema = [EmpresaResponse.model_validate(e) for e in empresas]
        data = [es.model_dump() for es in empresas_schema]
        return success_response("Empresas encontradas", data=data)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_all_empresas: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/cuit/{cuit}", response_model=EmpresaResponse)
def get_empresa_by_cuit(
    cuit: str,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener una empresa por su CUIT.
    """
    try:
        empresa = controlador_py_logger_get_by_cuit(cuit, db)
        empresa_schema = EmpresaResponse.model_validate(empresa)
        return success_response("Empresa encontrada", data=empresa_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_empresa_by_cuit: %s", e)
        return error_response(str(e), status_code=500)
    
@router.get("/id/{empresa_id}", response_model=EmpresaResponse)
def get_empresa_by_id(
    empresa_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener una empresa por su ID.
    """
    try:
        empresa = controlador_py_logger_get_by_id_empresa(empresa_id, db)
        empresa_schema = EmpresaResponse.model_validate(empresa)
        return success_response("Empresa encontrada", data=empresa_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_empresa_by_id: %s", e)
        return error_response(str(e), status_code=500)

@router.get("/razon_social/{razon_social}", response_model=EmpresaResponse)
def get_empresa_by_razon_social(
    razon_social: str,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener una empresa por su razón social.
    """
    try:
        empresa = controlador_py_logger_get_by_razon_social(razon_social, db)
        empresa_schema = EmpresaResponse.model_validate(empresa)
        return success_response("Empresa encontrada", data=empresa_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_empresa_by_razon_social: %s", e)
        return error_response(str(e), status_code=500)

@router.post("/", response_model=EmpresaResponse)
def create_empresa(
    empresa_data: EmpresaBase,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para crear una nueva Empresa.
    
    Recibe un objeto EmpresaBase y lo transforma en una instancia de Empresa (modelo SQLAlchemy),
    luego llama al controlador para crear la empresa y retorna la respuesta con el formato estandarizado.
    """
    try:
        # Convertir la entrada (EmpresaBase) en una instancia del modelo SQLAlchemy
        nueva_empresa = Empresa(**empresa_data.model_dump())
        # Crear la empresa usando el controlador con logging
        empresa_creada = controlador_py_logger_create_empresa(nueva_empresa, db)
        # Validar y transformar la instancia creada en el esquema de respuesta
        empresa_schema = EmpresaResponse.model_validate(empresa_creada)
        return success_response("Empresa creada exitosamente", data=empresa_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en create_empresa: %s", e)
        return error_response(str(e), status_code=500)
    
@router.put("/{empresa_id}", response_model=EmpresaResponse)
def update_empresa_partial(
    empresa_id: int,
    empresa_update: EmpresaUpdate,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para actualizar parcialmente una Empresa.
    Solo se actualizarán los campos que se envíen en el body.
    """
    try:
        # Recuperar la empresa actual mediante su ID
        empresa_actual = controlador_py_logger_get_by_id_empresa(empresa_id, db)
        
        # Extraer los datos enviados; se excluyen aquellos que no se hayan enviado
        update_data = empresa_update.dict(exclude_unset=True)
        
        # Convertir el objeto actual en un diccionario
        current_data = {
            "id": empresa_actual.id,
            "razon_social": empresa_actual.razon_social,
            "cuit": empresa_actual.cuit,
        }
        
        # Actualizar los datos actuales con los nuevos valores
        current_data.update(update_data)
        
        # Crear una nueva instancia del modelo SQLAlchemy con los datos combinados
        empresa_to_update = Empresa(**current_data)
        
        # Actualizar la empresa usando el controlador con logging
        empresa_actualizada = controlador_py_logger_update_empresa(empresa_to_update, db)
        
        # Validar y transformar la instancia actualizada al esquema de respuesta
        empresa_schema = EmpresaResponse.model_validate(empresa_actualizada)
        return success_response("Empresa actualizada exitosamente", data=empresa_schema.model_dump())
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en update_empresa_partial: %s", e)
        return error_response(str(e), status_code=500)

@router.delete("/{empresa_id}")
def delete_empresa(
    empresa_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para eliminar una Empresa por su ID.
    
    Retorna una respuesta estandarizada indicando el resultado de la operación.
    """
    try:
        resultado = controlador_py_logger_delete_empresa(empresa_id, db)
        return success_response("Empresa eliminada exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_empresa: %s", e)
        return error_response(str(e), status_code=500)
