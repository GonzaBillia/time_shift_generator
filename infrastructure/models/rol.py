from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class Rol(Base):
    __tablename__ = "roles_colaboradores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False, unique=True)
    principal = Column(Boolean, nullable=False, default=False)

    # Asociación con Formato -> FormatosRoles
    formatos = relationship(
        "FormatosRoles",
        back_populates="rol",
        cascade="all, delete-orphan"
    )

    # Asociación con ColaboradorSucursal
    colaboradores_sucursales = relationship("ColaboradorSucursal", back_populates="rol_colaborador")

    # Relaciones con otras tablas
    espacios_disponibles = relationship("EspacioDisponibleSucursal", back_populates="rol_colaborador")
    minimo_puestos = relationship("MinimoPuestosRequeridos", back_populates="rol_colaborador")
    puestos_cubiertos = relationship("PuestosCubiertosPorHora", back_populates="rol_colaborador")

    def __repr__(self):
        return f"<Rol(id={self.id}, nombre={self.nombre}, principal={self.principal})>"
