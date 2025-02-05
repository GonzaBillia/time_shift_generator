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


class FormatoTradicional(Formato):
    def __init__(self):
        """
        Inicializa el formato tradicional con los roles correspondientes.
        """
        super().__init__(
            nombre="tradicional",
            roles=[
                Rol("atencion", principal=True),
                Rol("cajero"),
                Rol("anfitrion"),
                Rol("pedidos"),
                Rol("carga_stock"),
            ]
        )


class FormatoGondola(Formato):
    def __init__(self):
        """
        Inicializa el formato góndola, heredando del tradicional y añadiendo nuevos roles.
        """
        base_roles = FormatoTradicional().roles
        super().__init__(
            nombre="gondola",
            roles=base_roles + [
                Rol("atencion_salon"),
                Rol("referentes"),
            ]
        )


class FormatoMarket(Formato):
    def __init__(self):
        """
        Inicializa el formato market, heredando del góndola y añadiendo nuevos roles.
        """
        base_roles = FormatoGondola().roles
        super().__init__(
            nombre="market",
            roles=base_roles + [
                Rol("repositor"),
                Rol("atencion_fiambreria"),
            ]
        )
