import jwt, os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi import HTTPException, status
from infrastructure.repositories.usuario_repo import UsuarioRepository

ENV_FILE = ".env"
load_dotenv(ENV_FILE)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(username: str, password: str):
    user = UsuarioRepository.get_by_username(username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes= int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, os.getenv("SECRET_KEY"), algorithm= os.getenv("ALGORITHM"))
    return token
