from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class ColaboradorSucursal(Base):
    __tablename__ = "colaboradores_sucursales"

    id = Column(Integer, primary_key=True, autoincrement=True)
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id", ondelete="CASCADE"), nullable=False)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id", ondelete="CASCADE"), nullable=False)
    rol_colaborador_id = Column(Integer, ForeignKey("roles_colaboradores.id", ondelete="CASCADE"), nullable=False)

    # Relaciones
    colaborador = relationship("Colaborador", back_populates="sucursales")
    sucursal = relationship("Sucursal", back_populates="colaboradores")
    rol_colaborador = relationship("Rol", back_populates="colaboradores_sucursales")

    def __repr__(self):
        return (
            f"<ColaboradorSucursal(id={self.id}, colaborador_id={self.colaborador_id}, "
            f"sucursal_id={self.sucursal_id}, rol_colaborador_id={self.rol_colaborador_id})>"
        )
