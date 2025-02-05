from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.colaborador import Colaborador
from infrastructure.databases.models.horario import Horario
from infrastructure.databases.models.rol import Rol
from infrastructure.databases.models.tipo_colaborador import TipoEmpleado
from datetime import date
from typing import List, Optional

class ColaboradorRepository:
    @staticmethod
    def get_by_id(colaborador_id: int) -> Optional[Colaborador]:
        """Obtiene un colaborador por su ID."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(id=colaborador_id).first()
        session.close()
        return colaborador
    
    @staticmethod
    def get_by_legajo(legajo: int) -> Optional[Colaborador]:
        """Obtiene un colaborador por su número de legajo."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(legajo=legajo).first()
        session.close()
        return colaborador

    @staticmethod
    def get_all() -> List[Colaborador]:
        """Obtiene todos los colaboradores."""
        session: Session = Database.get_session("rrhh")
        colaboradores = session.query(Colaborador).all()
        session.close()
        return colaboradores

    @staticmethod
    def create(colaborador: Colaborador) -> Colaborador:
        """Crea un nuevo colaborador en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.add(colaborador)
        session.commit()
        session.refresh(colaborador)
        session.close()
        return colaborador

    @staticmethod
    def update(colaborador: Colaborador) -> Colaborador:
        """Actualiza un colaborador en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.merge(colaborador)
        session.commit()
        session.refresh(colaborador)
        session.close()
        return colaborador

    @staticmethod
    def delete(colaborador_id: int) -> bool:
        """Elimina un colaborador de la base de datos."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            session.delete(colaborador)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @staticmethod
    def get_by_email(email: str) -> Optional[Colaborador]:
        """Obtiene un colaborador por su email."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(email=email).first()
        session.close()
        return colaborador

    @staticmethod
    def get_by_dni(dni: str) -> Optional[Colaborador]:
        """Obtiene un colaborador por su DNI."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(dni=dni).first()
        session.close()
        return colaborador

    @staticmethod
    def asignar_horario(colaborador_id: int, horario: Horario):
        """Asigna un horario a un colaborador."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            colaborador.horarios.append(horario)
            session.commit()
        session.close()

    @staticmethod
    def agregar_vacacion(colaborador_id: int, fecha: date):
        """Agrega una fecha de vacaciones al colaborador."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            if fecha not in colaborador.vacaciones:
                colaborador.vacaciones.append(fecha)
                session.commit()
        session.close()

    @staticmethod
    def agregar_horas_extra(colaborador_id: int, tipo: str, cantidad: int):
        """Agrega horas extra a un colaborador."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            if tipo not in {'devolver', 'cobrar'}:
                session.close()
                raise ValueError("El tipo debe ser 'devolver' o 'cobrar'.")
            colaborador.hs_extra[tipo] = colaborador.hs_extra.get(tipo, 0) + cantidad
            session.commit()
        session.close()
