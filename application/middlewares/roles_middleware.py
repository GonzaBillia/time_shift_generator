from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException, status

class RolesMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Ejemplo: restringir rutas que comienzan con /admin
        if request.url.path.startswith("/admin"):
            user = getattr(request.state, "user", None)
            if not user or user.rol_usuario.nombre not in ["admin", "superadmin"]:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos")
        response = await call_next(request)
        return response
