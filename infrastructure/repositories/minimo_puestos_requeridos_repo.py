from typing import List, Optional
from datetime import time
from sqlalchemy.orm import Session
from infrastructure.databases.models.minimo_puestos_requeridos import MinimoPuestosRequeridos

class MinimoPuestosRequeridosRepository:
    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Session) -> List[MinimoPuestosRequeridos]:
        """
        Obtiene todos los registros de mínimos de puestos requeridos para la sucursal dada.
        """
        return db.query(MinimoPuestosRequeridos).filter_by(sucursal_id=sucursal_id).all()

    @staticmethod
    def get_by_rol(sucursal_id: int, rol_colaborador_id: int, db: Session) -> List[MinimoPuestosRequeridos]:
        """
        Obtiene los registros de mínimos de puestos para una sucursal y un rol específico.
        """
        return db.query(MinimoPuestosRequeridos).filter_by(
            sucursal_id=sucursal_id,
            rol_colaborador_id=rol_colaborador_id
        ).all()

    @staticmethod
    def get_by_horario(sucursal_id: int, dia_id: int, hora: time, db: Session) -> Optional[MinimoPuestosRequeridos]:
        """
        Obtiene el mínimo de puestos requeridos para un día y hora específicos en una sucursal.
        Retorna None si no existe.
        """
        return db.query(MinimoPuestosRequeridos).filter_by(
            sucursal_id=sucursal_id,
            dia_id=dia_id,
            hora=hora
        ).first()

    @staticmethod
    def create(minimo: MinimoPuestosRequeridos, db: Session) -> MinimoPuestosRequeridos:
        """
        Crea un nuevo registro de mínimos de puestos requeridos en la base de datos.
        Se asume que el manejo del commit se realizará externamente.
        """
        db.add(minimo)
        db.flush()  # Sin commit para sincronizar los cambios (commit se debe realizar externamente)
        db.refresh(minimo)
        return minimo

    @staticmethod
    def update(minimo: MinimoPuestosRequeridos, db: Session) -> Optional[MinimoPuestosRequeridos]:
        """
        Actualiza un registro de mínimos de puestos requeridos.
        Retorna el objeto actualizado o None si no existe.
        Se asume que el manejo del commit se realizará externamente.
        """
        existente = db.query(MinimoPuestosRequeridos).filter_by(id=minimo.id).first()
        if not existente:
            return None

        db_minimo = db.merge(minimo)
        db.flush()
        db.refresh(db_minimo)
        return db_minimo

    @staticmethod
    def delete(minimo_id: int, db: Session) -> bool:
        """
        Elimina un registro de mínimos de puestos requeridos por su ID.
        Retorna True si se elimina, False si no existe.
        Se asume que el manejo del commit se realizará externamente.
        """
        minimo = db.query(MinimoPuestosRequeridos).filter_by(id=minimo_id).first()
        if minimo:
            db.delete(minimo)
            db.flush()
            return True
        return False
