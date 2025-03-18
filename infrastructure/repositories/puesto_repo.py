# src/infrastructure/repositories/puesto_repo.py
from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.puestos import Puesto

class PuestoRepository:
    @staticmethod
    def get_by_id(puesto_id: int, db: Optional[Session] = None) -> Optional[Puesto]:
        """
        Obtiene un puesto por su ID.
        Si no se pasa una sesión, se crea una sesión interna que se cierra al finalizar.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            puesto = db.query(Puesto).filter_by(id=puesto_id).first()
            return puesto
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_all(db: Optional[Session] = None) -> List[Puesto]:
        """
        Obtiene todos los puestos.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            puestos = db.query(Puesto).all()
            return puestos
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Optional[Session] = None) -> List[Puesto]:
        """
        Obtiene todos los puestos de una sucursal.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            puestos = db.query(Puesto).filter_by(sucursal_id=sucursal_id).all()
            return puestos
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_colaborador(colaborador_id: int, db: Optional[Session] = None) -> List[Puesto]:
        """
        Obtiene todos los puestos de un colaborador.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            puestos = db.query(Puesto).filter_by(colaborador_id=colaborador_id).all()
            return puestos
        finally:
            if close_session:
                db.close()

    @staticmethod
    def create(puesto: Puesto, db: Optional[Session] = None) -> Puesto:
        """
        Crea un nuevo puesto en la base de datos.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db.add(puesto)
            db.commit()
            db.refresh(puesto)
            return puesto
        finally:
            if close_session:
                db.close()

    @staticmethod
    def create_many(puestos: List[Puesto], db: Optional[Session]) -> List[Puesto]:
        """
        Crea varios puestos en la base de datos.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db.add_all(puestos)
            db.commit()
            # Actualiza cada objeto con los datos generados en la BD (como el id)
            for puesto in puestos:
                db.refresh(puesto)
            return puestos
        finally:
            if close_session:
                db.close()

    @staticmethod
    def update(puesto: Puesto, db: Optional[Session] = None) -> Puesto:
        """
        Actualiza un puesto en la base de datos.
        Si se pasa una sesión externa, se asume que el manejo de la transacción se hace afuera.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db_puesto = db.merge(puesto)
            if close_session:
                db.commit()
            else:
                db.flush()
            db.refresh(db_puesto)
            return db_puesto
        finally:
            if close_session:
                db.close()

    @staticmethod
    def delete(puesto_id: int, db: Optional[Session] = None) -> bool:
        """
        Elimina un puesto de la base de datos por su ID.
        Retorna True si se elimina, False si no existe.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            puesto = db.query(Puesto).filter_by(id=puesto_id).first()
            if puesto:
                db.delete(puesto)
                db.commit()
                return True
            return False
        finally:
            if close_session:
                db.close()

    @staticmethod
    def delete_many(puesto_ids: List[int], db: Optional[Session] = None) -> None:
        """
        Elimina múltiples puestos de la base de datos dado una lista de IDs.
        """
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            # Se filtran los puestos cuyo id esté en la lista y se eliminan
            db.query(Puesto).filter(Puesto.id.in_(puesto_ids)).delete(synchronize_session=False)
            db.commit()
        finally:
            if close_session:
                db.close()