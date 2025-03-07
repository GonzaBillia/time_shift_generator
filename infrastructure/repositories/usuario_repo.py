from typing import Optional
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.usuario import Usuario

class UsuarioRepository:
    @staticmethod
    def get_by_username(username: str) -> Optional[Usuario]:
        session: Session = Database.get_session("default")
        usuario = session.query(Usuario).filter_by(username=username).first()
        session.close()
        return usuario

    @staticmethod
    def get_by_id(user_id: int) -> Optional[Usuario]:
        session: Session = Database.get_session("default")
        usuario = session.query(Usuario).filter_by(id=user_id).first()
        session.close()
        return usuario
