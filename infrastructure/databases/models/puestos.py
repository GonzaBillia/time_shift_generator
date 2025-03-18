from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class Puesto(Base):
    __tablename__ = "puestos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sucursal_id = Column(Integer, ForeignKey("sucursales.id"), nullable=False)
    rol_colaborador_id = Column(Integer, ForeignKey("roles_colaboradores.id"), nullable=False)
    dia_id = Column(Integer, ForeignKey("dias.id"), nullable=False)
    fecha = Column(Date, nullable=False)
    nombre = Column(String(100), nullable=False)
    # Se asigna en la fase de asignación; inicialmente puede ser None.
    colaborador_id = Column(Integer, ForeignKey("colaboradores.id"), nullable=True)

    # Relaciones
    sucursal = relationship("Sucursal", back_populates="puestos")
    rol_colaborador = relationship("Rol", back_populates="puestos")
    dia = relationship("Dia", back_populates="puestos")
    colaborador = relationship("Colaborador", back_populates="puestos")
    # Un puesto tendrá uno o más horarios (bloques)
    horarios = relationship("Horario", back_populates="puesto")

    def __repr__(self):
        return (
            f"<Puesto(id={self.id}, sucursal_id={self.sucursal_id}, "
            f"rol_colaborador_id={self.rol_colaborador_id}, dia_id={self.dia_id}, "
            f"fecha={self.fecha}, nombre='{self.nombre}', colaborador_id={self.colaborador_id})>"
        )
