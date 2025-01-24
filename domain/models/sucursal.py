# domain/models/sucursal.py

from typing import List, Dict
from datetime import date
from domain.models.horario import Horario
from domain.models.formato import Formato


class Sucursal:
    def __init__(self, nombre: str, formato: Formato, disposicion_fisica: Dict[str, int], horario_atencion: Horario, dias_atencion: List[Horario] = None):
        """
        Inicializa una sucursal.

        Args:
            nombre (str): Nombre de la sucursal.
            formato (Formato): Formato de la sucursal (define los roles necesarios).
            disposicion_fisica (Dict[str, int]): Diccionario que representa la disposición física de la sucursal.
                Las claves son los nombres de los roles y los valores son enteros que indican la cantidad máxima de puestos.
            horario_atencion (Horario): Horario de atención general de la sucursal.
            dias_atencion (List[Horario], opcional): Lista de objetos Horario en los que la sucursal está abierta.
        """
        self.nombre = nombre
        self.formato = formato
        self.disposicion_fisica = self.validar_disposicion(disposicion_fisica)
        self.horario_atencion = horario_atencion
        self.dias_atencion = dias_atencion if dias_atencion is not None else []
        self.espacios_ocupados = {rol: 0 for rol in formato.roles}  # Control de espacios ocupados por rol

    def validar_disposicion(self, disposicion_fisica: Dict[str, int]) -> Dict[str, int]:
        """
        Valida que la disposición física incluya únicamente roles definidos en el formato.

        Args:
            disposicion_fisica (Dict[str, int]): Diccionario de disposición física.

        Returns:
            Dict[str, int]: Diccionario validado.

        Raises:
            ValueError: Si hay roles en la disposición física que no pertenecen al formato.
        """
        for rol in disposicion_fisica:
            if rol not in self.formato.roles:
                raise ValueError(f"El rol '{rol}' no pertenece al formato '{self.formato.nombre}'.")
        return disposicion_fisica

    def agregar_dia(self, horario: Horario) -> bool:
        """
        Agrega un día al calendario de la sucursal.

        Args:
            horario (Horario): Objeto de la clase Horario.

        Returns:
            bool: True si el día fue agregado exitosamente, False de lo contrario.
        """
        if any(h.fecha == horario.fecha for h in self.dias_atencion):
            print("El día ya está en la lista de días de atención.")
            return False
        self.dias_atencion.append(horario)
        return True

    def obtener_disposicion_por_rol(self, rol: str) -> int:
        """
        Obtiene la cantidad máxima de puestos para un rol dado.

        Args:
            rol (str): Nombre del rol.

        Returns:
            int: Cantidad máxima de puestos para el rol.

        Raises:
            ValueError: Si el rol no pertenece al formato.
        """
        if rol not in self.formato.roles:
            raise ValueError(f"El rol '{rol}' no pertenece al formato '{self.formato.nombre}'.")
        return self.disposicion_fisica.get(rol, 0)

    def puede_asignar_rol(self, rol: str) -> bool:
        """
        Verifica si un rol puede asignarse, basándose en la disposición física.

        Args:
            rol (str): Nombre del rol a verificar.

        Returns:
            bool: True si el rol puede asignarse, False de lo contrario.

        Raises:
            ValueError: Si el rol no pertenece al formato.
        """
        if rol not in self.formato.roles:
            raise ValueError(f"El rol '{rol}' no pertenece al formato '{self.formato.nombre}'.")
        return self.espacios_ocupados[rol] < self.disposicion_fisica.get(rol, 0)

    def asignar_rol(self, rol: str) -> bool:
        """
        Asigna un rol si hay espacio disponible.

        Args:
            rol (str): Nombre del rol a asignar.

        Returns:
            bool: True si se pudo asignar el rol, False si no hay espacio disponible.
        """
        if self.puede_asignar_rol(rol):
            self.espacios_ocupados[rol] += 1
            return True
        return False

    def liberar_rol(self, rol: str) -> None:
        """
        Libera un puesto ocupado por un rol.

        Args:
            rol (str): Nombre del rol a liberar.

        Raises:
            ValueError: Si no hay puestos ocupados para el rol.
        """
        if rol not in self.formato.roles:
            raise ValueError(f"El rol '{rol}' no pertenece al formato '{self.formato.nombre}'.")
        if self.espacios_ocupados[rol] > 0:
            self.espacios_ocupados[rol] -= 1
        else:
            raise ValueError(f"No hay puestos ocupados para el rol '{rol}' para liberar.")

    def verificar_disponibilidad(self) -> Dict[str, int]:
        """
        Devuelve un diccionario con la disponibilidad de puestos por rol.

        Returns:
            Dict[str, int]: Disponibilidad por rol.
        """
        return {rol: self.disposicion_fisica.get(rol, 0) - self.espacios_ocupados[rol] for rol in self.formato.roles}

    def listar_roles(self) -> List[str]:
        """
        Lista todos los roles disponibles en el formato.

        Returns:
            List[str]: Lista de roles en el formato.
        """
        return self.formato.roles
