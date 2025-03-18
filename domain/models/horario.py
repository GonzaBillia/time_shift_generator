from datetime import date, time, timedelta
from typing import List, Tuple, Optional

class Horario:
    def __init__(
        self,
        sucursal_id: int,
        colaborador_id: Optional[int],  # Puede ser None si es un horario general de sucursal
        rol_colaborador_id: Optional[int],
        dia_id: int,  # Nuevo campo para reflejar la base de datos
        fecha: Optional[date],
        bloques: List[Tuple[time, time]],
        horario_corrido: bool
    ):
        """
        Inicializa un objeto Horario.

        Args:
            sucursal_id (int): ID de la sucursal donde aplica el horario.
            colaborador_id (Optional[int]): ID del colaborador (None si es un horario general de sucursal).
            dia_id (int): Día de la semana (0=Lunes, 6=Domingo), según la BD.
            fecha (date): Fecha del horario.
            bloques (List[Tuple[time, time]]): Lista de bloques de tiempo (inicio, fin).
            horario_corrido (bool): Define si es horario corrido o no.
        """
        self.sucursal_id = sucursal_id
        self.colaborador_id = colaborador_id
        self.rol_colaborador_id = rol_colaborador_id
        self.dia_id = dia_id  # Se alinea con la BD
        self.fecha = fecha
        self.horario_corrido = horario_corrido

        if not bloques:
            raise ValueError("Debes proporcionar al menos un bloque de tiempo.")

        # Ordenar y validar los bloques
        self.bloques = sorted(bloques, key=lambda b: b[0])  
        self._validar_bloques()

    def _validar_bloques(self):
        """Valida que los bloques de horario sean correctos (sin superposiciones y orden lógico)."""
        for i, (inicio, fin) in enumerate(self.bloques):
            if fin <= inicio:
                raise ValueError(f"El bloque {i + 1} tiene una hora de fin anterior o igual a la hora de inicio.")
            if i > 0:  
                _, fin_anterior = self.bloques[i - 1]
                if inicio < fin_anterior:
                    raise ValueError(f"El bloque {i + 1} se superpone con el bloque anterior.")

    def duracion(self) -> int:
        """
        Calcula la duración total del horario en minutos.
        Ahora maneja el caso de horarios que cruzan medianoche.
        """
        duracion_total = 0
        for inicio, fin in self.bloques:
            inicio_min = inicio.hour * 60 + inicio.minute
            fin_min = fin.hour * 60 + fin.minute

            if fin_min < inicio_min:  # Caso en el que el horario cruza medianoche
                duracion = (24 * 60 - inicio_min) + fin_min
            else:
                duracion = fin_min - inicio_min

            duracion_total += duracion

        return duracion_total

    def se_superpone(self, otro_horario: 'Horario') -> bool:
        """Verifica si este horario se superpone con otro horario en la misma sucursal y fecha."""
        if self.fecha != otro_horario.fecha or self.sucursal_id != otro_horario.sucursal_id:
            return False  

        return any(
            inicio1 < fin2 and inicio2 < fin1  # Se superponen si hay intersección
            for inicio1, fin1 in self.bloques
            for inicio2, fin2 in otro_horario.bloques
        )

    def esta_dentro(self, otro: 'Horario') -> bool:
        """Verifica si todos los bloques de este horario están completamente contenidos dentro del otro horario."""
        if self.fecha != otro.fecha or self.sucursal_id != otro.sucursal_id:
            return False  

        return all(
            any(inicio2 <= inicio1 and fin1 <= fin2 for inicio2, fin2 in otro.bloques)
            for inicio1, fin1 in self.bloques
        )

    def agregar_bloque(self, inicio: time, fin: time):
        """
        Agrega un nuevo bloque de tiempo al horario después de validar que no haya superposición.
        También valida que el bloque no cruce al siguiente día.
        """
        if fin < inicio:  # No permitir bloques que pasen de un día al siguiente
            raise ValueError("El bloque no puede cruzar al siguiente día.")

        nuevo_bloque = (inicio, fin)

        for bloque_existente in self.bloques:
            if nuevo_bloque[0] < bloque_existente[1] and nuevo_bloque[1] > bloque_existente[0]:
                raise ValueError("El nuevo bloque se superpone con un bloque existente.")

        self.bloques.append(nuevo_bloque)
        self.bloques.sort(key=lambda b: b[0])  # Ordenar después de agregar el bloque

    def eliminar_bloque(self, inicio: time, fin: time):
        """
        Elimina un bloque de tiempo si existe en la lista.

        Args:
            inicio (time): Hora de inicio del bloque a eliminar.
            fin (time): Hora de fin del bloque a eliminar.

        Returns:
            bool: True si el bloque fue eliminado, False si no se encontró.
        """
        try:
            self.bloques.remove((inicio, fin))
            return True
        except ValueError:
            return False

    def to_dict(self):
        """Convierte el objeto Horario en un diccionario."""
        return {
            "sucursal_id": self.sucursal_id,
            "colaborador_id": self.colaborador_id,
            "dia_id": self.dia_id,
            "fecha": self.fecha.isoformat(),
            "horario_corrido": self.horario_corrido,
            "bloques": [(inicio.strftime("%H:%M"), fin.strftime("%H:%M")) for inicio, fin in self.bloques]
        }

    def __str__(self):
        """Representación en cadena del objeto Horario."""
        return f"Horario(sucursal={self.sucursal_id}, colaborador={self.colaborador_id}, dia_id={self.dia_id}, fecha={self.fecha}, bloques={self.bloques}, horario_corrido={self.horario_corrido})"
