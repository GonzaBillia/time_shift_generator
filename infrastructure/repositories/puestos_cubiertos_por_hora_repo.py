# archivo: infrastructure/repositories/puestos_cubiertos_por_hora_repo.py
from typing import List, Optional
from datetime import time
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.puestos_cubiertos_por_hora import PuestosCubiertosPorHora

class PuestosCubiertosPorHoraRepository:
    @staticmethod
    def get_by_sucursal(sucursal_id: int) -> List[PuestosCubiertosPorHora]:
        """
        Devuelve la lista de registros de puestos cubiertos para la sucursal dada.
        """
        session: Session = Database.get_session("rrhh")
        puestos = session.query(PuestosCubiertosPorHora).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return puestos

    @staticmethod
    def get_by_rol(sucursal_id: int, rol_colaborador_id: int) -> List[PuestosCubiertosPorHora]:
        """
        Obtiene la lista de registros de puestos cubiertos en una sucursal para un rol específico.
        """
        session: Session = Database.get_session("rrhh")
        puestos = session.query(PuestosCubiertosPorHora).filter_by(
            sucursal_id=sucursal_id,
            rol_colaborador_id=rol_colaborador_id
        ).all()
        session.close()
        return puestos

    @staticmethod
    def get_by_horario(sucursal_id: int, dia_id: int, hora: time) -> Optional[PuestosCubiertosPorHora]:
        """
        Retorna el registro de puestos cubiertos en una sucursal para cierto día y hora.
        """
        session: Session = Database.get_session("rrhh")
        puesto = session.query(PuestosCubiertosPorHora).filter_by(
            sucursal_id=sucursal_id,
            dia_id=dia_id,
            hora=hora
        ).first()
        session.close()
        return puesto

    @staticmethod
    def create(puesto: PuestosCubiertosPorHora) -> PuestosCubiertosPorHora:
        """
        Crea un nuevo registro de puestos cubiertos en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(puesto)
        session.commit()
        session.refresh(puesto)
        session.close()
        return puesto

    @staticmethod
    def update(puesto: PuestosCubiertosPorHora) -> Optional[PuestosCubiertosPorHora]:
        """
        Actualiza un registro de puestos cubiertos.
        Retorna el objeto actualizado o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        existente = session.query(PuestosCubiertosPorHora).filter_by(id=puesto.id).first()
        if not existente:
            session.close()
            return None

        db_puesto = session.merge(puesto)
        session.commit()
        session.refresh(db_puesto)
        session.close()
        return db_puesto

    @staticmethod
    def delete(puesto_id: int) -> bool:
        """
        Elimina un registro de puestos cubiertos por su ID.
        Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        puesto = session.query(PuestosCubiertosPorHora).filter_by(id=puesto_id).first()
        if puesto:
            session.delete(puesto)
            session.commit()
            session.close()
            return True
        session.close()
        return False
