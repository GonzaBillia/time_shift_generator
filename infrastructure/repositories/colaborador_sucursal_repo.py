from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig
from infrastructure.databases.models.colaborador_sucursal import ColaboradorSucursal

class ColaboradorSucursalRepository:
    @staticmethod
    def get_by_id(relacion_id: int, db: Optional[Session] = None) -> Optional[ColaboradorSucursal]:
        """
        Devuelve una relación específica por su ID en la tabla 'colaboradores_sucursales'.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            relacion = db.query(ColaboradorSucursal).filter_by(id=relacion_id).first()
            return relacion
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_colaborador(colaborador_id: int, db: Optional[Session] = None) -> List[ColaboradorSucursal]:
        """
        Devuelve la lista de asociaciones 'ColaboradorSucursal' para un colaborador específico.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            relaciones = db.query(ColaboradorSucursal).filter_by(colaborador_id=colaborador_id).all()
            return relaciones
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Optional[Session] = None) -> List[ColaboradorSucursal]:
        """
        Devuelve la lista de asociaciones 'ColaboradorSucursal' para una sucursal específica.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            relaciones = db.query(ColaboradorSucursal).filter_by(sucursal_id=sucursal_id).all()
            return relaciones
        finally:
            if close_session:
                db.close()

    @staticmethod
    def create(relacion: ColaboradorSucursal, db: Optional[Session] = None) -> ColaboradorSucursal:
        """
        Crea una nueva relación en la tabla 'colaboradores_sucursales'.
        Si no se proporciona una sesión, se crea y se cierra internamente.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            db.add(relacion)
            if close_session:
                db.commit()
            else:
                db.flush()
            db.refresh(relacion)
            return relacion
        finally:
            if close_session:
                db.close()

    @staticmethod
    def update(relacion: ColaboradorSucursal, db: Optional[Session] = None) -> ColaboradorSucursal:
        """
        Actualiza una relación existente en la tabla 'colaboradores_sucursales'.
        Si 'relacion' no existe en la sesión, se hace un merge.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            db_relacion = db.merge(relacion)
            if close_session:
                db.commit()
            else:
                db.flush()
            db.refresh(db_relacion)
            return db_relacion
        finally:
            if close_session:
                db.close()

    @staticmethod
    def delete(relacion_id: int, db: Optional[Session] = None) -> bool:
        """
        Elimina la relación (fila) de la tabla 'colaboradores_sucursales'
        identificada por 'relacion_id'. Retorna True si se elimina correctamente.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            relacion = db.query(ColaboradorSucursal).filter_by(id=relacion_id).first()
            if relacion:
                db.delete(relacion)
                if close_session:
                    db.commit()
                else:
                    db.flush()
                return True
            return False
        finally:
            if close_session:
                db.close()
