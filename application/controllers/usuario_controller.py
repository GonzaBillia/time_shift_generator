from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from application.services.usuario_service import (
    get_all_users_paginated,
    get_user_by_id,
    update_user,
    delete_user
)

def get_all_users_paginated_controller(page: int, limit: int, search: str, db: Session):
    try:
        users = get_all_users_paginated(db, page, limit, search)
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def get_user_by_id_controller(user_id: int, db: Session):
    try:
        user = get_user_by_id(user_id, db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def update_user_controller(user_id: int, update_data: dict, db: Session):
    try:
        user = update_user(user_id, update_data, db)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

def delete_user_controller(user_id: int, db: Session):
    try:
        delete_user(user_id, db)
        return {"message": "Usuario eliminado exitosamente"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
