from fastapi import APIRouter, Depends, Response
from fastapi.security import OAuth2PasswordRequestForm
from application.controllers.auth_controller import login, logout, profile, register
from infrastructure.schemas.usuario import UsuarioCreate

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/token")
def token_endpoint(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    return login(response, form_data)

@router.post("/logout")
def logout_endpoint(response: Response):
    return logout(response)

@router.get("/profile")
def profile_endpoint(current_user=Depends(profile)):
    # La dependencia get_current_user_from_cookie se ejecuta internamente en profile()
    return profile()

@router.post("/register")
def register_endpoint(response: Response, user_data: UsuarioCreate):
    return register(response, user_data)
