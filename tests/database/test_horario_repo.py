import pytest
from infrastructure.repositories.horario_repo import HorarioRepository
from infrastructure.databases.models.horario import Horario
from datetime import date, time

def test_create_horario():
    """Prueba la creación de un horario."""
    horario = Horario(
        sucursal_id=1,
        colaborador_id=1,
        dia_id=2,  # Martes
        fecha=date(2024, 6, 20),
        hora_inicio=time(9, 0),
        hora_fin=time(17, 0),
        horario_corrido=True
    )
    horario_creado = HorarioRepository.create(horario)
    assert horario_creado.id is not None

def test_get_horario():
    """Prueba la obtención de un horario."""
    horarios = HorarioRepository.get_by_colaborador(1)
    assert len(horarios) > 0

def test_delete_horario():
    """Prueba la eliminación de un horario."""
    horario = HorarioRepository.get_by_colaborador(1)[0]
    assert HorarioRepository.delete(horario.id) == True
