from typing import List, Optional
from sqlalchemy.orm import Session
from infrastructure.databases.config.database import DBConfig
from infrastructure.databases.models.empresa import Empresa

class EmpresaRepository:
    @staticmethod
    def create(empresa: Empresa, db: Optional[Session] = None) -> Empresa:
        """
        Crea una nueva Empresa en la base de datos.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            db.add(empresa)
            db.commit()
            db.refresh(empresa)
            return empresa
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_id(empresa_id: int, db: Optional[Session] = None) -> Optional[Empresa]:
        """
        Obtiene una Empresa por su ID.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            empresa = db.query(Empresa).filter_by(id=empresa_id).first()
            return empresa
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_cuit(cuit: str, db: Optional[Session] = None) -> Optional[Empresa]:
        """
        Obtiene una Empresa por su CUIT.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            empresa = db.query(Empresa).filter_by(cuit=cuit).first()
            return empresa
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_razon_social(razon_social: str, db: Optional[Session] = None) -> Optional[Empresa]:
        """
        Obtiene una Empresa por su razón social.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            empresa = db.query(Empresa).filter_by(razon_social=razon_social).first()
            return empresa
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_all(db: Optional[Session] = None) -> List[Empresa]:
        """
        Devuelve todas las Empresas.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            empresas = db.query(Empresa).all()
            return empresas
        finally:
            if close_session:
                db.close()

    @staticmethod
    def update(empresa: Empresa, db: Optional[Session] = None) -> Empresa:
        """
        Actualiza una Empresa existente en la base de datos.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            db_empresa = db.merge(empresa)
            db.commit()
            db.refresh(db_empresa)
            return db_empresa
        finally:
            if close_session:
                db.close()

    @staticmethod
    def delete(empresa_id: int, db: Optional[Session] = None) -> bool:
        """
        Elimina una Empresa por su ID.
        Retorna True si se elimina correctamente.
        """
        close_session = False
        if db is None:
            db = DBConfig.get_session("rrhh")
            close_session = True
        try:
            empresa = db.query(Empresa).filter_by(id=empresa_id).first()
            if empresa:
                db.delete(empresa)
                db.commit()
                return True
            return False
        finally:
            if close_session:
                db.close()
