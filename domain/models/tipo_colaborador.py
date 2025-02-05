class TipoEmpleado:
    def __init__(self, id, tipo, horas_por_dia_max, horas_semanales):
        self.id = id  # Referencia al ID en la base de datos
        self.tipo = tipo
        self.horas_por_dia_max = horas_por_dia_max
        self.horas_semanales = horas_semanales
