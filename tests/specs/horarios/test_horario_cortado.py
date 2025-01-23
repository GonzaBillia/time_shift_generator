import pytest
from datetime import time, date
from domain.models.horario import Horario
from domain.models.colaborador import Colaborador, TIEMPO_COMPLETO, TIEMPO_PARCIAL, HORARIO_ESPECIAL
from tests.mocks.mock_horarios import MockHorario
from tests.mocks.mock_colaborador import MockColaborador
from domain.specs.horario_specs import (
    HorarioCortadoSpecification
)

def test_happy_path_tiempo_completo():
    """
    Prueba de Camino Feliz para Tipo de Empleado 'TIEMPO_COMPLETO'.
    Verifica que los horarios asignados cumplan con las configuraciones por defecto:
    - 2 bloques por día.
    - Cada bloque tiene al menos 3 horas.
    - Espacio entre bloques es de al menos 4 horas.
    - Duración total de 7 u 8 horas.
    """
    # Crear un horario cortado válido
    horario_cortado = MockHorario(
        fecha=date(2025, 1, 6),  # Lunes
        bloques=[
            (time(9, 0), time(12, 0)),  # 3 horas
            (time(16, 0), time(20, 0))  # 4 horas
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
    assert spec.is_satisfied_by(horario_cortado, colaborador) == True, "Horario cortado válido para TIEMPO_COMPLETO no pasó la especificación."

def test_invalid_path_tiempo_completo_mas_de_dos_bloques():
    """
    Prueba de Ruta Inválida para Tipo de Empleado 'TIEMPO_COMPLETO'.
    Verifica que la especificación falle cuando hay más de dos bloques.
    """
    # Crear un horario con más de dos bloques
    horario_invalido = MockHorario(
        fecha=date(2025, 1, 6),  # Lunes
        bloques=[
            (time(9, 0), time(12, 0)),  # 3 horas
            (time(13, 0), time(15, 0)),  # 2 horas
            (time(16, 0), time(20, 0))   # 4 horas
        ],
        horario_corrido=False
    )
    
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO,
        horas_diarias_maximas=8,
        horas_semanales=45,
        horario_asignado=[horario_invalido],
        horario_corrido=False
    )

    spec = HorarioCortadoSpecification()
    # Pasar el horario inválido del colaborador
    assert spec.is_satisfied_by(horario_invalido, colaborador) == False, "Horario con más de dos bloques no fue detectado como inválido para TIEMPO_COMPLETO."

def test_invalid_path_tiempo_completo_bloque_tiempo_insuficiente():
    """
    Prueba de Ruta Inválida para Tipo de Empleado 'TIEMPO_COMPLETO'.
    Verifica que la especificación falle cuando un bloque tiene menos de 3 horas.
    """
    # Crear un horario donde el segundo bloque tiene solo 2 horas
    horario_invalido = MockHorario(
        fecha=date(2025, 1, 6),  # Lunes
        bloques=[
            (time(9, 0), time(12, 0)),  # 3 horas
            (time(16, 0), time(18, 0))   # 2 horas (insuficiente)
        ],
        horario_corrido=False
    )
    
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO,
        horas_diarias_maximas=8,
        horas_semanales=45,
        horario_asignado=[horario_invalido],
        horario_corrido=False
    )

    spec = HorarioCortadoSpecification()
    # Pasar el horario inválido del colaborador
    assert spec.is_satisfied_by(horario_invalido, colaborador) == False, "Horario con bloque de tiempo insuficiente no fue detectado como inválido para TIEMPO_COMPLETO."

def test_invalid_path_tiempo_completo_espacio_insuficiente_entre_bloques():
    """
    Prueba de Ruta Inválida para Tipo de Empleado 'TIEMPO_COMPLETO'.
    Verifica que la especificación falle cuando el espacio entre bloques es menor a 4 horas.
    """
    # Crear un horario donde el espacio entre bloques es de solo 3 horas
    horario_invalido = MockHorario(
        fecha=date(2025, 1, 6),  # Lunes
        bloques=[
            (time(9, 0), time(12, 0)),  # 3 horas
            (time(15, 0), time(20, 0))   # 5 horas (espacio de 3 horas entre 12:00 y 15:00)
        ],
        horario_corrido=False
    )
    
    colaborador = MockColaborador(
        tipo_empleado=TIEMPO_COMPLETO,
        horas_diarias_maximas=8,
        horas_semanales=45,
        horario_asignado=[horario_invalido],
        horario_corrido=False
    )

    spec = HorarioCortadoSpecification()
    # Pasar el horario inválido del colaborador
    assert spec.is_satisfied_by(horario_invalido, colaborador) == False, "Horario con espacio insuficiente entre bloques no fue detectado como inválido para TIEMPO_COMPLETO."

