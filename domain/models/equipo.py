class Equipo:
    def __init__(self, nombre, sucursal, colaboradores=[]):
        """
        Inicializa un objeto Equipo.

        Args:
            nombre (str): Nombre del equipo.
            sucursal (Sucursal): Sucursal a la que pertenece el equipo.
            colaboradores (list, opcional): Lista de colaboradores que pertenecen al equipo.
        """

        self.nombre = nombre
        self.sucursal = sucursal
        self.colaboradores = colaboradores

    def agregar_colaborador(self, colaborador):
        """
        Agrega un colaborador al equipo.

        Args:
            colaborador (Colaborador): Objeto de la clase Colaborador.
        """
        self.colaboradores.append(colaborador)

    def quitar_colaborador(self, colaborador):
        """
        Quita un colaborador del equipo.

        Args:
            colaborador (Colaborador): Objeto de la clase Colaborador.
        """
        self.colaboradores.remove(colaborador)

    def obtener_colaboradores(self):
        """
        Devuelve una lista de los colaboradores del equipo.

        Returns:
            list: Lista de objetos Colaborador.
        """
        return self.colaboradores