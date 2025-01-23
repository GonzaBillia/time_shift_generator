from datetime import date, time
from typing import List, Tuple

class MockHorario:
    def __init__(self, fecha: date, bloques: List[Tuple[time, time]]):
        """
        Inicializa un objeto MockHorario.

        Args:
            fecha (date): Fecha del horario.
            bloques (List[Tuple[time, time]]): Lista de tuplas con hora de inicio y fin.
        """
        self.fecha = fecha  # Objeto datetime.date
        self.bloques = bloques  # Lista de tuplas [(hora_inicio, hora_fin)]

    def duracion(self) -> int:
        """
        Calcula la duración total de todos los bloques en minutos.

        Returns:
            int: Duración total en minutos.
        """
        duracion_total = 0
        for bloque in self.bloques:
            if len(bloque) != 2:
                raise ValueError("Cada bloque debe ser una tupla de (hora_inicio, hora_fin).")
            inicio, fin = bloque
            inicio_minutos = inicio.hour * 60 + inicio.minute
            fin_minutos = fin.hour * 60 + fin.minute
            if fin_minutos < inicio_minutos:
                # Asume que el horario se extiende al día siguiente
                duracion_total += (24 * 60 - inicio_minutos) + fin_minutos
            else:
                duracion_total += fin_minutos - inicio_minutos
        return duracion_total
