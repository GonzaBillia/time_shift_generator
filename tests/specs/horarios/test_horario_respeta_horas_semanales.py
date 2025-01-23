import pytest
from datetime import time, date
from domain.models.horario import Horario
from domain.models.colaborador import Colaborador, TIEMPO_COMPLETO, TIEMPO_PARCIAL, HORARIO_ESPECIAL
from tests.mocks.mock_horarios import MockHorario
from tests.mocks.mock_colaborador import MockColaborador
from domain.specs.horario_specs import (
    HorarioRespetaHorasSemanales
)

# Tests para HorarioRespetaHorasSemanales
def test_happy_path_tiempo_completo():
    horarios = [
        MockHorario(
            fecha=date(2025, 1, 6),  # Lunes
            bloques=[(time(9, 0), time(16, 0))]  # 7 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 7),  # Martes
            bloques=[(time(9, 0), time(16, 0))]  # 7 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 8),  # Miércoles
            bloques=[(time(9, 0), time(16, 0))]  # 7 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 9),  # Jueves
            bloques=[(time(9, 0), time(17, 0))]  # 8 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 10),  # Viernes
            bloques=[(time(9, 0), time(17, 0))]  # 8 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 11),  # Sábado
            bloques=[(time(9, 0), time(17, 0))]  # 8 horas
        ),
    ]
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO, 
        horas_diarias_maximas=8, 
        horas_semanales=45, 
        horario_asignado=horarios
    )

    spec = HorarioRespetaHorasSemanales()
    # Pasar cualquier horario, ya que la especificación evalúa todas las asignaciones
    assert spec.is_satisfied_by(horarios, colaborador) == True

    # Además, puedes agregar un assert para verificar que la suma es efectivamente 45
    assert colaborador.calcular_horas_totales_semanales() == 45

def test_happy_path_tiempo_parcial():
    horarios = [
        MockHorario(
            fecha=date(2025, 1, 6),
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 7),
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 8),
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 9),
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 10),
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 11),
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
    ]
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_PARCIAL, 
        horas_diarias_maximas=5, 
        horas_semanales=30, 
        horario_asignado=horarios
    )

    spec = HorarioRespetaHorasSemanales()
    # Pasar cualquier horario, ya que la especificación evalúa todas las asignaciones
    assert spec.is_satisfied_by(horarios, colaborador) == True

    # Además, puedes agregar un assert para verificar que la suma es efectivamente 30
    assert colaborador.calcular_horas_totales_semanales() == 30