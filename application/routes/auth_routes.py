from typing import Any, Optional
from fastapi import APIRouter, Depends, Response, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from application.controllers.auth_controller import login, logout, register
from application.dependencies.auth_dependency import get_current_user_from_cookie
from application.dependencies.roles_dependency import require_roles
from infrastructure.schemas.usuario import UsuarioCreate
from application.helpers.response_handler import success_response, error_response
from application.config.logger_config import setup_logger

router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = setup_logger(__name__, "logs/auth.log")

@router.post("/login")
def token_endpoint(response: Response, form_data: OAuth2PasswordRequestForm = Depends()) -> Any:
    """
    Endpoint para autenticar al usuario y obtener el token.
    """
    try:
        result = login(response, form_data)
        response.status_code = status.HTTP_200_OK
        return {
            "success": True,
            "message": "Login exitoso",
            "statusCode": status.HTTP_200_OK,
            "data": result
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en token_endpoint: %s", e)
        return error_response(str(e), status_code=500)

from starlette.responses import JSONResponse

@router.post("/logout")
def logout_endpoint(response: Response) -> Any:
    """
    Endpoint para cerrar la sesión del usuario.
    """
    try:
        logout(response)
        # Creamos un JSONResponse que incluya el header de la cookie borrada.
        headers = dict(response.headers)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"success": True, "message": "Logout exitoso", "data": {"message": "Logout exitoso"}},
            headers=headers
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en logout_endpoint: %s", e)
        return error_response(str(e), status_code=500)


@router.get("/profile")
def profile_endpoint(current_user=Depends(get_current_user_from_cookie)) -> Any:
    """
    Endpoint para obtener el perfil del usuario autenticado.
    """
    try:
        result = {
            "user_id": current_user.id,
            "username": current_user.username,
            "rol": current_user.rol_usuario.nombre
        }
        return success_response("Perfil obtenido", data=result)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en profile_endpoint: %s", e)
        return error_response(str(e), status_code=500)


@router.post("/register")
def register_endpoint(
    user_data: UsuarioCreate,
    current_user=Depends(require_roles("superadmin"))
) -> Any:
    """
    Endpoint para registrar un nuevo usuario. Solo puede acceder un superadmin.
    """
    try:
        result = register(user_data)
        return success_response("Usuario registrado exitosamente", data=result)
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error("Error en register_endpoint: %s", e)
        return error_response(str(e), status_code=500)
