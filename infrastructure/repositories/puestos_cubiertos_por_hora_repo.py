from typing import List, Optional
from datetime import time
from sqlalchemy.orm import Session
from infrastructure.databases.models.puestos_cubiertos_por_hora import PuestosCubiertosPorHora

class PuestosCubiertosPorHoraRepository:
    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Session) -> List[PuestosCubiertosPorHora]:
        """
        Devuelve la lista de registros de puestos cubiertos para la sucursal dada.
        """
        return db.query(PuestosCubiertosPorHora).filter_by(sucursal_id=sucursal_id).all()

    @staticmethod
    def get_by_rol(sucursal_id: int, rol_colaborador_id: int, db: Session) -> List[PuestosCubiertosPorHora]:
        """
        Obtiene la lista de registros de puestos cubiertos en una sucursal para un rol específico.
        """
        return db.query(PuestosCubiertosPorHora).filter_by(
            sucursal_id=sucursal_id,
            rol_colaborador_id=rol_colaborador_id
        ).all()

    @staticmethod
    def get_by_horario(sucursal_id: int, dia_id: int, hora: time, db: Session) -> Optional[PuestosCubiertosPorHora]:
        """
        Retorna el registro de puestos cubiertos en una sucursal para cierto día y hora.
        """
        return db.query(PuestosCubiertosPorHora).filter_by(
            sucursal_id=sucursal_id,
            dia_id=dia_id,
            hora=hora
        ).first()

    @staticmethod
    def create(puesto: PuestosCubiertosPorHora, db: Session) -> PuestosCubiertosPorHora:
        """
        Crea un nuevo registro de puestos cubiertos en la base de datos.
        Se asume que el manejo del commit se realizará externamente.
        """
        db.add(puesto)
        db.flush()
        db.refresh(puesto)
        return puesto

    @staticmethod
    def update(puesto: PuestosCubiertosPorHora, db: Session) -> Optional[PuestosCubiertosPorHora]:
        """
        Actualiza un registro de puestos cubiertos.
        Retorna el objeto actualizado o None si no existe.
        Se asume que el manejo del commit se realizará externamente.
        """
        existente = db.query(PuestosCubiertosPorHora).filter_by(id=puesto.id).first()
        if not existente:
            return None

        db_puesto = db.merge(puesto)
        db.flush()
        db.refresh(db_puesto)
        return db_puesto

    @staticmethod
    def delete(puesto_id: int, db: Session) -> bool:
        """
        Elimina un registro de puestos cubiertos por su ID.
        Retorna True si se elimina, False si no existe.
        Se asume que el manejo del commit se realizará externamente.
        """
        puesto = db.query(PuestosCubiertosPorHora).filter_by(id=puesto_id).first()
        if puesto:
            db.delete(puesto)
            db.flush()
            return True
        return False
