from typing import List
from tests.mocks.mock_horarios import MockHorario

class MockColaborador:
    def __init__(
        self,
        tipo_empleado: str,
        horas_diarias_maximas: int,
        horas_semanales: int,
        horario_asignado: list,
        horario_corrido: bool = True
    ):
        """
        Mock de la clase Colaborador con solo los atributos necesarios para el test.
        """
        self.tipo_empleado = tipo_empleado
        self.horas_diarias_maximas = horas_diarias_maximas
        self.horas_semanales = horas_semanales
        self.horario_asignado = horario_asignado
        self.horario_corrido = horario_corrido

    def calcular_horas_totales_semanales(self) -> float:
        """
        Calcula el total de horas trabajadas en la semana.
        """
        minutos_totales = sum(horario.duracion() for horario in self.horario_asignado)
        horas_totales = minutos_totales / 60
        return horas_totales
