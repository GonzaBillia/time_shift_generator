class Sucursal:
    def __init__(self, nombre, formato, disposicion_fisica, horario_atencion, dias_atencion):
        """
        Inicializa una sucursal.

        Args:
            nombre (str): Nombre de la sucursal.
            formato (Formato): Formato de la sucursal (define los roles necesarios).
            disposicion_fisica (dict): Diccionario que representa la disposición física de la sucursal.
                Las claves son los nombres de los roles y los valores son enteros que indican la cantidad máxima de puestos.
            horario_atencion (Horario): Horario de atención general de la sucursal.
            dias_atencion (list): Lista de objetos Dia en los que la sucursal está abierta.
        """

        self.nombre = nombre
        self.formato = formato
        self.disposicion_fisica = disposicion_fisica
        self.horario_atencion = horario_atencion
        self.dias_atencion = dias_atencion

    def agregar_dia(self, dia):
        """
        Agrega un día al calendario de la sucursal.

        Args:
            dia (Dia): Objeto de la clase Dia.
        """
        self.calendario.append(dia)

    def obtener_disposicion_por_rol(self, rol):
        """
        Obtiene la cantidad máxima de puestos para un rol dado.

        Args:
            rol (str): Nombre del rol.

        Returns:
            int: Cantidad máxima de puestos para el rol.
        """

        return self.disposicion_fisica.get(rol, 0)