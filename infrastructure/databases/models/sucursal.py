from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class Sucursal(Base):
    __tablename__ = "sucursales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False, unique=True)
    direccion = Column(String, nullable=False)
    telefono = Column(String(20), nullable=True)
    empresa_id = Column(Integer, ForeignKey("empresas.id"), nullable=False)
    formato_id = Column(Integer, ForeignKey("formatos_sucursales.id"), nullable=False)

    # Relaciones existentes
    empresa = relationship("Empresa", back_populates="sucursales")
    formato = relationship("Formato", back_populates="sucursales")
    puestos = relationship("Puesto", back_populates="sucursal")
    
    # Nueva relación con HorarioPreferidoColaborador
    horarios_preferidos_colaboradores = relationship("HorarioPreferidoColaborador", back_populates="sucursal")

    # Asociación con Colaborador (vía ColaboradorSucursal)
    colaboradores = relationship(
        "ColaboradorSucursal",
        back_populates="sucursal",
        cascade="all, delete-orphan"
    )

    # Otras relaciones
    horarios_sucursal = relationship("HorarioSucursal", back_populates="sucursal")
    espacios_disponibles = relationship("EspacioDisponibleSucursal", back_populates="sucursal")
    minimo_puestos = relationship("MinimoPuestosRequeridos", back_populates="sucursal")
    puestos_cubiertos = relationship("PuestosCubiertosPorHora", back_populates="sucursal")

    def __repr__(self):
        return (
            f"<Sucursal(id={self.id}, nombre={self.nombre}, "
            f"empresa_id={self.empresa_id}, formato_id={self.formato_id})>"
        )
