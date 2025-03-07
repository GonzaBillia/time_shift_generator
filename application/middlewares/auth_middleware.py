from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException, status
import jwt, os
from dotenv import load_dotenv
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.usuario import Usuario

ENV_FILE = ".env"
load_dotenv(ENV_FILE)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Rutas públicas que no requieren autenticación
        if request.url.path in ["/auth/token", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        auth_header = request.headers.get("Authorization")
        if auth_header:
            try:
                token = auth_header.split(" ")[1]
                payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
                user_id = payload.get("sub")
                if not user_id:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
                db = Database.get_session("default")
                user = db.query(Usuario).filter(Usuario.id == int(user_id)).first()
                db.close()
                if not user:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
                # Se asigna el usuario al estado de la request
                request.state.user = user
            except Exception:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No se proporcionó token")
        response = await call_next(request)
        return response
