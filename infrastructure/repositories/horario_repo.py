# horario_repo.py
from typing import List, Optional
from datetime import date, time
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario import Horario

class HorarioRepository:
    @staticmethod
    def get_by_id(horario_id: int) -> Optional[Horario]:
        """
        Obtiene un Horario por su ID.
        Retorna None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        horario = session.query(Horario).filter_by(id=horario_id).first()
        session.close()
        return horario

    @staticmethod
    def get_by_puesto(puesto_id: int, db: Optional[Session] = None) -> List[Horario]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horarios = db.query(Horario).filter_by(puesto_id=puesto_id).all()
            return horarios
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_colaborador(colaborador_id: int, db: Optional[Session] = None) -> List[Horario]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horarios = db.query(Horario).filter_by(colaborador_id=colaborador_id).all()
            return horarios
        finally:
            if close_session:
                db.close()


    @staticmethod
    def get_all() -> List[Horario]:
        """
        Devuelve todos los horarios registrados en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).all()
        session.close()
        return horarios

    @staticmethod
    def create(horario: Horario) -> Horario:
        """
        Crea un nuevo Horario y lo persiste en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(horario)
        session.commit()
        session.refresh(horario)
        session.close()
        return horario

    @staticmethod
    def update(horario: Horario) -> Optional[Horario]:
        """
        Actualiza un Horario existente.
        Recibe un objeto Horario con id,
        hace 'merge' en la sesión y lo refresca luego del commit.

        Retorna el Horario actualizado o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        # Verificamos si existe el objeto en la BD
        existente = session.query(Horario).filter_by(id=horario.id).first()
        if not existente:
            session.close()
            return None

        db_horario = session.merge(horario)  # Une los cambios al objeto en sesión
        session.commit()
        session.refresh(db_horario)
        session.close()
        return db_horario

    @staticmethod
    def delete(horario_id: int) -> bool:
        """
        Elimina un Horario de la base de datos por su ID.
        Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        horario = session.query(Horario).filter_by(id=horario_id).first()
        if horario:
            session.delete(horario)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @staticmethod
    def delete_many(horario_ids: list[int]) -> bool:
        """
        Elimina múltiples Horarios de la base de datos por sus IDs.
        Retorna True si se eliminó al menos uno, o False si ninguno fue encontrado.
        """
        session: Session = Database.get_session("rrhh")
        try:
            # Se filtran los horarios cuyos id estén en la lista
            query = session.query(Horario).filter(Horario.id.in_(horario_ids))
            if query.count() == 0:
                session.close()
                return False
            query.delete(synchronize_session=False)
            session.commit()
            return True
        finally:
            session.close()

    @staticmethod
    def bulk_crear_horarios(horarios: List[Horario]) -> List[Horario]:
        session: Session = Database.get_session("rrhh")
        session.add_all(horarios)
        session.commit()
        for horario in horarios:
            session.refresh(horario)
        result = horarios.copy()  # Copia de las instancias ya refrescadas
        session.close()
        return result

    @staticmethod
    def bulk_actualizar_horarios(horarios: List[Horario]) -> List[Horario]:
        session: Session = Database.get_session("rrhh")
        persisted_horarios = []
        for horario in horarios:
            # merge devuelve la instancia persistente asociada a la sesión.
            persisted = session.merge(horario)
            persisted_horarios.append(persisted)
        session.commit()
        for ph in persisted_horarios:
            session.refresh(ph)
        result = persisted_horarios.copy()
        session.close()
        return result

