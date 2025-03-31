from typing import List, Optional, Dict, Any
from datetime import date, datetime
from sqlalchemy.orm import Session, joinedload

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario import Horario
from infrastructure.databases.models.sucursal import Sucursal
from infrastructure.databases.models.colaborador import Colaborador
from infrastructure.databases.models.colaborador_sucursal import ColaboradorSucursal
from infrastructure.databases.models.puestos import Puesto


class HorarioRepository:
    @staticmethod
    def get_by_id(horario_id: int) -> Optional[Horario]:
        """
        Obtiene un Horario por su ID.
        Retorna None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        horario = session.query(Horario).filter_by(id=horario_id).first()
        session.close()
        return horario

    @staticmethod
    def get_by_puesto(puesto_id: int, db: Optional[Session] = None) -> List[Horario]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horarios = db.query(Horario).filter_by(puesto_id=puesto_id).all()
            return horarios
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_puestos(puestos_ids: List[int], db: Optional[Session] = None) -> List[Horario]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horarios = db.query(Horario).filter(Horario.puesto_id.in_(puestos_ids)).all()
            return horarios
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_by_colaborador(colaborador_id: int, db: Optional[Session] = None) -> List[Horario]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            horarios = db.query(Horario).filter_by(colaborador_id=colaborador_id).all()
            return horarios
        finally:
            if close_session:
                db.close()

    @staticmethod
    def get_all() -> List[Horario]:
        """
        Devuelve todos los horarios registrados en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        horarios = session.query(Horario).all()
        session.close()
        return horarios

    @staticmethod
    def create(horario: Horario) -> Horario:
        """
        Crea un nuevo Horario y lo persiste en la base de datos.
        """
        session: Session = Database.get_session("rrhh")
        session.add(horario)
        session.commit()
        session.refresh(horario)
        session.close()
        return horario

    @staticmethod
    def update(horario: Horario) -> Optional[Horario]:
        """
        Actualiza un Horario existente.
        Recibe un objeto Horario con id,
        hace 'merge' en la sesión y lo refresca luego del commit.
        Retorna el Horario actualizado o None si no existe.
        """
        session: Session = Database.get_session("rrhh")
        existente = session.query(Horario).filter_by(id=horario.id).first()
        if not existente:
            session.close()
            return None

        db_horario = session.merge(horario)
        session.commit()
        session.refresh(db_horario)
        session.close()
        return db_horario

    @staticmethod
    def delete(horario_id: int) -> bool:
        """
        Elimina un Horario de la base de datos por su ID.
        Retorna True si se elimina, False si no existe.
        """
        session: Session = Database.get_session("rrhh")
        horario = session.query(Horario).filter_by(id=horario_id).first()
        if horario:
            session.delete(horario)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @staticmethod
    def delete_many(horario_ids: List[int]) -> bool:
        """
        Elimina múltiples Horarios de la base de datos por sus IDs.
        Retorna True si se eliminó al menos uno, o False si ninguno fue encontrado.
        """
        session: Session = Database.get_session("rrhh")
        try:
            query = session.query(Horario).filter(Horario.id.in_(horario_ids))
            if query.count() == 0:
                session.close()
                return False
            query.delete(synchronize_session=False)
            session.commit()
            return True
        finally:
            session.close()

    @staticmethod
    def bulk_crear_horarios(horarios: List[Horario]) -> List[Horario]:
        session: Session = Database.get_session("rrhh")
        session.add_all(horarios)
        session.commit()
        for horario in horarios:
            session.refresh(horario)
        result = horarios.copy()
        session.close()
        return result

    @staticmethod
    def bulk_actualizar_horarios(horarios: List[Horario]) -> List[Horario]:
        session: Session = Database.get_session("rrhh")
        persisted_horarios = []
        for horario in horarios:
            persisted = session.merge(horario)
            persisted_horarios.append(persisted)
        session.commit()
        for ph in persisted_horarios:
            session.refresh(ph)
        result = persisted_horarios.copy()
        session.close()
        return result

    @staticmethod
    def get_horarios_por_sucursales(
        sucursal_ids: List[int],
        fecha_inicio: date,
        fecha_fin: date
    ) -> Dict[str, Any]:
        """
        Retorna la lista de sucursales filtradas por los ids proporcionados.
        Cada sucursal contendrá su lista de colaboradores (con id, username y email)
        y, para cada colaborador, la lista de puestos que correspondan a la sucursal actual y 
        cuyo campo 'fecha' se encuentre dentro del rango [fecha_inicio, fecha_fin],
        incluyendo sus horarios (hora_inicio y hora_fin).
        Además, se incluye el rango de fechas elegido en el resultado.
        """
        session: Session = Database.get_session("rrhh")
        try:
            sucursales = session.query(Sucursal).filter(
                Sucursal.id.in_(sucursal_ids)
            ).options(
                joinedload(Sucursal.colaboradores)
                .joinedload(ColaboradorSucursal.colaborador)
                .joinedload(Colaborador.puestos)
                .joinedload(Puesto.horarios)
            ).all()

            resultado: Dict[str, Any] = {
                "fecha_inicio": fecha_inicio.isoformat(),
                "fecha_fin": fecha_fin.isoformat(),
                "sucursales": []
            }

            for sucursal in sucursales:
                sucursal_data = {
                    "id": sucursal.id,
                    "nombre": sucursal.nombre,
                    "colaboradores": []
                }
                # Recorremos la relación intermedia ColaboradorSucursal
                for cs in sucursal.colaboradores:
                    colaborador = cs.colaborador
                    colaborador_data = {
                        "id": colaborador.id,
                        "nombre": colaborador.nombre,  # Se asume que el 'nombre' actúa como username
                        "email": colaborador.email,
                        "puestos": []
                    }
                    # Se itera sobre los puestos asociados al colaborador
                    for puesto in colaborador.puestos:
                        # Filtramos para incluir solo los puestos que pertenezcan a la sucursal actual 
                        # y cuya fecha esté dentro del rango especificado.
                        if puesto.sucursal_id == sucursal.id and fecha_inicio <= puesto.fecha <= fecha_fin:
                            puesto_data = {
                                "dia_id": puesto.dia_id,
                                "fecha": puesto.fecha.isoformat(),
                                "horarios": []
                            }
                            # Agregamos cada uno de los horarios asociados al puesto.
                            for horario in puesto.horarios:
                                horario_data = {
                                    "hora_inicio": horario.hora_inicio.strftime("%H:%M:%S"),
                                    "hora_fin": horario.hora_fin.strftime("%H:%M:%S")
                                }
                                puesto_data["horarios"].append(horario_data)
                            colaborador_data["puestos"].append(puesto_data)
                    sucursal_data["colaboradores"].append(colaborador_data)
                resultado["sucursales"].append(sucursal_data)

            return resultado
        finally:
            session.close()

    @staticmethod
    def bulk_crear_horarios_session(horarios: List[Horario], db: Optional[Session] = None) -> List[Horario]:
        close_session = False
        if db is None:
            db = Database.get_session("rrhh")
            close_session = True
        try:
            db.add_all(horarios)
            db.commit()
            for horario in horarios:
                db.refresh(horario)
            return horarios.copy()
        finally:
            if close_session:
                db.close()