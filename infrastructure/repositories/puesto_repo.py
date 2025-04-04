from typing import List, Optional
from datetime import date
from sqlalchemy.orm import Session
from infrastructure.databases.models.puestos import Puesto

class PuestoRepository:
    @staticmethod
    def get_by_id(puesto_id: int, db: Session) -> Optional[Puesto]:
        """
        Obtiene un puesto por su ID.
        """
        return db.query(Puesto).filter_by(id=puesto_id).first()

    @staticmethod
    def get_by_ids(puesto_ids: List[int], db: Session) -> List[Puesto]:
        """
        Obtiene varios puestos a partir de una lista de IDs.
        """
        return db.query(Puesto).filter(Puesto.id.in_(puesto_ids)).all()

    @staticmethod
    def get_all(db: Session) -> List[Puesto]:
        """
        Obtiene todos los puestos.
        """
        return db.query(Puesto).all()

    @staticmethod
    def get_by_sucursal(sucursal_id: int, db: Session) -> List[Puesto]:
        """
        Obtiene todos los puestos de una sucursal.
        """
        return db.query(Puesto).filter_by(sucursal_id=sucursal_id).all()

    @staticmethod
    def get_by_colaborador(colaborador_id: int, db: Session) -> List[Puesto]:
        """
        Obtiene todos los puestos de un colaborador.
        """
        return db.query(Puesto).filter_by(colaborador_id=colaborador_id).all()

    @staticmethod
    def get_by_colaborador_date(colaborador_id: int, fecha_desde: date, fecha_hasta: date, db: Session) -> List[Puesto]:
        """
        Obtiene todos los puestos de un colaborador filtrando por el rango de fechas.
        """
        return db.query(Puesto).filter(
            Puesto.colaborador_id == colaborador_id,
            Puesto.fecha >= fecha_desde,
            Puesto.fecha <= fecha_hasta
        ).all()

    @staticmethod
    def create(puesto: Puesto, db: Session) -> Puesto:
        """
        Crea un nuevo puesto en la base de datos.
        """
        db.add(puesto)
        db.commit()
        db.refresh(puesto)
        return puesto

    @staticmethod
    def create_many(puestos: List[Puesto], db: Session) -> List[Puesto]:
        """
        Crea varios puestos en la base de datos.
        """
        db.add_all(puestos)
        db.commit()
        for puesto in puestos:
            db.refresh(puesto)
        return puestos

    @staticmethod
    def update(puesto: Puesto, db: Session) -> Puesto:
        """
        Actualiza un puesto en la base de datos.
        Se asume que el manejo del commit se hace externamente.
        """
        db_puesto = db.merge(puesto)
        # Si se maneja commit externamente, se puede usar flush() para sincronizar los cambios
        db.flush()
        db.refresh(db_puesto)
        return db_puesto

    @staticmethod
    def update_many(puestos: List[Puesto], db: Session) -> List[Puesto]:
        """
        Actualiza varios puestos en la base de datos.
        Se asume que el manejo del commit se hace externamente.
        """
        updated_puestos = [db.merge(puesto) for puesto in puestos]
        db.flush()
        for puesto in updated_puestos:
            db.refresh(puesto)
        return updated_puestos

    @staticmethod
    def delete(puesto_id: int, db: Session) -> bool:
        """
        Elimina un puesto de la base de datos por su ID.
        Retorna True si se elimina, False si no existe.
        Se asume que el manejo del commit se realiza externamente.
        """
        puesto = db.query(Puesto).filter_by(id=puesto_id).first()
        if puesto:
            db.delete(puesto)
            db.commit()
            return True
        return False

    @staticmethod
    def delete_many(puesto_ids: List[int], db: Session) -> None:
        """
        Elimina múltiples puestos de la base de datos dado una lista de IDs.
        """
        db.query(Puesto).filter(Puesto.id.in_(puesto_ids)).delete(synchronize_session=False)
        db.commit()
