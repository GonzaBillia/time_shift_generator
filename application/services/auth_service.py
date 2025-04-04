import jwt, os, logging
from dotenv import load_dotenv
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from infrastructure.repositories.usuario_repo import UsuarioRepository

# Cargar variables de entorno y configurar logging
ENV_FILE = ".env"
load_dotenv(ENV_FILE)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(db: Session, username: str, password: str):
    """
    Autentica un usuario validando que exista, que la contraseña sea correcta
    y que el usuario esté activo. Además, actualiza last_login y token_version.
    """
    user = UsuarioRepository.get_by_username(db, username)
    if not user:
        logger.warning(f"Autenticación fallida: usuario '{username}' no encontrado.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    if not verify_password(password, user.password_hash):
        logger.warning(f"Autenticación fallida: contraseña incorrecta para el usuario '{username}'.")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    if not user.is_active:
        logger.warning(f"Autenticación fallida: el usuario '{username}' está inactivo.")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    # Actualizamos la información de login en la capa de repositorio
    user = UsuarioRepository.update_login_info(db, user)
    return user


def create_access_token(db: Session, data: dict) -> str:
    """
    Genera un JWT incluyendo el token_version del usuario y con un tiempo de expiración configurable.
    """
    # Verificar que SECRET_KEY esté definida
    secret_key = os.getenv("SECRET_KEY")
    if not secret_key:
        logger.error("La variable de entorno SECRET_KEY no está definida.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Configuración del servidor inválida"
        )
    algorithm = os.getenv("ALGORITHM", "HS256")
    
    # Se asegura que el token incluya el token_version del usuario, para poder invalidar tokens antiguos.
    token_version = data.get("token_version", 0)
    payload = data.copy()
    payload["token_version"] = token_version

    # Configuración del tiempo de expiración del token
    expire_minutes_str = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "15")
    try:
        expire_minutes = int(expire_minutes_str)
    except ValueError:
        logger.error("ACCESS_TOKEN_EXPIRE_MINUTES debe ser un entero válido.")
        expire_minutes = 15
    expire = datetime.utcnow() + timedelta(minutes=expire_minutes)
    payload.update({"exp": expire})

    try:
        token = jwt.encode(payload, secret_key, algorithm=algorithm)
    except Exception as e:
        logger.error(f"Error al generar el token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno al generar token"
        )
    return token
