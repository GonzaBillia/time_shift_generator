from fastapi import Depends, HTTPException, status, Request

def require_roles(*roles: str):
    def role_checker(request: Request):
        user = getattr(request.state, "user", None)
        if not user or user.rol_usuario.nombre not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos")
        return user
    return role_checker

