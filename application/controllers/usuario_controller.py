from fastapi import HTTPException, status
from application.services.usuario_service import (
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)
from application.helpers.response_handler import success_response, error_response

def get_all_users_controller():
    try:
        users = get_all_users()
        return success_response("Usuarios encontrados", data=users)
    except Exception as e:
        return error_response(str(e), status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

def get_user_by_id_controller(user_id: int):
    try:
        user = get_user_by_id(user_id)
        return success_response("Usuario encontrado", data=user)
    except ValueError as e:
        return error_response(str(e), status_code=404)
    except Exception as e:
        return error_response(str(e), status_code=500)

def update_user_controller(user_id: int, update_data: dict):
    try:
        user = update_user(user_id, update_data)
        return success_response("Usuario actualizado", data=user)
    except ValueError as e:
        return error_response(str(e), status_code=404)
    except Exception as e:
        return error_response(str(e), status_code=500)

def delete_user_controller(user_id: int):
    try:
        delete_user(user_id)
        return success_response("Usuario eliminado exitosamente")
    except ValueError as e:
        return error_response(str(e), status_code=404)
    except Exception as e:
        return error_response(str(e), status_code=500)
