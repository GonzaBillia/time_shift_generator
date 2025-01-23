# domain/specifications/horario_specifications.py

from abc import abstractmethod
from typing import List
from domain.models.horario import Horario
from domain.models.colaborador import Colaborador, TIEMPO_COMPLETO, TIEMPO_PARCIAL, HORARIO_ESPECIAL

from .base import Specification

class HorarioSpecification(Specification):
    @abstractmethod
    def is_satisfied_by(self, horario: Horario, colaborador: Colaborador) -> bool:
        """
        Determina si el horario cumple con la especificación dada para el colaborador.

        Args:
            horario (Horario): El horario a evaluar.
            colaborador (Colaborador): El colaborador al que se asigna el horario.

        Returns:
            bool: True si se cumple la especificación, False en caso contrario.
        """
        pass

    def calcular_horas_totales_semanales(self, colaborador: Colaborador) -> float:
        """
        Calcula el total de horas trabajadas por un colaborador en una semana.

        Args:
            colaborador (Colaborador): El colaborador.

        Returns:
            float: El total de horas trabajadas en la semana.
        """
        return colaborador.calcular_horas_totales_semanales()


class HorarioValidoSpecification(HorarioSpecification):
    def is_satisfied_by(self, horario: Horario, colaborador: Colaborador) -> bool:
        """
        Verifica que la duración del horario no exceda las horas diarias máximas permitidas para el colaborador.

        Args:
            horario (Horario): El horario a evaluar.
            colaborador (Colaborador): El colaborador al que se asigna el horario.

        Returns:
            bool: True si la duración es válida, False en caso contrario.
        """
        duracion_minutos = horario.duracion()
        horas_maximas_minutos = colaborador.horas_diarias_maximas * 60
        return duracion_minutos <= horas_maximas_minutos


class HorarioRespetaHorasSemanales(HorarioSpecification):
    def is_satisfied_by(self, horario: Horario, colaborador: Colaborador) -> bool:
        """
        Verifica que el total de horas semanales del colaborador no exceda las horas semanales permitidas.

        Args:
            horario (Horario): El horario a evaluar (puede ser ignorado en esta especificación).
            colaborador (Colaborador): El colaborador al que se asigna el horario.

        Returns:
            bool: True si se respeta el límite semanal, False en caso contrario.
        """
        horas_totales_semanales = self.calcular_horas_totales_semanales(colaborador)
        return horas_totales_semanales == colaborador.horas_semanales


class DiaLibreSpecification(HorarioSpecification):
    def is_satisfied_by(self, horario: Horario, colaborador: Colaborador) -> bool:
        """
        Verifica que los empleados de TIEMPO_COMPLETO y TIEMPO_PARCIAL tengan al menos un día libre por semana.

        Args:
            horario (Horario): El horario a evaluar (puede ser ignorado en esta especificación).
            colaborador (Colaborador): El colaborador al que se asigna el horario.

        Returns:
            bool: True si se cumple la especificación, False en caso contrario.
        """
        tipo = colaborador.tipo_empleado
        if tipo not in {TIEMPO_COMPLETO, TIEMPO_PARCIAL}:
            return True  # No aplica para otros tipos

        # Obtener los días trabajados (0=Monday, 6=Sunday)
        dias_trabajados = set(horario.fecha.weekday() for horario in colaborador.horario_asignado)
        # Verificar que no se trabajen los 7 días
        return len(dias_trabajados) < 7  # Al menos un día libre


class TipoEmpleadoSpecification(HorarioSpecification):
    def is_satisfied_by(self, horario: Horario, colaborador: Colaborador) -> bool:
        """
        Verifica que el tipo de empleado tenga las horas semanales y configuraciones por defecto correctas.

        Args:
            horario (Horario): El horario a evaluar (puede ser ignorado en esta especificación).
            colaborador (Colaborador): El colaborador al que se asigna el horario.

        Returns:
            bool: True si se cumple la especificación, False en caso contrario.
        """
        tipo = colaborador.tipo_empleado
        horas_semanales = colaborador.horas_semanales

        if tipo == TIEMPO_COMPLETO and horas_semanales != 45:
            return False
        elif tipo == TIEMPO_PARCIAL and horas_semanales != 30:
            return False
        elif tipo == HORARIO_ESPECIAL and horas_semanales != 22:
            return False
        return True


class HorariosPorDefectoSpecification(HorarioSpecification):
    def is_satisfied_by(self, horario: Horario, colaborador: Colaborador) -> bool:
        """
        Verifica que los horarios asignados coincidan con las configuraciones por defecto del tipo de empleado.

        Args:
            horario (Horario): El horario a evaluar (puede ser ignorado en esta especificación).
            colaborador (Colaborador): El colaborador al que se asigna el horario.

        Returns:
            bool: True si se cumple la especificación, False en caso contrario.
        """
        tipo = colaborador.tipo_empleado

        if tipo == TIEMPO_COMPLETO:
            # Espera 3 días de 7hs y 3 días de 8hs
            conteo_7 = sum(1 for h in colaborador.horario_asignado if h.duracion() / 60 == 7)
            conteo_8 = sum(1 for h in colaborador.horario_asignado if h.duracion() / 60 == 8)
            return conteo_7 == 3 and conteo_8 == 3

        elif tipo == TIEMPO_PARCIAL:
            # Espera 6 días de 5hs
            conteo_5 = sum(1 for h in colaborador.horario_asignado if h.duracion() / 60 == 5)
            return conteo_5 == 6

        elif tipo == HORARIO_ESPECIAL:
            # Espera 2 días de 11hs
            conteo_11 = sum(1 for h in colaborador.horario_asignado if h.duracion() / 60 == 11)
            return conteo_11 == 2

        return False


class HorarioCortadoSpecification(HorarioSpecification):
    def is_satisfied_by(self, horario: Horario, colaborador: Colaborador) -> bool:
        """
        Verifica las reglas específicas para horarios cortados:
        - Cada bloque es mínimo de 3 horas.
        - Los dos bloques deben estar en el mismo día para completar la jornada.
        - El espacio entre bloques debe ser mínimo de 4 horas.

        Args:
            horario (Horario): El horario a evaluar.
            colaborador (Colaborador): El colaborador al que se asigna el horario.

        Returns:
            bool: True si se cumplen todas las reglas, False en caso contrario.
        """
        if colaborador.horario_corrido:
            return True  # No aplica si es horario corrido

        bloques = horario.bloques
        if len(bloques) != 2:
            return False  # Deben ser exactamente 2 bloques para horario cortado

        # Validar duración mínima de cada bloque
        for i, (inicio, fin) in enumerate(bloques):
            duracion_minutos = fin.hour * 60 + fin.minute - inicio.hour * 60 - inicio.minute
            if duracion_minutos < 3 * 60:
                return False  # Cada bloque debe ser al menos de 3 horas

        # Validar espacio entre bloques
        # Asumiendo que los bloques están ordenados por hora de inicio
        fin_primero = bloques[0][1]
        inicio_segundo = bloques[1][0]
        espacio_minutos = (inicio_segundo.hour * 60 + inicio_segundo.minute) - (fin_primero.hour * 60 + fin_primero.minute)
        if espacio_minutos < 4 * 60:
            return False  # Debe haber al menos 4 horas de espacio entre bloques

        # Validar suma total de bloques (7 u 8 horas)
        duracion_total = horario.duracion() / 60  # Convertir a horas
        return duracion_total in {7, 8}
