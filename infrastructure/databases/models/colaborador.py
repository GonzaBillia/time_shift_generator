from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import DBConfig as Base

class Colaborador(Base):
    __tablename__ = "colaboradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    dni = Column(String(20), nullable=False, unique=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    tipo_empleado_id = Column(Integer, ForeignKey("tipo_empleado.id"), nullable=False)
    horario_corrido = Column(Boolean, nullable=False, default=True)

    # Relaciones
    empresa = relationship("Empresa", back_populates="colaboradores")
    tipo_empleado = relationship("TipoEmpleado", back_populates="colaboradores")
    horarios = relationship("Horario", back_populates="colaborador")
    sucursales = relationship("Sucursal", secondary="colaboradores_sucursales", back_populates="colaboradores")

    def __repr__(self):
        return f"<Colaborador(id={self.id}, nombre={self.nombre}, email={self.email}, empresa_id={self.empresa_id}, tipo_empleado_id={self.tipo_empleado_id})>"
