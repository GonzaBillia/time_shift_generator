from typing import List
from .rol import Rol  # Ahora usamos objetos `Rol`, no strings

class Formato:
    def __init__(self, nombre: str, roles: List[Rol]):
        """
        Inicializa un formato de sucursal.

        Args:
            nombre (str): Nombre del formato.
            roles (List[Rol]): Lista de roles asociados al formato.
        """
        self.nombre = nombre
        self.roles = list(roles)  # Copia la lista para evitar mutaciones

    def __str__(self):
        """Representación en cadena del objeto Formato."""
        return f"Formato(nombre={self.nombre}, roles={[rol.nombre for rol in self.roles]})"
