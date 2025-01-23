import datetime

class Dia:
    def __init__(self, fecha, festivo=False):
        """
        Inicializa un objeto Dia.

        Args:
            fecha (datetime.date): Fecha del día.
            festivo (bool, opcional): Indica si el día es festivo. Por defecto, False.
        """

        self.fecha = datetime.date(fecha)
        self.festivo = bool(festivo)