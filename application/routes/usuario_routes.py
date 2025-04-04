from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from application.controllers.usuario_controller import (
    get_all_users_controller,
    get_user_by_id_controller,
    update_user_controller,
    delete_user_controller
)
from infrastructure.schemas.usuario import UsuarioResponse
from application.dependencies.auth_dependency import get_db_factory
from application.helpers.response_handler import success_response, error_response

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=list[UsuarioResponse])
def get_all_users(db: Session = Depends(get_db_factory("rrhh"))):
    try:
        users = get_all_users_controller(db)
        encoded_users = jsonable_encoder(users)
        return success_response("Usuarios encontrados", data=encoded_users)
    except Exception as e:
        return error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.get("/{user_id}", response_model=UsuarioResponse)
def get_user(user_id: int, db: Session = Depends(get_db_factory("rrhh"))):
    try:
        user = get_user_by_id_controller(user_id, db)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        encoded_user = jsonable_encoder(user)
        return success_response("Usuario encontrado", data=encoded_user)
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.put("/{user_id}", response_model=UsuarioResponse)
def update_user(user_id: int, update_data: dict = Body(...), db: Session = Depends(get_db_factory("rrhh"))):
    try:
        updated_user = update_user_controller(user_id, update_data, db)
        encoded_user = jsonable_encoder(updated_user)
        return success_response("Usuario actualizado", data=encoded_user)
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db_factory("rrhh"))):
    try:
        result = delete_user_controller(user_id, db)
        encoded_result = jsonable_encoder(result)
        return success_response("Usuario eliminado exitosamente", data=encoded_result)
    except HTTPException as he:
        raise he
    except Exception as e:
        return error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
