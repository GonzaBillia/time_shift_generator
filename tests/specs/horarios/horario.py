import pytest
from datetime import time, date
from domain.models.horario import Horario
from domain.models.colaborador import Colaborador, TIEMPO_COMPLETO
from ....tests.mocks.mock_horarios import MockHorario
from ....tests.mocks.mock_colaborador import MockColaborador
from domain.specs.horario_specs import (
    HorarioRespetaHorasSemanales,
    DiaLibreSpecification,
    TipoEmpleadoSpecification,
    HorariosPorDefectoSpecification,
    HorarioCortadoSpecification,
)

# Tests para DiaLibreSpecification
def test_dia_libre_specification():
    horarios = [
        MockHorario(
            fecha=date(2025, 1, i),
            bloques=[(time(9, 0), time(17, 0))]
        )
        for i in range(1, 7)  # Lunes a sábado
    ]
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO, 
        horas_diarias_maximas=8, 
        horas_semanales=45, 
        horario_asignado=horarios
    )

    spec = DiaLibreSpecification()
    assert spec.is_satisfied_by(horarios[0], colaborador) == True

# Tests para TipoEmpleadoSpecification
def test_tipo_empleado_specification():
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO, 
        horas_diarias_maximas=8, 
        horas_semanales=45, 
        horario_asignado=[]
    )

    spec = TipoEmpleadoSpecification()
    assert spec.is_satisfied_by(None, colaborador) == True

# Tests para HorariosPorDefectoSpecification
def test_horarios_por_defecto_specification():
    horarios = [
        MockHorario(
            fecha=date(2025, 1, i),
            bloques=[(time(9, 0), time(16, 0))]
        )
        for i in range(1, 7)
    ]
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO,
        horas_diarias_maximas=8,
        horas_semanales=45,
        horario_asignado=horarios
    )

    spec = HorariosPorDefectoSpecification()
    # Pasar un horario específico del colaborador
    assert spec.is_satisfied_by(horarios[0], colaborador) == False

# Tests para HorarioCortadoSpecification
def test_horario_cortado_specification():
    # Crear un único objeto Horario con bloques de tiempo (representa horario cortado)
    horario_cortado = Horario(
        fecha=date(2025, 1, 1),
        bloques=[
            (time(9, 0), time(12, 0)),  # Primer bloque
            (time(16, 0), time(20, 0))  # Segundo bloque
        ],
        horario_corrido=False
    )
    
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO,
        horas_diarias_maximas=8,
        horas_semanales=45,
        horario_asignado=[horario_cortado],
        horario_corrido=False
    )

    spec = HorarioCortadoSpecification()
    # Pasar el horario del colaborador
    assert spec.is_satisfied_by(horario_cortado, colaborador) == True

