from typing import List
from sqlalchemy.orm import Session
from infrastructure.repositories.usuario_repo import UsuarioRepository
from infrastructure.databases.models.usuario import Usuario
from infrastructure.schemas.usuario import UsuarioCreate
from application.services.auth_service import get_password_hash

def register_user(user_data: UsuarioCreate, db: Session) -> Usuario:
    # Valida si ya existe el usuario
    if UsuarioRepository.get_by_username(db, user_data.username):
        raise ValueError("El usuario ya existe")
    
    # Crea la instancia de Usuario y hashea la contraseña
    new_user = Usuario(
        colaborador_id=user_data.colaborador_id,
        username=user_data.username,
        password_hash=get_password_hash(user_data.password),
        rol_usuario_id=user_data.rol_usuario_id
    )
    return UsuarioRepository.create(db, new_user)

def update_user(user_id: int, update_data: dict, db: Session) -> Usuario:
    user = UsuarioRepository.get_by_id(db, user_id)
    if not user:
        raise ValueError("Usuario no encontrado")
    for key, value in update_data.items():
        setattr(user, key, value)
    return UsuarioRepository.update(db, user)

def delete_user(user_id: int, db: Session) -> None:
    user = UsuarioRepository.get_by_id(db, user_id)
    if not user:
        raise ValueError("Usuario no encontrado")
    UsuarioRepository.delete(db, user)

def get_user_by_id(user_id: int, db: Session) -> Usuario:
    user = UsuarioRepository.get_by_id(db, user_id)
    if not user:
        raise ValueError("Usuario no encontrado")
    return user

def get_all_users(db: Session) -> List[Usuario]:
    return UsuarioRepository.get_all(db)
