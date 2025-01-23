import pytest
from datetime import time, date
from domain.models.horario import Horario
from domain.models.colaborador import Colaborador, TIEMPO_COMPLETO, TIEMPO_PARCIAL, HORARIO_ESPECIAL
from tests.mocks.mock_horarios import MockHorario
from tests.mocks.mock_colaborador import MockColaborador
from domain.specs.horario_specs import (
    DiaLibreSpecification
)

# Test corregido para DiaLibreSpecification
def test_happy_path_tiempo_completo():
    # Crear horarios para Lunes a Sábado: 6 días de 8 horas cada uno
    horarios = [
        MockHorario(
            fecha=date(2025, 1, i),
            bloques=[(time(9, 0), time(17, 0))]  # 8 horas
        )
        for i in range(6, 12)  # 6 a 11 de enero de 2025 (Lunes a Sábado)
    ]
    
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO, 
        horas_diarias_maximas=8, 
        horas_semanales=45, 
        horario_asignado=horarios
    )

    spec = DiaLibreSpecification()
    
    # En esta especificación, el parámetro 'horario' no es relevante para la verificación de días libres,
    # ya que se revisan todos los horarios asignados al colaborador.
    # Por lo tanto, se puede pasar cualquier horario o incluso None si se ajusta la implementación.
    # Sin embargo, mantendremos el contrato de la interfaz y pasaremos el primer horario.
    
    assert spec.is_satisfied_by(horarios[0], colaborador) == True  # Debería tener al menos un día libre (domingo)

def test_invalid_path_tiempo_completo():
    # Crear horarios para Lunes a Sábado: 6 días de 8 horas cada uno
    horarios = [
        MockHorario(
            fecha=date(2025, 1, i),
            bloques=[(time(9, 0), time(17, 0))]  # 8 horas
        )
        for i in range(6, 13)  # 6 a 11 de enero de 2025 (Lunes a Sábado)
    ]
    
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO, 
        horas_diarias_maximas=8, 
        horas_semanales=45, 
        horario_asignado=horarios
    )

    spec = DiaLibreSpecification()
    
    # En esta especificación, el parámetro 'horario' no es relevante para la verificación de días libres,
    # ya que se revisan todos los horarios asignados al colaborador.
    # Por lo tanto, se puede pasar cualquier horario o incluso None si se ajusta la implementación.
    # Sin embargo, mantendremos el contrato de la interfaz y pasaremos el primer horario.
    
    assert spec.is_satisfied_by(horarios[0], colaborador) == False  # Debería tener al menos un día libre (domingo)
