from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario import Horario
from typing import List, Optional
from datetime import date, time

class HorarioRepository:
    @staticmethod
    def get_by_id(horario_id: int) -> Optional[Horario]:
        """Obtiene un horario por su ID."""
        session: Session = Database.get_session("rrhh")
        horario = session.query(Horario).filter_by(id=horario_id).first()
        session.close()
        return horario

    @staticmethod
    def get_all() -> List[Horario]:
        """Obtiene todos los horarios registrados en la base de datos."""
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).all()
        session.close()
        return horarios

    @staticmethod
    def create(horario: Horario) -> Horario:
        """Crea un nuevo horario en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.add(horario)
        session.commit()
        session.refresh(horario)
        session.close()
        return horario

    @staticmethod
    def update(horario: Horario) -> Horario:
        """Actualiza un horario existente en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.merge(horario)
        session.commit()
        session.refresh(horario)
        session.close()
        return horario

    @staticmethod
    def delete(horario_id: int) -> bool:
        """Elimina un horario de la base de datos."""
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
        """Obtiene todos los horarios de una sucursal específica."""
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return horarios

    @staticmethod
    def get_by_colaborador(colaborador_id: int) -> List[Horario]:
        """Obtiene todos los horarios asignados a un colaborador."""
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).filter_by(colaborador_id=colaborador_id).all()
        session.close()
        return horarios

    @staticmethod
    def get_by_fecha(fecha: date) -> List[Horario]:
        """Obtiene todos los horarios asignados en una fecha específica."""
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).filter_by(fecha=fecha).all()
        session.close()
        return horarios

    @staticmethod
    def verificar_superposicion(sucursal_id: int, fecha: date, hora_inicio: time, hora_fin: time) -> bool:
        """
        Verifica si un horario se superpone con otros en la misma sucursal y fecha.
        """
        session: Session = Database.get_session("rrhh")
        existe_superposicion = session.query(Horario).filter(
            Horario.sucursal_id == sucursal_id,
            Horario.fecha == fecha,
            Horario.hora_inicio < hora_fin,  # Se superpone si hay cruce de horarios
            Horario.hora_fin > hora_inicio
        ).first() is not None

        session.close()
        return existe_superposicion

    @staticmethod
    def get_horarios_por_dia(sucursal_id: int, dia_id: int) -> List[Horario]:
        """Obtiene los horarios de una sucursal en un día de la semana específico."""
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).filter_by(sucursal_id=sucursal_id, dia_id=dia_id).all()
        session.close()
        return horarios
