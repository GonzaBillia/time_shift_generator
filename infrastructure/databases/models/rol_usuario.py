from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class RolUsuario(Base):
    __tablename__ = 'roles_usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(50), unique=True, nullable=False)
    
    # Relación con usuarios
    usuarios = relationship("Usuario", back_populates="rol_usuario")
