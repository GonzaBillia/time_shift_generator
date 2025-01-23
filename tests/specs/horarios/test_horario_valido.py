import pytest
from datetime import time, date
from domain.models.horario import Horario
from domain.models.colaborador import Colaborador, TIEMPO_COMPLETO
from tests.mocks.mock_horarios import MockHorario
from tests.mocks.mock_colaborador import MockColaborador
from domain.specs.horario_specs import (
    HorarioValidoSpecification
)

def test_happy_path():
    horario = MockHorario(
        fecha=date(2025, 1, 1),
        bloques=[(time(9, 0), time(17, 0))]
    )
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO, 
        horas_diarias_maximas=8, 
        horas_semanales=45, 
        horario_asignado=[horario]
    )

    spec = HorarioValidoSpecification()
    assert spec.is_satisfied_by(horario, colaborador) == True

def test_invalid_path():
    horario = MockHorario(
        fecha=date(2025, 1, 1),
        bloques=[(time(9, 0), time(18, 0))]
    )
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO, 
        horas_diarias_maximas=8, 
        horas_semanales=45, 
        horario_asignado=[horario]
    )

    spec = HorarioValidoSpecification()
    assert spec.is_satisfied_by(horario, colaborador) == False