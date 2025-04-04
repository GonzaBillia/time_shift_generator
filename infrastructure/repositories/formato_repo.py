from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from infrastructure.databases.models.formato import Formato
from infrastructure.databases.models.rol import Rol
from infrastructure.databases.models.formato_rol import FormatosRoles

class FormatoRepository:
    @staticmethod
    def get_by_id(formato_id: int, db: Session) -> Optional[Formato]:
        """
        Retorna un Formato por su ID, o None si no existe.
        'formato.roles' es una lista de objetos FormatosRoles.
        Se utiliza joinedload para cargar la relación 'roles' de forma anticipada.
        """
        return db.query(Formato)\
            .options(joinedload(Formato.roles).joinedload(FormatosRoles.rol))\
            .filter_by(id=formato_id).first()

    @staticmethod
    def get_all(db: Session) -> List[Formato]:
        """
        Retorna la lista de todos los Formato en la base.
        Se utiliza joinedload para cargar la relación 'roles' de forma anticipada.
        """
        return db.query(Formato)\
            .options(joinedload(Formato.roles).joinedload(FormatosRoles.rol))\
            .all()

    @staticmethod
    def create(formato: Formato, db: Session) -> Formato:
        """
        Crea un Formato y (opcionalmente) sus asociaciones FormatosRoles
        si 'formato.roles' tiene elementos.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        db.add(formato)
        db.flush()  # Sincroniza los cambios para asignar un ID si es necesario
        db.refresh(formato)
        return formato

    @staticmethod
    def update(formato: Formato, db: Session) -> Optional[Formato]:
        """
        Actualiza un Formato existente en la BD (nombre y asociaciones).

        1) Busca el Formato real: 'formato_existente'.
        2) Actualiza el 'nombre'.
        3) Limpia 'formato_existente.roles' (FormatosRoles).
        4) Por cada obj en 'formato.roles', reasigna 'assoc.formato = formato_existente' y
           ajusta 'assoc.rol' o 'assoc.rol_id'.
        5) Sincroniza los cambios y retorna el Formato actualizado. Si no existe, retorna None.
        """
        formato_existente = db.query(Formato)\
            .options(joinedload(Formato.roles).joinedload(FormatosRoles.rol))\
            .filter_by(id=formato.id).first()
        if not formato_existente:
            return None

        # Actualiza campos simples
        formato_existente.nombre = formato.nombre

        # Limpiar la lista actual de asociaciones
        formato_existente.roles.clear()

        # Reasignar las nuevas asociaciones
        for assoc in formato.roles:
            assoc.formato = formato_existente
            if assoc.rol is not None:
                db_rol = db.merge(assoc.rol)
                assoc.rol = db_rol
            db.add(assoc)

        db.flush()
        db.refresh(formato_existente)
        return formato_existente

    @staticmethod
    def delete(formato_id: int, db: Session) -> bool:
        """
        Elimina el Formato por su ID. Por cascada (cascade="all, delete-orphan"),
        se eliminarán los FormatosRoles asociados.
        Se asume que se pasa una sesión activa y que el commit se realizará externamente.
        """
        formato = db.query(Formato).filter_by(id=formato_id).first()
        if formato:
            db.delete(formato)
            db.flush()
            return True
        return False

    @staticmethod
    def get_by_nombre(nombre: str, db: Session) -> Optional[Formato]:
        """
        Obtiene un Formato por su nombre, o None si no existe.
        """
        return db.query(Formato)\
            .options(joinedload(Formato.roles).joinedload(FormatosRoles.rol))\
            .filter_by(nombre=nombre).first()

    @staticmethod
    def get_roles_by_formato(formato_id: int, db: Session) -> List[Rol]:
        """
        Obtiene la lista de Rol que están asociados a un Formato dado,
        extrayendo 'assoc.rol' de cada FormatosRoles en formato.roles.
        """
        formato = db.query(Formato)\
            .options(joinedload(Formato.roles).joinedload(FormatosRoles.rol))\
            .filter_by(id=formato_id).first()

        if not formato:
            return []

        lista_roles = [assoc.rol for assoc in formato.roles if assoc.rol is not None]
        return lista_roles
