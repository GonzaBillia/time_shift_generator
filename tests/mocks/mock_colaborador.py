from typing import List
from tests.mocks.mock_horarios import MockHorario

class MockColaborador:
    def __init__(
        self, 
        tipo_empleado: str, 
        horas_diarias_maximas: int, 
        horas_semanales: int, 
        horario_asignado: List[MockHorario]
    ):
        """
        Inicializa un objeto MockColaborador.

        Args:
            tipo_empleado (str): Tipo de empleado ('tiempo completo', 'tiempo parcial', 'horario especial').
            horas_diarias_maximas (int): Máximo de horas diarias permitidas.
            horas_semanales (int): Horas semanales asignadas.
            horario_asignado (List[MockHorario]): Lista de horarios asignados.
        """
        self.tipo_empleado = tipo_empleado
        self.horas_diarias_maximas = horas_diarias_maximas
        self.horas_semanales = horas_semanales
        self.horario_asignado = horario_asignado  # Lista de objetos MockHorario

    def calcular_horas_totales_semanales(self) -> float:
        """
        Calcula el total de horas trabajadas por el colaborador en una semana.

        Returns:
            float: Total de horas trabajadas en la semana.
        """
        if not self.horario_asignado:
            return 0.0

        minutos_totales = sum(horario.duracion() for horario in self.horario_asignado)
        horas_totales = minutos_totales / 60
        return horas_totales
