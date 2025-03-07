from fastapi import APIRouter, Body
from application.controllers.usuario_controller import (
    get_all_users_controller,
    get_user_by_id_controller,
    update_user_controller,
    delete_user_controller
)
from infrastructure.schemas.usuario import UsuarioResponse

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=list[UsuarioResponse])
def get_all_users():
    return get_all_users_controller()

@router.get("/{user_id}", response_model=UsuarioResponse)
def get_user(user_id: int):
    return get_user_by_id_controller(user_id)

@router.put("/{user_id}", response_model=UsuarioResponse)
def update_user(user_id: int, update_data: dict = Body(...)):
    return update_user_controller(user_id, update_data)

@router.delete("/{user_id}")
def delete_user(user_id: int):
    return delete_user_controller(user_id)
