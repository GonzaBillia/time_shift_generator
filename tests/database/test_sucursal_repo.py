import pytest
from infrastructure.repositories.sucursal_repo import SucursalRepository
from infrastructure.databases.models.sucursal import Sucursal

def test_create_sucursal():
    """Prueba la creación de una sucursal."""
    sucursal = Sucursal(
        nombre="Sucursal Centro",
        empresa_id=1,
        direccion="Av. Principal 123",
        telefono="5551234",
        formato_id=1
    )
    sucursal_creada = SucursalRepository.create(sucursal)
    assert sucursal_creada.id is not None

def test_get_sucursal():
    """Prueba la obtención de una sucursal."""
    sucursal = SucursalRepository.get_by_nombre("Sucursal Centro")
    assert sucursal is not None
    assert sucursal.direccion == "Av. Principal 123"

def test_delete_sucursal():
    """Prueba la eliminación de una sucursal."""
    sucursal = SucursalRepository.get_by_nombre("Sucursal Centro")
    assert SucursalRepository.delete(sucursal.id) == True
