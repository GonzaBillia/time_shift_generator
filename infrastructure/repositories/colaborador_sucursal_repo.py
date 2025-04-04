from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig
from infrastructure.databases.models.colaborador_sucursal import ColaboradorSucursal

class ColaboradorSucursalRepository:
    @staticmethod
    def get_by_id(relacion_id: int, db: Session) -> Optional[ColaboradorSucursal]:
        """
        Devuelve una relación específica por su ID en la tabla 'colaboradores_sucursales'.
        Retorna None si no existe.
        """
        return db.query(ColaboradorSucursal).filter_by(id=relacion_id).first()

    @staticmethod
    def get_by_colaborador(colaborador_id: int, db: Session) -> List[ColaboradorSucursal]:
        """
        Devuelve la lista de asociaciones 'ColaboradorSucursal' para un colaborador específico.
        """
        return db.query(ColaboradorSucursal).filter_by(colaborador_id=colaborador_id).all()

    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Session) -> List[ColaboradorSucursal]:
        """
        Devuelve la lista de asociaciones 'ColaboradorSucursal' para una sucursal específica.
        """
        return db.query(ColaboradorSucursal).filter_by(sucursal_id=sucursal_id).all()

    @staticmethod
    def create(relacion: ColaboradorSucursal, db: Session) -> ColaboradorSucursal:
        """
        Crea una nueva relación en la tabla 'colaboradores_sucursales'.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db.add(relacion)
        db.flush()  # Sincroniza los cambios para asignar un ID, si es necesario
        db.refresh(relacion)
        return relacion

    @staticmethod
    def update(relacion: ColaboradorSucursal, db: Session) -> ColaboradorSucursal:
        """
        Actualiza una relación existente en la tabla 'colaboradores_sucursales'.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db_relacion = db.merge(relacion)
        db.flush()
        db.refresh(db_relacion)
        return db_relacion

    @staticmethod
    def delete(relacion_id: int, db: Session) -> bool:
        """
        Elimina la relación (fila) de la tabla 'colaboradores_sucursales'
        identificada por 'relacion_id'. Retorna True si se elimina correctamente, False en caso contrario.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        relacion = db.query(ColaboradorSucursal).filter_by(id=relacion_id).first()
        if relacion:
            db.delete(relacion)
            db.flush()
            return True
        return False
