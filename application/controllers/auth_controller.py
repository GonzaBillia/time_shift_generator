import os
from dotenv import load_dotenv
from fastapi import Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from application.services.auth_service import authenticate_user, create_access_token
from application.services.usuario_service import register_user
from infrastructure.schemas.usuario import UsuarioCreate

ENV_FILE = ".env"
load_dotenv(ENV_FILE)

def login(response: Response, form_data: OAuth2PasswordRequestForm, db: Session):
    # Se pasa la sesión al servicio de autenticación
    user = authenticate_user(db, form_data.username, form_data.password)
    
    access_token = create_access_token(
        db, data={"sub": str(user.id), "token_version": user.token_version}
    )
    
    max_age = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "720")) * 60
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=False,    # Configura True en producción si usas HTTPS
        samesite="lax",
        max_age=max_age
    )
    return access_token

def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logout exitoso"}

def register(user_data: UsuarioCreate, db: Session):
    try:
        new_user = register_user(user_data, db)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {
        "user_id": new_user.id,
        "username": new_user.username,
        "rol": new_user.rol_usuario.nombre
    }
