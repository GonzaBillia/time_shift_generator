# colaborador_sucursal_repo.py

from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.colaborador_sucursal import ColaboradorSucursal

class ColaboradorSucursalRepository:
    @staticmethod
    def get_by_id(relacion_id: int) -> Optional[ColaboradorSucursal]:
        """
        Devuelve una relación específica por su ID en la tabla 'colaboradores_sucursales'.
        """
        session: Session = Database.get_session("rrhh")
        relacion = session.query(ColaboradorSucursal).filter_by(id=relacion_id).first()
        session.close()
        return relacion

    @staticmethod
    def get_by_colaborador(colaborador_id: int) -> List[ColaboradorSucursal]:
        """
        Devuelve la lista de asociaciones 'ColaboradorSucursal'
        para un colaborador específico.
        """
        session: Session = Database.get_session("rrhh")
        relaciones = session.query(ColaboradorSucursal).filter_by(colaborador_id=colaborador_id).all()
        session.close()
        return relaciones

    @staticmethod
    def get_by_sucursal(sucursal_id: int) -> List[ColaboradorSucursal]:
        """
        Devuelve la lista de asociaciones 'ColaboradorSucursal'
        para una sucursal específica.
        """
        session: Session = Database.get_session("rrhh")
        relaciones = session.query(ColaboradorSucursal).filter_by(sucursal_id=sucursal_id).all()
        session.close()
        return relaciones

    @staticmethod
    def create(relacion: ColaboradorSucursal) -> ColaboradorSucursal:
        """
        Crea una nueva relación en la tabla 'colaboradores_sucursales'.
        """
        session: Session = Database.get_session("rrhh")
        session.add(relacion)
        session.commit()
        session.refresh(relacion)
        session.close()
        return relacion

    @staticmethod
    def update(relacion: ColaboradorSucursal) -> ColaboradorSucursal:
        """
        Actualiza una relación existente en la tabla 'colaboradores_sucursales'.
        Si 'relacion' no existe en la sesión, se hace un merge.
        """
        session: Session = Database.get_session("rrhh")
        db_relacion = session.merge(relacion)  # Retorna la instancia persistida
        session.commit()
        session.refresh(db_relacion)
        session.close()
        return db_relacion

    @staticmethod
    def delete(relacion_id: int) -> bool:
        """
        Elimina la relación (fila) de la tabla 'colaboradores_sucursales'
        identificada por 'relacion_id'. Retorna True si se elimina.
        """
        session: Session = Database.get_session("rrhh")
        relacion = session.query(ColaboradorSucursal).filter_by(id=relacion_id).first()
        if relacion:
            session.delete(relacion)
            session.commit()
            session.close()
            return True
        session.close()
        return False
