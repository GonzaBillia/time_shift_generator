from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class EspacioDisponibleSucursal(Base):
    __tablename__ = "espacios_disponibles_sucursal"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False)
    rol_colaborador_id = Column(Integer, ForeignKey("roles_colaboradores.id"), nullable=False)
    cantidad = Column(Integer, nullable=False)
    limitado_por_pc = Column(Boolean, nullable=False, default=False)

    # Relaciones
    sucursal = relationship("Sucursal", back_populates="espacios_disponibles")
    rol_colaborador = relationship("Rol", back_populates="espacios_disponibles")

    def __repr__(self):
        return (
            f"<EspacioDisponibleSucursal(id={self.id}, sucursal_id={self.sucursal_id}, "
            f"rol_colaborador_id={self.rol_colaborador_id}, cantidad={self.cantidad}, "
            f"limitado_por_pc={self.limitado_por_pc})>"
        )
