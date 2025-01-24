from abc import abstractmethod
from typing import Dict
from domain.models.sucursal import Sucursal
from domain.models.horario import Horario
from .base import Specification


class SucursalSpecification(Specification):
    @abstractmethod
    def is_satisfied_by(self, sucursal: Sucursal) -> bool:
        pass


class CapacidadRolSpecification(SucursalSpecification):
    def __init__(self, rol: str, capacidad_minima: int):
        """
        Verifica que una sucursal tenga una capacidad mínima disponible para un rol específico.

        Args:
            rol (str): Nombre del rol a validar.
            capacidad_minima (int): Capacidad mínima requerida.
        """
        self.rol = rol
        self.capacidad_minima = capacidad_minima

    def is_satisfied_by(self, sucursal: Sucursal) -> bool:
        capacidad_disponible = sucursal.verificar_disponibilidad().get(self.rol, 0)
        return capacidad_disponible >= self.capacidad_minima


class FormatoSucursalSpecification(SucursalSpecification):
    def __init__(self, formato_esperado: str):
        """
        Verifica que el formato de la sucursal sea el esperado.

        Args:
            formato_esperado (str): Nombre del formato esperado.
        """
        self.formato_esperado = formato_esperado

    def is_satisfied_by(self, sucursal: Sucursal) -> bool:
        return sucursal.formato.nombre == self.formato_esperado


class HorarioAtencionSpecification(SucursalSpecification):
    def __init__(self, horario: Horario):
        """
        Verifica que el horario de atención de la sucursal incluya el horario especificado.

        Args:
            horario (Horario): Objeto Horario a verificar.
        """
        self.horario = horario

    def is_satisfied_by(self, sucursal: Sucursal) -> bool:
        return sucursal.horario_atencion.esta_dentro(self.horario)


class DiasAtencionSpecification(SucursalSpecification):
    def __init__(self, dias_requeridos: Dict[str, Horario]):
        """
        Verifica que la sucursal opere los días requeridos con los horarios especificados.

        Args:
            dias_requeridos (Dict[str, Horario]): Diccionario con los días y horarios requeridos.
        """
        self.dias_requeridos = dias_requeridos

    def is_satisfied_by(self, sucursal: Sucursal) -> bool:
        dias_actuales = {h.fecha: h for h in sucursal.dias_atencion}
        for dia, horario in self.dias_requeridos.items():
            if dia not in dias_actuales or not dias_actuales[dia].esta_dentro(horario):
                return False
        return True


class DisposicionFisicaSpecification(SucursalSpecification):
    def __init__(self, disposicion_requerida: Dict[str, int]):
        """
        Verifica que la disposición física de la sucursal cumpla con los requisitos mínimos.

        Args:
            disposicion_requerida (Dict[str, int]): Diccionario con los roles y capacidades mínimas requeridas.
        """
        self.disposicion_requerida = disposicion_requerida

    def is_satisfied_by(self, sucursal: Sucursal) -> bool:
        for rol, capacidad_requerida in self.disposicion_requerida.items():
            capacidad_actual = sucursal.disposicion_fisica.get(rol, 0)
            if capacidad_actual < capacidad_requerida:
                return False
        return True
