from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from infrastructure.databases.models.usuario import Usuario

class UsuarioRepository:
    @staticmethod
    def get_by_username(session: Session, username: str) -> Optional[Usuario]:
        return session.query(Usuario).filter_by(username=username).first()

    @staticmethod
    def get_by_id(session: Session, user_id: int) -> Optional[Usuario]:
        return session.query(Usuario).filter_by(id=user_id).first()

    @staticmethod
    def get_all(session: Session) -> List[Usuario]:
        return session.query(Usuario).all()

    @staticmethod
    def create(session: Session, user: Usuario) -> Usuario:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def update(session: Session, user: Usuario) -> Usuario:
        session.merge(user)
        session.commit()
        session.refresh(user)
        return user

    @staticmethod
    def delete(session: Session, user: Usuario) -> None:
        session.delete(user)
        session.commit()

    @staticmethod
    def update_login_info(session: Session, user: Usuario) -> Usuario:
        """
        Actualiza el campo last_login y aumenta la versión del token.
        """
        user.last_login = datetime.utcnow()
        user.token_version += 1
        session.commit()
        session.refresh(user)
        return user