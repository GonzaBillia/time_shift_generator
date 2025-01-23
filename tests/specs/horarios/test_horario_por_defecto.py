import pytest
from datetime import time, date
from domain.models.horario import Horario
from domain.models.colaborador import Colaborador, TIEMPO_COMPLETO, TIEMPO_PARCIAL, HORARIO_ESPECIAL
from tests.mocks.mock_horarios import MockHorario
from tests.mocks.mock_colaborador import MockColaborador
from domain.specs.horario_specs import (
    HorariosPorDefectoSpecification
)

def test_happy_path_tiempo_completo():
    """
    Prueba de Camino Feliz para Tipo de Empleado 'TIEMPO_COMPLETO'.
    Verifica que los horarios asignados coincidan con las configuraciones por defecto:
    - 3 días de 7 horas
    - 3 días de 8 horas
    Total: 3*7 + 3*8 = 45 horas
    """
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

    spec = HorariosPorDefectoSpecification()
    # Pasar un horario específico del colaborador
    assert spec.is_satisfied_by(horarios[0], colaborador) == True, "Horario por defecto para TIEMPO_COMPLETO no cumplió."

def test_happy_path_tiempo_parcial():
    """
    Prueba de Camino Feliz para Tipo de Empleado 'TIEMPO_PARCIAL'.
    Verifica que los horarios asignados coincidan con las configuraciones por defecto:
    - 6 días de 5 horas
    Total: 6*5 = 30 horas
    """
    horarios = [
        MockHorario(
            fecha=date(2025, 1, 6),  # Lunes
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 7),  # Martes
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 8),  # Miércoles
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 9),  # Jueves
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 10),  # Viernes
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 11),  # Sábado
            bloques=[(time(9, 0), time(14, 0))]  # 5 horas
        ),
    ]
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_PARCIAL,
        horas_diarias_maximas=5,
        horas_semanales=30,
        horario_asignado=horarios
    )

    spec = HorariosPorDefectoSpecification()
    # Pasar un horario específico del colaborador
    assert spec.is_satisfied_by(horarios[0], colaborador) == True, "Horario por defecto para TIEMPO_PARCIAL no cumplió."

def test_happy_path_horario_especial():
    """
    Prueba de Camino Feliz para Tipo de Empleado 'HORARIO_ESPECIAL'.
    Verifica que los horarios asignados coincidan con las configuraciones por defecto:
    - 2 días de 11 horas
    Total: 2*11 = 22 horas
    """
    horarios = [
        MockHorario(
            fecha=date(2025, 1, 6),  # Lunes
            bloques=[(time(8, 0), time(19, 0))]  # 11 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 7),  # Martes
            bloques=[(time(8, 0), time(19, 0))]  # 11 horas
        ),
    ]
    colaborador = MockColaborador(
        tipo_empleado=HORARIO_ESPECIAL,
        horas_diarias_maximas=11,
        horas_semanales=22,
        horario_asignado=horarios
    )

    spec = HorariosPorDefectoSpecification()
    # Pasar un horario específico del colaborador
    assert spec.is_satisfied_by(horarios[0], colaborador) == True, "Horario por defecto para HORARIO_ESPECIAL no cumplió."

# ------------------------
# Funciones de Ruta Inválida
# ------------------------

def test_invalid_path_tiempo_completo():
    """
    Prueba de Ruta Inválida para Tipo de Empleado 'TIEMPO_COMPLETO'.
    Verifica que la especificación falle cuando las horas semanales no coinciden con las configuraciones por defecto.
    - Horas semanales incorrectas: 40 en lugar de 45.
    """
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
            bloques=[(time(9, 0), time(16, 0))]  # 7 horas
        ),
    ]
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO,
        horas_diarias_maximas=8,
        horas_semanales=40,  # Incorrecto, debería ser 45
        horario_asignado=horarios
    )

    spec = HorariosPorDefectoSpecification()
    # Pasar un horario específico del colaborador
    assert spec.is_satisfied_by(horarios[0], colaborador) == False, "Horario inválido para TIEMPO_COMPLETO no fue detectado."

def test_invalid_path_tiempo_parcial():
    """
    Prueba de Ruta Inválida para Tipo de Empleado 'TIEMPO_PARCIAL'.
    Verifica que la especificación falle cuando las horas semanales no coinciden con las configuraciones por defecto.
    - Horas semanales incorrectas: 35 en lugar de 30.
    """
    horarios = [
        MockHorario(
            fecha=date(2025, 1, 6),  # Lunes
            bloques=[(time(9, 0), time(15, 0))]  # 6 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 7),  # Martes
            bloques=[(time(9, 0), time(15, 0))]  # 6 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 8),  # Miércoles
            bloques=[(time(9, 0), time(15, 0))]  # 6 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 9),  # Jueves
            bloques=[(time(9, 0), time(15, 0))]  # 6 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 10),  # Viernes
            bloques=[(time(9, 0), time(15, 0))]  # 6 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 11),  # Sábado
            bloques=[(time(9, 0), time(15, 0))]  # 6 horas
        ),
    ]
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_PARCIAL,
        horas_diarias_maximas=5,
        horas_semanales=35,  # Incorrecto, debería ser 30
        horario_asignado=horarios
    )

    spec = HorariosPorDefectoSpecification()
    # Pasar un horario específico del colaborador
    assert spec.is_satisfied_by(horarios[0], colaborador) == False, "Horario inválido para TIEMPO_PARCIAL no fue detectado."

def test_invalid_path_horario_especial():
    """
    Prueba de Ruta Inválida para Tipo de Empleado 'HORARIO_ESPECIAL'.
    Verifica que la especificación falle cuando las horas semanales no coinciden con las configuraciones por defecto.
    - Horas semanales incorrectas: 20 en lugar de 22.
    """
    horarios = [
        MockHorario(
            fecha=date(2025, 1, 6),  # Lunes
            bloques=[(time(8, 0), time(19, 0))]  # 11 horas
        ),
        MockHorario(
            fecha=date(2025, 1, 7),  # Martes
            bloques=[(time(8, 0), time(18, 0))]  # 10 horas
        ),
    ]
    colaborador = MockColaborador(
        tipo_empleado=HORARIO_ESPECIAL,
        horas_diarias_maximas=11,
        horas_semanales=20,  # Incorrecto, debería ser 22
        horario_asignado=horarios
    )

    spec = HorariosPorDefectoSpecification()
    # Pasar un horario específico del colaborador
    assert spec.is_satisfied_by(horarios[0], colaborador) == False, "Horario inválido para HORARIO_ESPECIAL no fue detectado."