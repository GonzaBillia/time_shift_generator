from typing import List, Optional
from sqlalchemy.orm import Session, joinedload

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.formato import Formato
from infrastructure.databases.models.rol import Rol
from infrastructure.databases.models.formato_rol import FormatosRoles

class FormatoRepository:
    @staticmethod
    def get_by_id(formato_id: int) -> Optional[Formato]:
        """
        Retorna un Formato por su ID, o None si no existe.
        'formato.roles' es una lista de objetos FormatosRoles.
        Se utiliza joinedload para cargar la relación 'roles' de forma anticipada.
        """
        session: Session = Database.get_session("rrhh")
        formato = session.query(Formato)\
            .options(joinedload(Formato.roles).joinedload(FormatosRoles.rol))\
            .filter_by(id=formato_id).first()
        session.close()
        return formato

    @staticmethod
    def get_all() -> List[Formato]:
        """
        Retorna la lista de todos los Formato en la base.
        Se utiliza joinedload para cargar la relación 'roles' de forma anticipada.
        """
        session: Session = Database.get_session("rrhh")
        formatos = session.query(Formato)\
            .options(joinedload(Formato.roles).joinedload(FormatosRoles.rol))\
            .all()
        session.close()
        return formatos

    @staticmethod
    def create(formato: Formato) -> Formato:
        """
        Crea un Formato y (opcionalmente) sus asociaciones FormatosRoles
        si 'formato.roles' tiene elementos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(formato)
        session.commit()
        session.refresh(formato)
        session.close()
        return formato

    @staticmethod
    def update(formato: Formato) -> Optional[Formato]:
        """
        Actualiza un Formato existente en la BD (nombre y asociaciones).
        
        1) Busca el Formato real: 'formato_existente'.
        2) Actualiza el 'nombre'.
        3) Limpia 'formato_existente.roles' (FormatosRoles).
        4) Por cada obj en 'formato.roles', reasigna 'assoc.formato = formato_existente' y
           ajusta 'assoc.rol' o 'assoc.rol_id'.
        5) Hace commit. Devuelve el Formato actualizado. Si no existe, retorna None.
        """
        session: Session = Database.get_session("rrhh")
        formato_existente = session.query(Formato)\
            .options(joinedload(Formato.roles).joinedload(FormatosRoles.rol))\
            .filter_by(id=formato.id).first()
        if not formato_existente:
            session.close()
            return None

        # Actualiza campos simples
        formato_existente.nombre = formato.nombre

        # Limpiar la lista actual de asociaciones
        formato_existente.roles.clear()

        # Reasignar las nuevas asociaciones
        for assoc in formato.roles:
            assoc.formato = formato_existente
            if assoc.rol is not None:
                db_rol = session.merge(assoc.rol)
                assoc.rol = db_rol
            session.add(assoc)

        session.commit()
        session.refresh(formato_existente)
        session.close()
        return formato_existente

    @staticmethod
    def delete(formato_id: int) -> bool:
        """
        Elimina el Formato por su ID. Por cascada (cascade="all, delete-orphan"),
        se eliminarán los FormatosRoles asociados.
        """
        session: Session = Database.get_session("rrhh")
        formato = session.query(Formato).filter_by(id=formato_id).first()
        if formato:
            session.delete(formato)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @staticmethod
    def get_by_nombre(nombre: str) -> Optional[Formato]:
        """
        Obtiene un Formato por su nombre, o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        formato = session.query(Formato)\
            .options(joinedload(Formato.roles).joinedload(FormatosRoles.rol))\
            .filter_by(nombre=nombre).first()
        session.close()
        return formato

    @staticmethod
    def get_roles_by_formato(formato_id: int) -> List[Rol]:
        """
        Obtiene la lista de Rol que están asociados a un Formato dado,
        extrayendo 'assoc.rol' de cada FormatosRoles en formato.roles.
        """
        session: Session = Database.get_session("rrhh")
        formato = session.query(Formato)\
            .options(joinedload(Formato.roles).joinedload(FormatosRoles.rol))\
            .filter_by(id=formato_id).first()

        if not formato:
            session.close()
            return []

        lista_roles = [assoc.rol for assoc in formato.roles if assoc.rol is not None]
        session.close()
        return lista_roles
