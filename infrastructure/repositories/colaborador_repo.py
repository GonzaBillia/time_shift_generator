from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session

from infrastructure.databases.config.database import DBConfig as Database
from infrastructure.databases.models.colaborador import Colaborador
from infrastructure.databases.models.horario import Horario
from infrastructure.databases.models.rol import Rol
from infrastructure.databases.models.tipo_colaborador import TipoEmpleado
from infrastructure.databases.models.vacacion_colaborador import VacacionColaborador
from infrastructure.databases.models.horas_extra_colaborador import HorasExtraColaborador

class ColaboradorRepository:
    @staticmethod
    def get_by_id(colaborador_id: int) -> Optional[Colaborador]:
        """Obtiene un colaborador por su ID."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(id=colaborador_id).first()
        session.close()
        return colaborador

    @staticmethod
    def get_by_legajo(legajo: int) -> Optional[Colaborador]:
        """Obtiene un colaborador por su número de legajo."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(legajo=legajo).first()
        session.close()
        return colaborador

    @staticmethod
    def get_all() -> List[Colaborador]:
        """Obtiene todos los colaboradores."""
        session: Session = Database.get_session("rrhh")
        colaboradores = session.query(Colaborador).all()
        session.close()
        return colaboradores
    
    @staticmethod
    def get_filtered(
        dni: Optional[int] = None,
        empresa_id: Optional[int] = None,
        tipo_empleado_id: Optional[int] = None,
        horario_corrido: Optional[bool] = None,
    ) -> List[Colaborador]:
        session: Session = Database.get_session("rrhh")
        try:
            query = session.query(Colaborador)
            if dni is not None:
                query = query.filter(Colaborador.dni == dni)
            if empresa_id is not None:
                query = query.filter(Colaborador.empresa_id == empresa_id)
            if tipo_empleado_id is not None:
                query = query.filter(Colaborador.tipo_empleado_id == tipo_empleado_id)
            if horario_corrido is not None:
                query = query.filter(Colaborador.horario_corrido == horario_corrido)
            colaboradores = query.all()
        finally:
            session.close()
        return colaboradores

    @staticmethod
    def create(colaborador: Colaborador) -> Colaborador:
        """Crea un nuevo colaborador en la base de datos."""
        session: Session = Database.get_session("rrhh")
        session.add(colaborador)
        session.commit()
        session.refresh(colaborador)
        session.close()
        return colaborador

    @staticmethod
    def update(colaborador: Colaborador) -> Colaborador:
        session: Session = Database.get_session("rrhh")
        db_colaborador = session.merge(colaborador)
        session.commit()
        session.refresh(db_colaborador)
        session.close()
        return db_colaborador


    @staticmethod
    def delete(colaborador_id: int) -> bool:
        """Elimina un colaborador de la base de datos."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            session.delete(colaborador)
            session.commit()
            session.close()
            return True
        session.close()
        return False

    @staticmethod
    def get_by_email(email: str) -> Optional[Colaborador]:
        """Obtiene un colaborador por su email."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(email=email).first()
        session.close()
        return colaborador

    @staticmethod
    def get_by_dni(dni: str) -> Optional[Colaborador]:
        """Obtiene un colaborador por su DNI."""
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(dni=dni).first()
        session.close()
        return colaborador

    @staticmethod
    def asignar_horario(colaborador_id: int, horario: Horario) -> None:
        """
        Asigna un objeto Horario a un colaborador existente.
        El objeto 'horario' ya debe tener sucursal_id, dia_id, etc. configurados.
        """
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            colaborador.horarios.append(horario)
            session.commit()
        session.close()

    @staticmethod
    def agregar_vacacion(colaborador_id: int, fecha: date) -> None:
        """
        Agrega una fecha de vacaciones para el colaborador.
        Crea un objeto VacacionColaborador.
        """
        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            # Verificar si ya existe esa fecha en la lista de vacaciones
            existe = any(vac.fecha == fecha for vac in colaborador.vacaciones)
            if not existe:
                nueva_vac = VacacionColaborador(
                    colaborador_id=colaborador.id,
                    fecha=fecha
                )
                session.add(nueva_vac)
                session.commit()
        session.close()

    @staticmethod
    def agregar_horas_extra(colaborador_id: int, tipo: str, cantidad: int) -> None:
        """
        Agrega horas extra para un colaborador.
        'tipo' debe ser 'devolver' o 'cobrar'.
        Suma la cantidad de horas en una nueva fila HorasExtraColaborador (o actualiza la existente).
        """
        if tipo not in {'devolver', 'cobrar'}:
            raise ValueError("El tipo debe ser 'devolver' o 'cobrar'.")

        session: Session = Database.get_session("rrhh")
        colaborador = session.query(Colaborador).filter_by(id=colaborador_id).first()
        if colaborador:
            # Opción A: siempre crear un nuevo registro de horas extra.
            nueva_hx = HorasExtraColaborador(
                colaborador_id=colaborador.id,
                tipo=tipo,
                cantidad=cantidad
            )
            session.add(nueva_hx)

            # Opción B (alternativa): buscar si ya existe un registro con ese 'tipo' y sumarle 'cantidad'.
            # horas_extra_existente = session.query(HorasExtraColaborador).filter_by(
            #     colaborador_id=colaborador.id,
            #     tipo=tipo
            # ).first()
            # if horas_extra_existente:
            #     horas_extra_existente.cantidad += cantidad
            # else:
            #     nueva_hx = HorasExtraColaborador(
            #         colaborador_id=colaborador.id,
            #         tipo=tipo,
            #         cantidad=cantidad
            #     )
            #     session.add(nueva_hx)

            session.commit()
        session.close()
