from fastapi import HTTPException, status
from application.services.usuario_service import (
    get_all_users,
    get_user_by_id,
    update_user,
    delete_user
)

def get_all_users_controller():
    try:
        return get_all_users()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def get_user_by_id_controller(user_id: int):
    try:
        return get_user_by_id(user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def update_user_controller(user_id: int, update_data: dict):
    try:
        return update_user(user_id, update_data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def delete_user_controller(user_id: int):
    try:
        delete_user(user_id)
        return {"message": "Usuario eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
