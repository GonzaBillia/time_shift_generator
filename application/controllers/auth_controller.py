import os
from dotenv import load_dotenv
from fastapi import Depends, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from application.services.auth_service import authenticate_user, create_access_token
from application.services.usuario_service import register_user
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.schemas.usuario import UsuarioCreate
from application.dependencies.auth_dependency import get_current_user_from_cookie

ENV_FILE=".env"
load_dotenv(ENV_FILE)

def login(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    db: Session = Database.get_session("rrhh")
    user = authenticate_user(form_data.username, form_data.password)
    db.close()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": str(user.id), "token_version": user.token_version}
    )

    max_age = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "720")) * 60
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=max_age
    )

    return access_token

def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout exitoso"}


def register(user_data):
    try:
        # Registra el usuario sin auto-login ni setear cookie
        new_user = register_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "user_id": new_user.id,
        "username": new_user.username,
        "rol": new_user.rol_usuario.nombre
    }