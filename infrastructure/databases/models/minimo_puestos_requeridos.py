from sqlalchemy import Column, Integer, Time, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class MinimoPuestosRequeridos(Base):
    __tablename__ = "minimo_puestos_requeridos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False)
    rol_colaborador_id = Column(Integer, ForeignKey("roles_colaboradores.id"), nullable=False)
    dia_id = Column(Integer, ForeignKey("dias.id"), nullable=False)
    hora = Column(Time, nullable=False)
    cantidad_minima = Column(Integer, nullable=False)

    # Relaciones
    sucursal = relationship("Sucursal", back_populates="minimo_puestos")
    rol_colaborador = relationship("Rol", back_populates="minimo_puestos")
    dia = relationship("Dia", back_populates="minimo_puestos")

    def __repr__(self):
        return (
            f"<MinimoPuestosRequeridos(id={self.id}, sucursal_id={self.sucursal_id}, "
            f"rol_colaborador_id={self.rol_colaborador_id}, dia_id={self.dia_id}, "
            f"hora={self.hora}, cantidad_minima={self.cantidad_minima})>"
        )
