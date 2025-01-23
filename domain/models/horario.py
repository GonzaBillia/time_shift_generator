import datetime

class Horario:
    def __init__(self, hora_inicio, hora_fin):
        """
        Inicializa un objeto Horario.

        Args:
            hora_inicio (datetime.time): Hora de inicio del horario.
            hora_fin (datetime.time): Hora de fin del horario.
        """

        if hora_fin <= hora_inicio:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")

        self.hora_inicio = datetime.time(hora_inicio)
        self.hora_fin = datetime.time(hora_fin)

    def duracion(self):
        """
        Calcula la duración del horario en minutos.

        Returns:
            int: Duración del horario en minutos.
        """

        tiempo_delta = datetime.timedelta(hours=self.hora_fin.hour, minutes=self.hora_fin.minute) - \
                       datetime.timedelta(hours=self.hora_inicio.hour, minutes=self.hora_inicio.minute)
        return tiempo_delta.total_seconds() // 60

    def se_superpone(self, otro_horario):
        """
        Verifica si este horario se superpone con otro horario.

        Args:
            otro_horario (Horario): Otro objeto Horario.

        Returns:
            bool: True si los horarios se superponen, False en caso contrario.
        """

        return (self.hora_inicio <= otro_horario.hora_fin) and (self.hora_fin >= otro_horario.hora_inicio)