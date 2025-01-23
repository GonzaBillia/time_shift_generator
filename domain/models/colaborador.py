class Colaborador:
    def __init__(self, nombre, legajo, email, telefono, dni, roles, equipo, horario_preferido, dias_preferidos, horas_semanales, hs_extra, vacaciones):
        """
        Inicializa un objeto Colaborador.

        Args:
            nombre (str): Nombre del colaborador.
            legajo (int): Número de legajo del colaborador.
            email (str): Correo electrónico del colaborador.
            telefono (str): Número de teléfono del colaborador.
            dni (str): Documento Nacional de Identidad del colaborador.
            roles (list): Lista de roles que el colaborador puede desempeñar.
            equipo (Equipo): Equipo de trabajo al que pertenece el colaborador.
            horario_preferido (Horario): Horario preferido del colaborador.
            dias_preferidos (list): Lista de días preferidos para trabajar.
            horas_semanales (int): Cantidad de horas semanales a trabajar.
            hs_extra (dict): Diccionario con las horas extras a devolver y a cobrar.
            vacaciones (list): Lista de períodos de vacaciones.
        """

        self.nombre = nombre
        self.legajo = legajo
        self.email = email
        self.telefono = telefono
        self.dni = dni
        self.roles = roles
        self.equipo = equipo
        self.horario_preferido = horario_preferido
        self.dias_preferidos = dias_preferidos
        self.horas_semanales = horas_semanales
        self.hs_extra = hs_extra
        self.vacaciones = vacaciones