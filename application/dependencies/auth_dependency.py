from fastapi import HTTPException, Request, status
import jwt, os
from typing import Generator, Callable
from dotenv import load_dotenv
from sqlalchemy.orm import joinedload, Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.usuario import Usuario

ENV_FILE = ".env"
load_dotenv(ENV_FILE)

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def get_current_user_from_cookie(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token no proporcionado")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    
    db = Database.get_session("rrhh")
    user = db.query(Usuario)\
             .options(joinedload(Usuario.rol_usuario))\
             .filter(Usuario.id == int(user_id))\
             .first()
    db.close()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")
    
    request.state.user = user
    return user

def get_db_factory(db_name: str) -> Callable[[], Generator[Session, None, None]]:
    def _get_db() -> Generator[Session, None, None]:
        session = Database.get_session(db_name)
        try:
            yield session
        finally:
            session.close()
    return _get_db