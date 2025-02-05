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
    def get_by_sucursal(sucursal_id: int) -> List[Horario]:
        """
        Devuelve todos los horarios asociados a una Sucursal específica.
        """
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return horarios

    @staticmethod
    def get_by_colaborador(colaborador_id: int) -> List[Horario]:
        """
        Devuelve todos los horarios asociados a un Colaborador específico.
        """
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).filter_by(colaborador_id=colaborador_id).all()
        session.close()
        return horarios

    @staticmethod
    def get_by_fecha(fecha: date) -> List[Horario]:
        """
        Devuelve todos los horarios establecidos para una fecha específica.
        """
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).filter_by(fecha=fecha).all()
        session.close()
        return horarios

    @staticmethod
    def verificar_superposicion(
        sucursal_id: int,
        fecha: date,
        hora_inicio: time,
        hora_fin: time
    ) -> bool:
        """
        Verifica si existe al menos un Horario en la misma sucursal y fecha
        que se superponga con el rango [hora_inicio, hora_fin].
        Retorna True si hay superposición, False en caso contrario.
        """
        session: Session = Database.get_session("rrhh")
        existe_superposicion = session.query(Horario).filter(
            Horario.sucursal_id == sucursal_id,
            Horario.fecha == fecha,
            Horario.hora_inicio < hora_fin,  # cruce en la parte final
            Horario.hora_fin > hora_inicio   # cruce en la parte inicial
        ).first() is not None
        session.close()
        return existe_superposicion

    @staticmethod
    def get_horarios_por_dia(sucursal_id: int, dia_id: int) -> List[Horario]:
        """
        Devuelve la lista de horarios de una Sucursal en un día de la semana específico
        (referenciado por 'dia_id').
        """
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).filter_by(sucursal_id=sucursal_id, dia_id=dia_id).all()
        session.close()
        return horarios
