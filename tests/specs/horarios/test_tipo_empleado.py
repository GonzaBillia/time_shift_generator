import pytest
from datetime import time, date
from domain.models.horario import Horario
from domain.models.colaborador import Colaborador, TIEMPO_COMPLETO, TIEMPO_PARCIAL, HORARIO_ESPECIAL
from tests.mocks.mock_horarios import MockHorario
from tests.mocks.mock_colaborador import MockColaborador
from domain.specs.horario_specs import (
    TipoEmpleadoSpecification
)

# Test para TipoEmpleadoSpecification - Tiempo Completo (Happy Path)
def test_happy_path_tiempo_completo():
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO, 
        horas_diarias_maximas=8, 
        horas_semanales=45, 
        horario_asignado=[]
    )

    spec = TipoEmpleadoSpecification()
    assert spec.is_satisfied_by(None, colaborador) == True, "TipoEmpleadoSpecification falló para TIEMPO_COMPLETO válido."

# Test para TipoEmpleadoSpecification - Tiempo Parcial (Happy Path)
def test_happy_path_tiempo_parcial():
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_PARCIAL, 
        horas_diarias_maximas=5, 
        horas_semanales=30, 
        horario_asignado=[]
    )

    spec = TipoEmpleadoSpecification()
    assert spec.is_satisfied_by(None, colaborador) == True, "TipoEmpleadoSpecification falló para TIEMPO_PARCIAL válido."

# Test para TipoEmpleadoSpecification - Horario Especial (Happy Path)
def test_happy_path_horario_especial():
    colaborador = MockColaborador(
        tipo_empleado=HORARIO_ESPECIAL, 
        horas_diarias_maximas=11, 
        horas_semanales=22, 
        horario_asignado=[]
    )

    spec = TipoEmpleadoSpecification()
    assert spec.is_satisfied_by(None, colaborador) == True, "TipoEmpleadoSpecification falló para HORARIO_ESPECIAL válido."

# Test para TipoEmpleadoSpecification - Tiempo Completo (Invalid Path)
def test_invalid_path_tiempo_completo():
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO, 
        horas_diarias_maximas=8, 
        horas_semanales=40,  # Incorrecto, debería ser 45
        horario_asignado=[]
    )

    spec = TipoEmpleadoSpecification()
    assert spec.is_satisfied_by(None, colaborador) == False, "TipoEmpleadoSpecification no detectó horas_semanales incorrectas para TIEMPO_COMPLETO."

# Test para TipoEmpleadoSpecification - Tiempo Parcial (Invalid Path)
def test_invalid_path_tiempo_parcial():
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_PARCIAL, 
        horas_diarias_maximas=5, 
        horas_semanales=35,  # Incorrecto, debería ser 30
        horario_asignado=[]
    )

    spec = TipoEmpleadoSpecification()
    assert spec.is_satisfied_by(None, colaborador) == False, "TipoEmpleadoSpecification no detectó horas_semanales incorrectas para TIEMPO_PARCIAL."

# Test para TipoEmpleadoSpecification - Horario Especial (Invalid Path)
def test_invalid_path_horario_especial():
    colaborador = MockColaborador(
        tipo_empleado=HORARIO_ESPECIAL, 
        horas_diarias_maximas=11, 
        horas_semanales=20,  # Incorrecto, debería ser 22
        horario_asignado=[]
    )

    spec = TipoEmpleadoSpecification()
    assert spec.is_satisfied_by(None, colaborador) == False, "TipoEmpleadoSpecification no detectó horas_semanales incorrectas para HORARIO_ESPECIAL."
