from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_, cast, String
from infrastructure.databases.models.colaborador import Colaborador
from infrastructure.databases.models.horario import Horario
from infrastructure.databases.models.rol import Rol
from infrastructure.databases.models.tipo_colaborador import TipoEmpleado
from infrastructure.databases.models.vacacion_colaborador import VacacionColaborador
from infrastructure.databases.models.horas_extra_colaborador import HorasExtraColaborador

class ColaboradorRepository:
    @staticmethod
    def get_by_id(colaborador_id: int, db: Session) -> Optional[Colaborador]:
        return db.query(Colaborador).filter_by(id=colaborador_id).first()

    @staticmethod
    def get_by_legajo(legajo: int, db: Session) -> Optional[Colaborador]:
        return db.query(Colaborador).filter_by(legajo=legajo).first()

    @staticmethod
    def get_all(db: Session) -> List[Colaborador]:
        return db.query(Colaborador).all()
    
    @staticmethod
    def get_all_paginated(page: int, limit: int, search: str, db: Session) -> List[Colaborador]:
        offset = (page - 1) * limit
        query = db.query(Colaborador)
        
        if search.strip():
            # Filtros por nombre y dni en modo ilike
            filters = [
                Colaborador.nombre.ilike(f"%{search}%"),
                Colaborador.dni.ilike(f"%{search}%")
            ]
            # Si el término es numérico, filtra por legajo; de lo contrario, búsqueda parcial en legajo
            if search.isdigit():
                filters.append(Colaborador.legajo == int(search))
            else:
                filters.append(cast(Colaborador.legajo, String).ilike(f"%{search}%"))
            
            query = query.filter(or_(*filters))
        
        query = query.order_by(Colaborador.nombre.asc())
        return query.offset(offset).limit(limit).all()

    @staticmethod
    def get_filtered(
        dni: Optional[int] = None,
        empresa_id: Optional[int] = None,
        tipo_empleado_id: Optional[int] = None,
        horario_corrido: Optional[bool] = None,
        db: Session = None
    ) -> List[Colaborador]:
        # Se asume que 'db' es obligatorio y se inyecta desde el servicio o controlador.
        query = db.query(Colaborador)
        if dni is not None:
            query = query.filter(Colaborador.dni == dni)
        if empresa_id is not None:
            query = query.filter(Colaborador.empresa_id == empresa_id)
        if tipo_empleado_id is not None:
            query = query.filter(Colaborador.tipo_empleado_id == tipo_empleado_id)
        if horario_corrido is not None:
            query = query.filter(Colaborador.horario_corrido == horario_corrido)
        return query.all()

    @staticmethod
    def create(colaborador: Colaborador, db: Session) -> Colaborador:
        db.add(colaborador)
        db.commit()
        db.refresh(colaborador)
        return colaborador

    @staticmethod
    def update(colaborador: Colaborador, db: Session) -> Colaborador:
        db_colaborador = db.merge(colaborador)
        db.commit()
        db.refresh(db_colaborador)
        return db_colaborador

    @staticmethod
    def delete(colaborador_id: int, db: Session) -> bool:
        colaborador = db.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            db.delete(colaborador)
            db.commit()
            return True
        return False

    @staticmethod
    def get_by_email(email: str, db: Session) -> Optional[Colaborador]:
        return db.query(Colaborador).filter_by(email=email).first()

    @staticmethod
    def get_by_dni(dni: str, db: Session) -> Optional[Colaborador]:
        return db.query(Colaborador).filter_by(dni=dni).first()

    @staticmethod
    def asignar_horario(colaborador_id: int, horario: Horario, db: Session) -> None:
        colaborador = db.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            colaborador.horarios.append(horario)
            db.commit()

    @staticmethod
    def agregar_vacacion(colaborador_id: int, fecha: date, db: Session) -> None:
        colaborador = db.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            # Verificar si ya existe esa fecha en la lista de vacaciones
            existe = any(vac.fecha == fecha for vac in colaborador.vacaciones)
            if not existe:
                nueva_vac = VacacionColaborador(
                    colaborador_id=colaborador.id,
                    fecha=fecha
                )
                db.add(nueva_vac)
                db.commit()

    @staticmethod
    def agregar_horas_extra(colaborador_id: int, tipo: str, cantidad: int, db: Session) -> None:
        if tipo not in {'devolver', 'cobrar'}:
            raise ValueError("El tipo debe ser 'devolver' o 'cobrar'.")
        colaborador = db.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            # Opción: siempre crear un nuevo registro de horas extra.
            nueva_hx = HorasExtraColaborador(
                colaborador_id=colaborador.id,
                tipo=tipo,
                cantidad=cantidad
            )
            db.add(nueva_hx)
            db.commit()
