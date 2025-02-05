from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.espacio_disponible_sucursal import EspacioDisponibleSucursal
from typing import List, Optional

class EspacioDisponibleSucursalRepository:
    @staticmethod
    def get_by_sucursal(sucursal_id: int) -> List[EspacioDisponibleSucursal]:
        """Obtiene los espacios disponibles en una sucursal."""
        session: Session = Database.get_session("rrhh")
        espacios = session.query(EspacioDisponibleSucursal).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return espacios

    @staticmethod
    def get_by_rol(sucursal_id: int, rol_colaborador_id: int) -> Optional[EspacioDisponibleSucursal]:
        """Obtiene el espacio disponible en una sucursal para un rol específico."""
        session: Session = Database.get_session("rrhh")
        espacio = session.query(EspacioDisponibleSucursal).filter_by(
            sucursal_id=sucursal_id, rol_colaborador_id=rol_colaborador_id
        ).first()
        session.close()
        return espacio

    @staticmethod
    def create(espacio: EspacioDisponibleSucursal) -> EspacioDisponibleSucursal:
        """Crea un nuevo registro de espacio disponible en una sucursal."""
        session: Session = Database.get_session("rrhh")
        session.add(espacio)
        session.commit()
        session.refresh(espacio)
        session.close()
        return espacio

    @staticmethod
    def update(espacio: EspacioDisponibleSucursal) -> EspacioDisponibleSucursal:
        """Actualiza un registro de espacio disponible en una sucursal."""
        session: Session = Database.get_session("rrhh")
        session.merge(espacio)
        session.commit()
        session.refresh(espacio)
        session.close()
        return espacio

    @staticmethod
    def delete(espacio_id: int) -> bool:
        """Elimina un registro de espacio disponible en una sucursal."""
        session: Session = Database.get_session("rrhh")
        espacio = session.query(EspacioDisponibleSucursal).filter_by(id=espacio_id).first()
        if espacio:
            session.delete(espacio)
            session.commit()
            session.close()
            return True
        session.close()
        return False
