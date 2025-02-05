# archivo: infrastructure/repositories/minimo_puestos_requeridos_repo.py
from typing import List, Optional
from datetime import time
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.minimo_puestos_requeridos import MinimoPuestosRequeridos

class MinimoPuestosRequeridosRepository:
    @staticmethod
    def get_by_sucursal(sucursal_id: int) -> List[MinimoPuestosRequeridos]:
        """
        Obtiene todos los registros de mínimos de puestos requeridos para la sucursal dada.
        """
        session: Session = Database.get_session("rrhh")
        minimos = session.query(MinimoPuestosRequeridos).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return minimos

    @staticmethod
    def get_by_rol(sucursal_id: int, rol_colaborador_id: int) -> List[MinimoPuestosRequeridos]:
        """
        Obtiene los registros de mínimos de puestos para una sucursal y un rol específico.
        """
        session: Session = Database.get_session("rrhh")
        minimos = session.query(MinimoPuestosRequeridos).filter_by(
            sucursal_id=sucursal_id,
            rol_colaborador_id=rol_colaborador_id
        ).all()
        session.close()
        return minimos

    @staticmethod
    def get_by_horario(sucursal_id: int, dia_id: int, hora: time) -> Optional[MinimoPuestosRequeridos]:
        """
        Obtiene el mínimo de puestos requeridos para un día y hora específicos en una sucursal.
        Retorna None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        minimo = session.query(MinimoPuestosRequeridos).filter_by(
            sucursal_id=sucursal_id,
            dia_id=dia_id,
            hora=hora
        ).first()
        session.close()
        return minimo

    @staticmethod
    def create(minimo: MinimoPuestosRequeridos) -> MinimoPuestosRequeridos:
        """
        Crea un nuevo registro de mínimos de puestos requeridos en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(minimo)
        session.commit()
        session.refresh(minimo)
        session.close()
        return minimo

    @staticmethod
    def update(minimo: MinimoPuestosRequeridos) -> Optional[MinimoPuestosRequeridos]:
        """
        Actualiza un registro de mínimos de puestos requeridos.
        Retorna el objeto actualizado o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        existente = session.query(MinimoPuestosRequeridos).filter_by(id=minimo.id).first()
        if not existente:
            session.close()
            return None

        db_minimo = session.merge(minimo)
        session.commit()
        session.refresh(db_minimo)
        session.close()
        return db_minimo

    @staticmethod
    def delete(minimo_id: int) -> bool:
        """
        Elimina un registro de mínimos de puestos requeridos por su ID.
        Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        minimo = session.query(MinimoPuestosRequeridos).filter_by(id=minimo_id).first()
        if minimo:
            session.delete(minimo)
            session.commit()
            session.close()
            return True
        session.close()
        return False
