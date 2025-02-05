from sqlalchemy import Column, Integer, Time, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import DBConfig as Base

class PuestosCubiertosPorHora(Base):
    __tablename__ = "puestos_cubiertos_por_hora"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False)
    rol_colaborador_id = Column(Integer, ForeignKey("roles_colaboradores.id"), nullable=False)
    dia_id = Column(Integer, ForeignKey("dias.id"), nullable=False)
    hora = Column(Time, nullable=False)
    cantidad_cubierta = Column(Integer, nullable=False)

    # Relaciones
    sucursal = relationship("Sucursal", back_populates="puestos_cubiertos")
    rol_colaborador = relationship("Rol", back_populates="puestos_cubiertos")
    dia = relationship("Dia", back_populates="puestos_cubiertos")

    def __repr__(self):
        return f"<PuestosCubiertosPorHora(id={self.id}, sucursal_id={self.sucursal_id}, rol_colaborador_id={self.rol_colaborador_id}, dia_id={self.dia_id}, hora={self.hora}, cantidad_cubierta={self.cantidad_cubierta})>"
