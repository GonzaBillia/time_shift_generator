# models/colaborador.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    dni = Column(Integer, nullable=False, unique=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    tipo_empleado_id = Column(Integer, ForeignKey("tipo_empleado.id"), nullable=False)
    horario_corrido = Column(Boolean, nullable=False, default=True)
    legajo = Column(Integer, nullable=False, unique=True)

    # Relaciones
    empresa = relationship("Empresa", back_populates="colaboradores")
    tipo_empleado = relationship("TipoEmpleado", back_populates="colaboradores")
    horarios = relationship("Horario", back_populates="colaborador")
    
    sucursales = relationship(
        "ColaboradorSucursal",
        back_populates="colaborador",
        cascade="all, delete-orphan"
    )

    vacaciones = relationship("VacacionColaborador", back_populates="colaborador")
    horas_extra = relationship("HorasExtraColaborador", back_populates="colaborador")

    # Nueva relación para horarios preferidos
    horarios_preferidos_colaboradores = relationship(
        "HorarioPreferidoColaborador", 
        back_populates="colaborador",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Colaborador(id={self.id}, nombre={self.nombre}, email={self.email}, "
            f"legajo={self.legajo}, empresa_id={self.empresa_id}, "
            f"tipo_empleado_id={self.tipo_empleado_id})>"
        )
