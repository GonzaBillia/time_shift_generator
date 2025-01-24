from typing import List

class Formato:
    def __init__(self, nombre: str, roles: List[str]):
        """
        Inicializa un formato.

        Args:
            nombre (str): Nombre del formato.
            roles (List[str]): Lista de roles asociados al formato.
        """
        self.nombre = nombre
        self.roles = roles

class FormatoTradicional(Formato):
    def __init__(self):
        """
        Inicializa el formato tradicional con los roles correspondientes.
        """
        super().__init__(
            nombre="tradicional",
            roles=["atencion", "cajero", "anfitrion", "pedidos", "carga_stock"]
        )

class FormatoGondola(FormatoTradicional):
    def __init__(self):
        """
        Inicializa el formato góndola, heredando del tradicional y añadiendo nuevos roles.
        """
        super().__init__()
        self.nombre = "gondola"
        self.roles.extend(["atencion_salon", "referentes"])

class FormatoMarket(FormatoGondola):
    def __init__(self):
        """
        Inicializa el formato market, heredando del góndola y añadiendo nuevos roles.
        """
        super().__init__()
        self.nombre = "market"
        self.roles.extend(["repositor", "atencion_fiambreria"])
