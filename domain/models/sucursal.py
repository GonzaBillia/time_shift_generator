from typing import List, Dict
from datetime import date
from domain.models.horario import Horario
from domain.models.formato import Formato
from domain.models.rol import Rol

class Sucursal:
    def __init__(
        self,
        id: int,
        nombre: str,
        empresa_id: int,
        direccion: str,
        telefono: str,
        formato: Formato,
        disposicion_fisica: Dict[Rol, int],  # Ahora usa `Rol` en lugar de strings
        horario_atencion: List[Horario],  # Puede haber varios horarios (lunes a viernes, sábados, etc.)
        dias_atencion: List[int]  # Lista de `dia_id` (0 = Lunes, 6 = Domingo)
    ):
        """
        Inicializa una sucursal.

        Args:
            id (int): Identificador único de la sucursal.
            nombre (str): Nombre de la sucursal.
            empresa_id (int): ID de la empresa a la que pertenece la sucursal.
            direccion (str): Dirección de la sucursal.
            telefono (str): Teléfono de contacto.
            formato (Formato): Formato de la sucursal (define los roles necesarios).
            disposicion_fisica (Dict[Rol, int]): Diccionario que representa la disposición física de la sucursal.
                Las claves son objetos `Rol` y los valores son enteros indicando la cantidad de puestos.
            horario_atencion (List[Horario]): Lista de horarios de atención (uno por cada día de la semana).
            dias_atencion (List[int]): Lista de `dia_id` en los que la sucursal está abierta (0=Lunes, 6=Domingo).
        """
        self.id = id
        self.nombre = nombre
        self.empresa_id = empresa_id
        self.direccion = direccion
        self.telefono = telefono
        self.formato = formato
        self.disposicion_fisica = self.validar_disposicion(disposicion_fisica)
        self.horario_atencion = horario_atencion  # Lista de Horarios
        self.dias_atencion = dias_atencion  # Lista de `dia_id`
        self.espacios_ocupados = {rol: 0 for rol in formato.roles}  # Control de espacios ocupados por rol

    def validar_disposicion(self, disposicion_fisica: Dict[Rol, int]) -> Dict[Rol, int]:
        """
        Valida que la disposición física incluya únicamente roles definidos en el formato.

        Args:
            disposicion_fisica (Dict[Rol, int]): Diccionario de disposición física.

        Returns:
            Dict[Rol, int]: Diccionario validado.

        Raises:
            ValueError: Si hay roles en la disposición física que no pertenecen al formato.
        """
        for rol in disposicion_fisica:
            if rol not in self.formato.roles:
                raise ValueError(f"El rol '{rol.nombre}' no pertenece al formato '{self.formato.nombre}'.")
        return disposicion_fisica

    def esta_abierta(self, dia_id: int) -> bool:
        """
        Verifica si la sucursal está abierta en un día específico.

        Args:
            dia_id (int): Día de la semana (0=Lunes, 6=Domingo).

        Returns:
            bool: True si la sucursal está abierta, False en caso contrario.
        """
        return dia_id in self.dias_atencion

    def obtener_disposicion_por_rol(self, rol: Rol) -> int:
        """
        Obtiene la cantidad máxima de puestos para un rol dado.

        Args:
            rol (Rol): Objeto Rol.

        Returns:
            int: Cantidad máxima de puestos para el rol.

        Raises:
            ValueError: Si el rol no pertenece al formato.
        """
        if rol not in self.formato.roles:
            raise ValueError(f"El rol '{rol.nombre}' no pertenece al formato '{self.formato.nombre}'.")
        return self.disposicion_fisica.get(rol, 0)

    def puede_asignar_rol(self, rol: Rol) -> bool:
        """
        Verifica si un rol puede asignarse, basándose en la disposición física.

        Args:
            rol (Rol): Objeto Rol.

        Returns:
            bool: True si el rol puede asignarse, False de lo contrario.
        """
        if rol not in self.formato.roles:
            raise ValueError(f"El rol '{rol.nombre}' no pertenece al formato '{self.formato.nombre}'.")
        return self.espacios_ocupados[rol] < self.disposicion_fisica.get(rol, 0)

    def asignar_rol(self, rol: Rol) -> bool:
        """
        Asigna un rol si hay espacio disponible.

        Args:
            rol (Rol): Objeto Rol.

        Returns:
            bool: True si se pudo asignar el rol, False si no hay espacio disponible.
        """
        if self.puede_asignar_rol(rol):
            self.espacios_ocupados[rol] += 1
            return True
        return False

    def liberar_rol(self, rol: Rol) -> None:
        """
        Libera un puesto ocupado por un rol.

        Args:
            rol (Rol): Objeto Rol.

        Raises:
            ValueError: Si no hay puestos ocupados para el rol.
        """
        if rol not in self.formato.roles:
            raise ValueError(f"El rol '{rol.nombre}' no pertenece al formato '{self.formato.nombre}'.")
        if self.espacios_ocupados[rol] > 0:
            self.espacios_ocupados[rol] -= 1
        else:
            raise ValueError(f"No hay puestos ocupados para el rol '{rol.nombre}' para liberar.")

    def listar_roles(self) -> List[str]:
        """
        Lista todos los roles disponibles en el formato.

        Returns:
            List[str]: Lista de nombres de roles en el formato.
        """
        return [rol.nombre for rol in self.formato.roles]

    def __str__(self):
        """
        Representación en cadena de la sucursal.

        Returns:
            str: Información resumida de la sucursal.
        """
        return f"Sucursal(id={self.id}, nombre={self.nombre}, formato={self.formato.nombre}, empresa_id={self.empresa_id})"
