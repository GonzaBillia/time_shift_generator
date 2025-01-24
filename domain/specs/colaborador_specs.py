from abc import abstractmethod
import re
from typing import List
from domain.models.colaborador import Colaborador, TIEMPO_COMPLETO, TIEMPO_PARCIAL, HORARIO_ESPECIAL

from .base import Specification

class ColaboradorSpecification(Specification):
    @abstractmethod
    def is_satisfied_by(self, colaborador: Colaborador):
        pass

class TipoEmpleadoSpecification(ColaboradorSpecification):
    def is_satisfied_by(self, colaborador: Colaborador) -> bool:
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

class EmailSpecification(ColaboradorSpecification):
    EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

    def is_satisfied_by(self, colaborador: Colaborador) -> bool:
        return bool(self.EMAIL_REGEX.match(colaborador.email))

class TelefonoSpecification(ColaboradorSpecification):
    PHONE_REGEX = re.compile(r"^\+?\d{7,15}$")  # Ejemplo: +1234567890 o 1234567

    def is_satisfied_by(self, colaborador: Colaborador) -> bool:
        return bool(self.PHONE_REGEX.match(colaborador.telefono))

class DNISpecification(ColaboradorSpecification):
    DNI_REGEX = re.compile(r"^\d{2}\.\d{3}\.\d{3}$")  # Ejemplo: 12.345.678

    def is_satisfied_by(self, colaborador: Colaborador) -> bool:
        return bool(self.DNI_REGEX.match(colaborador.dni))
    
class RolesSpecification(ColaboradorSpecification):
    VALID_ROLES = {'Desarrollador', 'Tester', 'Diseñador', 'Analista'}

    def is_satisfied_by(self, colaborador: Colaborador) -> bool:
        return (
            isinstance(colaborador.roles, list) and
            len(colaborador.roles) > 0 and
            all(role in self.VALID_ROLES for role in colaborador.roles)
        )

class HorarioAsignadoSpecification(ColaboradorSpecification):
    def is_satisfied_by(self, colaborador: Colaborador) -> bool:
        # Verificar total de horas semanales
        total_horas = colaborador.calcular_horas_totales_semanales()
        if total_horas != colaborador.horas_semanales:
            return False

        # Verificar horas diarias máximas
        for horario in colaborador.horario_asignado:
            horas_dia = horario.duracion() / 60
            if horas_dia > colaborador.horas_diarias_maximas:
                return False

        # Verificar superposición de horarios
        horarios = colaborador.horario_asignado
        for i in range(len(horarios)):
            for j in range(i + 1, len(horarios)):
                if horarios[i].se_superpone(horarios[j]):
                    return False

        return True

class DiasPreferidosSpecification(ColaboradorSpecification):
    def is_satisfied_by(self, colaborador: Colaborador) -> bool:
        if not isinstance(colaborador.dias_preferidos, list):
            return False
        if not all(isinstance(dia, int) and 0 <= dia <= 6 for dia in colaborador.dias_preferidos):
            return False
        # Asegurar que no trabaje todos los días
        return len(colaborador.dias_preferidos) < 7

class VacacionesSpecification(ColaboradorSpecification):
    def is_satisfied_by(self, colaborador: Colaborador) -> bool:
        for vacacion in colaborador.vacaciones:
            for horario in colaborador.horario_asignado:
                if vacacion == horario.fecha:
                    return False
        return True