from typing import Optional, List
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.usuario import Usuario

class UsuarioRepository:
    @staticmethod
    def get_by_username(username: str) -> Optional[Usuario]:
        session: Session = Database.get_session("rrhh")
        usuario = session.query(Usuario).filter_by(username=username).first()
        session.close()
        return usuario

    @staticmethod
    def get_by_id(user_id: int) -> Optional[Usuario]:
        session: Session = Database.get_session("rrhh")
        usuario = session.query(Usuario).filter_by(id=user_id).first()
        session.close()
        return usuario

    @staticmethod
    def get_all() -> List[Usuario]:
        session: Session = Database.get_session("rrhh")
        usuarios = session.query(Usuario).all()
        session.close()
        return usuarios

    @staticmethod
    def create(user: Usuario) -> Usuario:
        session: Session = Database.get_session("rrhh")
        session.add(user)
        session.commit()
        session.refresh(user)
        session.close()
        return user

    @staticmethod
    def update(user: Usuario) -> Usuario:
        session: Session = Database.get_session("rrhh")
        session.merge(user)
        session.commit()
        session.refresh(user)
        session.close()
        return user

    @staticmethod
    def delete(user: Usuario) -> None:
        session: Session = Database.get_session("rrhh")
        session.delete(user)
        session.commit()
        session.close()
