from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.puestos_cubiertos_por_hora import PuestosCubiertosPorHora
from typing import List, Optional
from datetime import time

class PuestosCubiertosPorHoraRepository:
    @staticmethod
    def get_by_sucursal(sucursal_id: int) -> List[PuestosCubiertosPorHora]:
        """Obtiene los puestos cubiertos en una sucursal."""
        session: Session = Database.get_session("rrhh")
        puestos = session.query(PuestosCubiertosPorHora).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return puestos

    @staticmethod
    def get_by_rol(sucursal_id: int, rol_colaborador_id: int) -> List[PuestosCubiertosPorHora]:
        """Obtiene los puestos cubiertos en una sucursal para un rol específico."""
        session: Session = Database.get_session("rrhh")
        puestos = session.query(PuestosCubiertosPorHora).filter_by(
            sucursal_id=sucursal_id, rol_colaborador_id=rol_colaborador_id
        ).all()
        session.close()
        return puestos

    @staticmethod
    def get_by_horario(sucursal_id: int, dia_id: int, hora: time) -> Optional[PuestosCubiertosPorHora]:
        """Obtiene el número de puestos cubiertos en una sucursal en un día y hora específicos."""
        session: Session = Database.get_session("rrhh")
        puesto = session.query(PuestosCubiertosPorHora).filter_by(
            sucursal_id=sucursal_id, dia_id=dia_id, hora=hora
        ).first()
        session.close()
        return puesto

    @staticmethod
    def create(puesto: PuestosCubiertosPorHora) -> PuestosCubiertosPorHora:
        """Crea un nuevo registro de puestos cubiertos en una sucursal."""
        session: Session = Database.get_session("rrhh")
        session.add(puesto)
        session.commit()
        session.refresh(puesto)
        session.close()
        return puesto

    @staticmethod
    def update(puesto: PuestosCubiertosPorHora) -> PuestosCubiertosPorHora:
        """Actualiza un registro de puestos cubiertos en una sucursal."""
        session: Session = Database.get_session("rrhh")
        session.merge(puesto)
        session.commit()
        session.refresh(puesto)
        session.close()
        return puesto

    @staticmethod
    def delete(puesto_id: int) -> bool:
        """Elimina un registro de puestos cubiertos en una sucursal."""
        session: Session = Database.get_session("rrhh")
        puesto = session.query(PuestosCubiertosPorHora).filter_by(id=puesto_id).first()
        if puesto:
            session.delete(puesto)
            session.commit()
            session.close()
            return True
        session.close()
        return False
