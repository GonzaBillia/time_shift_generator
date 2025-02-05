from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.minimo_puestos_requeridos import MinimoPuestosRequeridos
from typing import List, Optional
from datetime import time

class MinimoPuestosRequeridosRepository:
    @staticmethod
    def get_by_sucursal(sucursal_id: int) -> List[MinimoPuestosRequeridos]:
        """Obtiene los mínimos de puestos requeridos en una sucursal."""
        session: Session = Database.get_session("rrhh")
        minimos = session.query(MinimoPuestosRequeridos).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return minimos

    @staticmethod
    def get_by_rol(sucursal_id: int, rol_colaborador_id: int) -> List[MinimoPuestosRequeridos]:
        """Obtiene los mínimos de puestos requeridos en una sucursal para un rol específico."""
        session: Session = Database.get_session("rrhh")
        minimos = session.query(MinimoPuestosRequeridos).filter_by(
            sucursal_id=sucursal_id, rol_colaborador_id=rol_colaborador_id
        ).all()
        session.close()
        return minimos

    @staticmethod
    def get_by_horario(sucursal_id: int, dia_id: int, hora: time) -> Optional[MinimoPuestosRequeridos]:
        """Obtiene el mínimo de puestos requeridos en una sucursal en un día y hora específicos."""
        session: Session = Database.get_session("rrhh")
        minimo = session.query(MinimoPuestosRequeridos).filter_by(
            sucursal_id=sucursal_id, dia_id=dia_id, hora=hora
        ).first()
        session.close()
        return minimo

    @staticmethod
    def create(minimo: MinimoPuestosRequeridos) -> MinimoPuestosRequeridos:
        """Crea un nuevo mínimo de puestos requeridos en una sucursal."""
        session: Session = Database.get_session("rrhh")
        session.add(minimo)
        session.commit()
        session.refresh(minimo)
        session.close()
        return minimo

    @staticmethod
    def update(minimo: MinimoPuestosRequeridos) -> MinimoPuestosRequeridos:
        """Actualiza un mínimo de puestos requeridos en una sucursal."""
        session: Session = Database.get_session("rrhh")
        session.merge(minimo)
        session.commit()
        session.refresh(minimo)
        session.close()
        return minimo

    @staticmethod
    def delete(minimo_id: int) -> bool:
        """Elimina un mínimo de puestos requeridos en una sucursal."""
        session: Session = Database.get_session("rrhh")
        minimo = session.query(MinimoPuestosRequeridos).filter_by(id=minimo_id).first()
        if minimo:
            session.delete(minimo)
            session.commit()
            session.close()
            return True
        session.close()
        return False
