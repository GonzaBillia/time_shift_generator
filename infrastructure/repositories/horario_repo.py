from typing import List, Optional, Dict, Any
from datetime import date
from sqlalchemy.orm import Session, joinedload

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.horario import Horario
from infrastructure.databases.models.sucursal import Sucursal
from infrastructure.databases.models.colaborador import Colaborador
from infrastructure.databases.models.colaborador_sucursal import ColaboradorSucursal
from infrastructure.databases.models.puestos import Puesto

class HorarioRepository:
    @staticmethod
    def get_by_id(horario_id: int, db: Session) -> Optional[Horario]:
        """
        Obtiene un Horario por su ID.
        Retorna None si no existe.
        """
        return db.query(Horario).filter_by(id=horario_id).first()

    @staticmethod
    def get_by_puesto(puesto_id: int, db: Session) -> List[Horario]:
        return db.query(Horario).filter_by(puesto_id=puesto_id).all()

    @staticmethod
    def get_by_puestos(puestos_ids: List[int], db: Session) -> List[Horario]:
        return db.query(Horario).filter(Horario.puesto_id.in_(puestos_ids)).all()

    @staticmethod
    def get_by_colaborador(colaborador_id: int, db: Session) -> List[Horario]:
        return db.query(Horario).filter_by(colaborador_id=colaborador_id).all()

    @staticmethod
    def get_all(db: Session) -> List[Horario]:
        """
        Devuelve todos los horarios registrados en la base de datos.
        """
        return db.query(Horario).all()

    @staticmethod
    def create(horario: Horario, db: Session) -> Horario:
        """
        Crea un nuevo Horario y lo persiste en la base de datos.
        Se asume que el commit se realizará externamente.
        """
        db.add(horario)
        db.flush()  # Sin commit, sincroniza para asignar ID si es necesario
        db.refresh(horario)
        return horario

    @staticmethod
    def update(horario: Horario, db: Session) -> Optional[Horario]:
        """
        Actualiza un Horario existente.
        Recibe un objeto Horario con id, hace 'merge' en la sesión y lo refresca.
        Retorna el Horario actualizado o None si no existe.
        """
        existente = db.query(Horario).filter_by(id=horario.id).first()
        if not existente:
            return None

        db_horario = db.merge(horario)
        db.flush()
        db.refresh(db_horario)
        return db_horario

    @staticmethod
    def delete(horario_id: int, db: Session) -> bool:
        """
        Elimina un Horario de la base de datos por su ID.
        Retorna True si se elimina, False si no existe.
        """
        horario = db.query(Horario).filter_by(id=horario_id).first()
        if horario:
            db.delete(horario)
            db.flush()
            return True
        return False

    @staticmethod
    def delete_many(horario_ids: List[int], db: Session) -> bool:
        """
        Elimina múltiples Horarios de la base de datos por sus IDs.
        Retorna True si se eliminó al menos uno, o False si ninguno fue encontrado.
        """
        query = db.query(Horario).filter(Horario.id.in_(horario_ids))
        if query.count() == 0:
            return False
        query.delete(synchronize_session=False)
        db.commit()
        return True

    @staticmethod
    def bulk_crear_horarios(horarios: List[Horario], db: Session) -> List[Horario]:
        db.add_all(horarios)
        db.commit()
        for horario in horarios:
            db.refresh(horario)
        return horarios.copy()

    @staticmethod
    def bulk_actualizar_horarios(horarios: List[Horario], db: Session) -> List[Horario]:
        persisted_horarios = []
        for horario in horarios:
            persisted = db.merge(horario)
            persisted_horarios.append(persisted)
        db.commit()
        for ph in persisted_horarios:
            db.refresh(ph)
        return persisted_horarios.copy()

    @staticmethod
    def get_horarios_por_sucursales(
        sucursal_ids: List[int],
        fecha_inicio: date,
        fecha_fin: date,
        db: Session
    ) -> Dict[str, Any]:
        """
        Retorna la lista de sucursales filtradas por los ids proporcionados.
        Cada sucursal contendrá su lista de colaboradores (con id, username y email)
        y, para cada colaborador, la lista de puestos que correspondan a la sucursal actual y 
        cuyo campo 'fecha' se encuentre dentro del rango [fecha_inicio, fecha_fin],
        incluyendo sus horarios (hora_inicio y hora_fin).
        Además, se incluye el rango de fechas elegido en el resultado.
        """
        sucursales = db.query(Sucursal).filter(
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
                    "nombre": colaborador.nombre,
                    "email": colaborador.email,
                    "puestos": []
                }
                # Se itera sobre los puestos asociados al colaborador
                for puesto in colaborador.puestos:
                    if puesto.sucursal_id == sucursal.id and fecha_inicio <= puesto.fecha <= fecha_fin:
                        puesto_data = {
                            "dia_id": puesto.dia_id,
                            "fecha": puesto.fecha.isoformat(),
                            "horarios": []
                        }
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

    @staticmethod
    def bulk_crear_horarios_session(horarios: List[Horario], db: Session) -> List[Horario]:
        db.add_all(horarios)
        db.commit()
        for horario in horarios:
            db.refresh(horario)
        return horarios.copy()
