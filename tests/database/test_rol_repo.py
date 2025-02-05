import pytest
from infrastructure.repositories.rol_repo import RolRepository
from infrastructure.databases.models.rol import Rol

def test_create_rol():
    """Prueba la creación de un rol."""
    rol = Rol(nombre="Supervisor")
    rol_creado = RolRepository.create(rol)
    assert rol_creado.id is not None

def test_get_rol():
    """Prueba la obtención de un rol."""
    rol = RolRepository.get_by_nombre("Supervisor")
    assert rol is not None

def test_delete_rol():
    """Prueba la eliminación de un rol."""
    rol = RolRepository.get_by_nombre("Supervisor")
    assert RolRepository.delete(rol.id) == True
