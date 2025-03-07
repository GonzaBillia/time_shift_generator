from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey, func
from sqlalchemy.orm import relationship
from infrastructure.databases.config.database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True, index=True)
    colaborador_id = Column(Integer, ForeignKey('colaboradores.id'), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)  # Se cambió contraseña_hash por password_hash
    rol_usuario_id = Column(Integer, ForeignKey('roles_usuarios.id'), nullable=False)
    
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=False, server_default=func.now(), onupdate=func.now())
    last_login = Column(TIMESTAMP, nullable=True)
    token_version = Column(Integer, nullable=False, default=0)
    
    
    # Relación con roles_usuarios
    rol_usuario = relationship("RolUsuario", back_populates="usuarios")
