from fastapi import APIRouter, HTTPException, Query, Body, Depends
from typing import List
from fastapi.encoders import jsonable_encoder
from starlette.responses import StreamingResponse
from io import BytesIO
import os
import tempfile
import zipfile
from datetime import datetime

from infrastructure.schemas.horario import (
    HorarioResponse, 
    HorarioBase, 
    HorarioUpdate, 
    HorarioDeleteRequest
)
from application.controllers.horario_controller import (
    controlador_py_logger_crear_horarios,
    controlador_py_logger_actualizar_horarios,
    controlador_py_logger_get_by_puesto,
    controlador_py_logger_delete_horarios,
    controlador_py_logger_get_by_puestos,
    controlador_py_logger_generar_excel_horarios
)
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

# Dependencias para autenticación y roles
from application.dependencies.auth_dependency import get_db_factory, get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles
from sqlalchemy.orm import Session

router = APIRouter(prefix="/horarios", tags=["Horarios"])
logger = setup_logger(__name__, "logs/horario.log")

@router.post("/crear", response_model=List[HorarioResponse])
def crear_horarios_endpoint(
    horarios_data: List[HorarioBase] = Body(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para crear en bloque los bloques horarias asociados a un puesto.
    Se espera una lista de HorarioBase (que contenga 'puesto_id', 'hora_inicio', 'hora_fin' y 'horario_corrido').
    """
    try:
        # Convertir cada esquema a diccionario
        horarios_front = [
            horario.model_dump() if hasattr(horario, "model_dump") else horario.dict()
            for horario in horarios_data
        ]
        resultados = controlador_py_logger_crear_horarios(horarios_front, db)
        resultados_encoded = jsonable_encoder(resultados)
        return success_response("Bloques horarias creados exitosamente", data=resultados_encoded)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en crear_horarios_endpoint: %s", e)
        return error_response(str(e), status_code=500)


@router.put("/actualizar", response_model=List[HorarioResponse])
def actualizar_horarios_endpoint(
    horarios_data: List[HorarioUpdate] = Body(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para actualizar en bloque los bloques horarias existentes.
    Se espera una lista de HorarioUpdate que incluya 'id' y 'puesto_id' junto con la información horaria.
    """
    try:
        horarios_front = [
            horario.model_dump() if hasattr(horario, "model_dump") else horario.dict()
            for horario in horarios_data
        ]
        resultados = controlador_py_logger_actualizar_horarios(horarios_front, db)
        resultados_encoded = jsonable_encoder(resultados)
        return success_response("Bloques horarias actualizados exitosamente", data=resultados_encoded)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en actualizar_horarios_endpoint: %s", e)
        return error_response(str(e), status_code=500)


@router.delete("/", response_model=dict)
def delete_horarios_endpoint(
    request: HorarioDeleteRequest = Body(...),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para eliminar en bloque los bloques horarias.
    Se espera un objeto con la lista de IDs a eliminar.
    """
    try:
        resultado = controlador_py_logger_delete_horarios(request.ids, db)
        return success_response("Bloques horarias eliminados exitosamente", data={"deleted": resultado})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en delete_horarios_endpoint: %s", e)
        return error_response(str(e), status_code=500)


@router.get("/puesto/{puesto_id}", response_model=List[HorarioResponse])
def get_horarios_by_puesto_id(
    puesto_id: int,
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todos los bloques horarias asociados a un puesto específico.
    """
    try:
        horarios = controlador_py_logger_get_by_puesto(puesto_id, db)
        horarios_schema = [HorarioResponse.model_validate(h) for h in horarios]
        data = [hs.model_dump() for hs in horarios_schema]
        return success_response("Bloques horarias para el puesto encontrados", data=jsonable_encoder(data))
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_puesto_id: %s", e)
        return error_response(str(e), status_code=500)
    

@router.get("/puestos", response_model=List[HorarioResponse])
def get_horarios_by_puestos(
    puesto_ids: List[int] = Query(..., alias="puesto_ids[]"),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para obtener todos los bloques horarias asociados a los puestos especificados.
    Se espera recibir los IDs en la query string, por ejemplo:
    /horarios/puestos?puesto_ids[]=37&puesto_ids[]=38
    """
    try:
        horarios = controlador_py_logger_get_by_puestos(puesto_ids, db)
        horarios_schema = [HorarioResponse.model_validate(h) for h in horarios]
        data = [hs.model_dump() for hs in horarios_schema]
        return success_response("Bloques horarias para el puesto encontrados", data=jsonable_encoder(data))
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en get_horarios_by_puestos: %s", e)
        return error_response(str(e), status_code=500)


@router.post("/excel/download", response_class=StreamingResponse)
def descargar_excel_horarios_endpoint(
    sucursal_ids: List[int] = Query(..., embed=True),
    fecha_inicio: str = Query(..., embed=True),
    fecha_fin: str = Query(..., embed=True),
    separar_por_sucursal: bool = Query(False, embed=True),
    db: Session = Depends(get_db_factory("rrhh")),
    current_user = Depends(get_current_user_from_cookie),
    role = Depends(require_roles("superadmin", "admin", "supervisor"))
):
    """
    Endpoint para generar y descargar archivos Excel con la información de horarios.
    Se espera:
      - sucursal_ids: lista de IDs de sucursales.
      - fecha_inicio y fecha_fin: rango de fechas en formato 'YYYY-MM-DD' (se asume un rango de lunes a domingo).
      - separar_por_sucursal: flag opcional para generar un archivo por sucursal.
    
    Se generan los archivos Excel en un directorio temporal, se comprimen en un ZIP y se retorna el contenido del ZIP.
    """
    try:
        # Crear un directorio temporal para almacenar los archivos Excel
        with tempfile.TemporaryDirectory() as temp_dir:
            # Llamar al controlador que genera los archivos Excel en el directorio temporal
            controlador_py_logger_generar_excel_horarios(sucursal_ids, fecha_inicio, fecha_fin, separar_por_sucursal, temp_dir, db)
            
            # Crear un archivo ZIP que contenga todos los archivos generados
            zip_filename = os.path.join(temp_dir, f"horarios_{datetime.now().strftime('%Y%m%d%H%M%S')}.zip")
            with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, _, files in os.walk(temp_dir):
                    for file in files:
                        if file.endswith(".xlsx"):
                            file_path = os.path.join(root, file)
                            zipf.write(file_path, arcname=file)
            
            # Leer el contenido del archivo ZIP en memoria
            with open(zip_filename, "rb") as f:
                zip_bytes = f.read()
        
        # Devolver el contenido del ZIP usando StreamingResponse
        zip_io = BytesIO(zip_bytes)
        headers = {"Content-Disposition": f"attachment; filename={os.path.basename(zip_filename)}"}
        return StreamingResponse(zip_io, media_type="application/x-zip-compressed", headers=headers)
    except Exception as e:
        logger.error("Error en descargar_excel_horarios_endpoint: %s", e)
        raise HTTPException(status_code=500, detail="Error interno del servidor") from e
