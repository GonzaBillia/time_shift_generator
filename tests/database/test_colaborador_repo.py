import pytest
from infrastructure.repositories.colaborador_repo import ColaboradorRepository
from infrastructure.databases.models.colaborador import Colaborador

# def test_create_colaborador():
    # """Prueba la creación de un colaborador."""
    # colaborador = Colaborador(
    #     nombre="Juan Pérez",
    #     email="juan@example.com",
    #     telefono="123456789",
    #     dni="12345678",
    #     empresa_id=1,
    #     tipo_empleado_id=1,
    #     legajo=1001  # ¡Ahora es obligatorio!
    # )
    # colaborador_creado = ColaboradorRepository.create(colaborador)
    # assert colaborador_creado.id is not None
    # assert colaborador_creado.legajo == 1001


def test_get_colaborador():
    """Prueba la obtención de un colaborador."""
    colaborador = ColaboradorRepository.get_by_legajo(1001)
    assert colaborador is not None
    assert colaborador.nombre == "Juan Pérez"

# def test_delete_colaborador():
#     """Prueba la eliminación de un colaborador."""
#     colaborador = ColaboradorRepository.get_by_legajo(1001)
#     assert ColaboradorRepository.delete(colaborador.id) == True
