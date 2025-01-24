# domain/models/horario.py

from datetime import date, time
from typing import List, Tuple

class Horario:
    def __init__(
        self,
        fecha: date,
        bloques: List[Tuple[time, time]],
        horario_corrido: bool = False
    ):
        """
        Inicializa un objeto Horario con múltiples bloques de tiempo.

        Args:
            fecha (date): Fecha del horario.
            bloques (List[Tuple[time, time]]): Lista de bloques (inicio, fin).
            horario_corrido (bool, optional): Define si es un horario corrido o no. Por defecto es False.

        Raises:
            ValueError: Si los datos proporcionados no son válidos.
        """
        self.fecha = fecha
        self.horario_corrido = horario_corrido

        if not bloques:
            raise ValueError("Debes proporcionar al menos un bloque de tiempo.")

        # Validar y ordenar los bloques
        self.bloques = sorted(bloques, key=lambda b: b[0])  # Ordenar bloques por hora de inicio
        self._validar_bloques()

    def _validar_bloques(self):
        """
        Valida los bloques de horario:
        - Verifica que cada bloque tenga una hora de inicio anterior a la hora de fin.
        - Verifica que los bloques no se superpongan entre sí.
        """
        for i, (inicio, fin) in enumerate(self.bloques):
            if fin <= inicio:
                raise ValueError(f"El bloque {i + 1} tiene una hora de fin anterior o igual a la hora de inicio.")
            if i > 0:  # Verificar superposición con el bloque anterior
                _, fin_anterior = self.bloques[i - 1]
                if inicio < fin_anterior:
                    raise ValueError(f"El bloque {i + 1} se superpone con el bloque anterior.")

    def duracion(self) -> int:
        """
        Calcula la duración total del horario en minutos.

        Returns:
            int: Duración total en minutos.
        """
        duracion_total = 0
        for inicio, fin in self.bloques:
            start_minutes = inicio.hour * 60 + inicio.minute
            end_minutes = fin.hour * 60 + fin.minute

            if end_minutes < start_minutes:
                # Horario que se extiende al día siguiente
                duracion = (24 * 60 - start_minutes) + end_minutes
            else:
                duracion = end_minutes - start_minutes

            duracion_total += duracion

        return duracion_total

    def se_superpone(self, otro_horario: 'Horario') -> bool:
        """
        Verifica si este horario se superpone con otro horario.

        Args:
            otro_horario (Horario): Otro objeto Horario.

        Returns:
            bool: True si algún bloque de este horario se superpone con algún bloque del otro horario.
        """
        if self.fecha != otro_horario.fecha:
            return False  # Los horarios no son del mismo día

        for inicio1, fin1 in self.bloques:
            for inicio2, fin2 in otro_horario.bloques:
                if not (fin1 <= inicio2 or fin2 <= inicio1):  # Hay superposición
                    return True

        return False
    
    def esta_dentro(self, otro: 'Horario') -> bool:
        """
        Verifica si todos los bloques de este horario están completamente contenidos dentro
        de los bloques del otro horario.

        Args:
            otro (Horario): El horario a comparar.

        Returns:
            bool: True si todos los bloques están dentro del otro horario, False de lo contrario.
        """
        if self.fecha != otro.fecha:
            return False  # Los horarios no son del mismo día

        for inicio1, fin1 in self.bloques:
            bloque_dentro = any(
                inicio2 <= inicio1 and fin1 <= fin2
                for inicio2, fin2 in otro.bloques
            )
            if not bloque_dentro:
                return False  # Si algún bloque no está contenido, retornamos False

        return True
