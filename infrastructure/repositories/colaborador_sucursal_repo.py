from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.colaborador_sucursal import ColaboradorSucursal
from typing import List, Optional

class ColaboradorSucursalRepository:
    @staticmethod
    def get_by_colaborador(colaborador_id: int) -> List[ColaboradorSucursal]:
        """Obtiene las relaciones de un colaborador con sus sucursales."""
        session: Session = Database.get_session("rrhh")
        relaciones = session.query(ColaboradorSucursal).filter_by(colaborador_id=colaborador_id).all()
        session.close()
        return relaciones

    @staticmethod
    def get_by_sucursal(sucursal_id: int) -> List[ColaboradorSucursal]:
        """Obtiene las relaciones de una sucursal con sus colaboradores."""
        session: Session = Database.get_session("rrhh")
        relaciones = session.query(ColaboradorSucursal).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return relaciones

    @staticmethod
    def create(relacion: ColaboradorSucursal) -> ColaboradorSucursal:
        """Crea una nueva relación entre colaborador y sucursal."""
        session: Session = Database.get_session("rrhh")
        session.add(relacion)
        session.commit()
        session.refresh(relacion)
        session.close()
        return relacion

    @staticmethod
    def delete(relacion_id: int) -> bool:
        """Elimina una relación entre colaborador y sucursal."""
        session: Session = Database.get_session("rrhh")
        relacion = session.query(ColaboradorSucursal).filter_by(id=relacion_id).first()
        if relacion:
            session.delete(relacion)
            session.commit()
            session.close()
            return True
        session.close()
        return False
