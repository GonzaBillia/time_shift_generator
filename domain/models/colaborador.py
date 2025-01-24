# domain/models/colaborador.py

from __future__ import annotations
from typing import List, Dict
from datetime import date
from .horario import Horario
from .tipo_colaborador import TipoEmpleado

# Definición de constantes para los tipos de empleado
# Crear los objetos de tipo empleado
TIEMPO_COMPLETO = TipoEmpleado(
    tipo="tiempo completo",
    horas_por_dia_max=8,
    horas_semanales=45
)

TIEMPO_PARCIAL = TipoEmpleado(
    tipo="tiempo parcial",
    horas_por_dia_max=4,
    horas_semanales=30
)

HORARIO_ESPECIAL = TipoEmpleado(
    tipo="horario especial",
    horas_por_dia_max=11,
    horas_semanales=22
)


class Colaborador:
    def __init__(
        self,
        nombre: str,
        legajo: int,
        email: str,
        telefono: str,
        dni: str,
        roles: List[str],
        horario_preferido: Horario,
        dias_preferidos: List[int],  # Ejemplo: 0=Monday, 6=Sunday
        horas_semanales: int,  # En horas
        hs_extra: Dict[str, int],  # Ejemplo: {'devolver': int, 'cobrar': int}
        vacaciones: List[date],
        horario_asignado: List[Horario],
        tipo_empleado: str,  # 'tiempo completo', 'tiempo parcial', 'horario especial'
        horas_diarias_maximas: int,  # En horas
        horario_corrido: bool = False,
    ):
        """
        Inicializa un objeto Colaborador.

        Args:
            nombre (str): Nombre del colaborador.
            legajo (int): Número de legajo del colaborador.
            email (str): Correo electrónico del colaborador.
            telefono (str): Número de teléfono del colaborador.
            dni (str): Documento Nacional de Identidad del colaborador.
            roles (List[str]): Lista de roles que el colaborador puede desempeñar.
            horario_preferido (Horario): Horario preferido del colaborador.
            dias_preferidos (List[int]): Lista de días preferidos para trabajar (0=Monday, 6=Sunday).
            horas_semanales (int): Cantidad de horas semanales a trabajar.
            hs_extra (Dict[str, int]): Diccionario con las horas extras a devolver y a cobrar.
            vacaciones (List[date]): Lista de fechas de vacaciones.
            horario_asignado (List[Horario]): Lista de horarios asignados en una semana.
            tipo_empleado (str): Tipo de empleado ('tiempo completo', 'tiempo parcial', 'horario especial').
            horario_corrido (bool, optional): Define si es corrido o cortado. Por defecto es False.
            horas_diarias_maximas (int, optional): Define el máximo de horas que puede trabajar. Por defecto es 8.
        
        Raises:
            ValueError: Si 'tipo_empleado' no es válido.
        """
        self.nombre = nombre
        self.legajo = legajo
        self.email = email
        self.telefono = telefono
        self.dni = dni
        self.roles = roles
        self.horario_preferido = horario_preferido
        self.dias_preferidos = dias_preferidos
        self.horas_semanales = horas_semanales  # En horas
        self.hs_extra = hs_extra
        self.vacaciones = vacaciones
        self.horario_asignado = horario_asignado  # Lista de objetos Horario
        self.horas_diarias_maximas = horas_diarias_maximas  # En horas
        self.horario_corrido = horario_corrido

        # Validación del tipo de empleado
        if tipo_empleado not in {TIEMPO_COMPLETO, TIEMPO_PARCIAL, HORARIO_ESPECIAL}:
            raise ValueError(f"tipo_empleado debe ser uno de: '{TIEMPO_COMPLETO}', '{TIEMPO_PARCIAL}', '{HORARIO_ESPECIAL}'.")
        self.tipo_empleado = tipo_empleado  # Asignación después de la validación

    def calcular_horas_totales_semanales(self) -> float:
        """
        Calcula el total de horas trabajadas por el colaborador en una semana.

        Returns:
            float: Total de horas trabajadas en la semana.
        """
        if not self.horario_asignado:
            return 0.0

        # Sumar la duración de todos los horarios asignados en minutos
        minutos_totales = sum(horario.duracion() for horario in self.horario_asignado)
        horas_totales = minutos_totales / 60  # Convertir a horas

        return horas_totales

    def verificar_horas_semanales(self) -> bool:
        """
        Verifica si el total de horas semanales trabajadas no excede las horas semanales asignadas.

        Returns:
            bool: True si no excede, False en caso contrario.
        """
        horas_totales = self.calcular_horas_totales_semanales()
        return horas_totales <= self.horas_semanales

    def verificar_horas_diarias(self) -> bool:
        """
        Verifica si en cada día, las horas trabajadas no exceden las horas diarias máximas.

        Returns:
            bool: True si en todos los días se respetan las horas máximas, False en caso contrario.
        """
        for horario in self.horario_asignado:
            horas_dia = horario.duracion() / 60  # Convertir a horas
            if horas_dia > self.horas_diarias_maximas:
                return False
        return True

    def agregar_horario(self, nuevo_horario: Horario):
        """
        Agrega un nuevo horario asignado al colaborador después de validar que no excede las horas diarias y semanales.

        Args:
            nuevo_horario (Horario): Nuevo objeto Horario a agregar.

        Raises:
            ValueError: Si agregar el nuevo horario excede las horas semanales o diarias.
        """
        # Verificar superposiciones con horarios existentes
        for horario_existente in self.horario_asignado:
            if horario_existente.se_superpone(nuevo_horario):
                raise ValueError("El nuevo horario se superpone con un horario existente.")

        # Calcular nuevas horas semanales si se agrega el nuevo horario
        horas_nuevas = nuevo_horario.duracion() / 60
        horas_totales = self.calcular_horas_totales_semanales() + horas_nuevas

        if horas_totales > self.horas_semanales:
            raise ValueError("Agregar este horario excede las horas semanales asignadas.")

        # Verificar horas diarias
        horas_dia = nuevo_horario.duracion() / 60
        if horas_dia > self.horas_diarias_maximas:
            raise ValueError("Agregar este horario excede las horas diarias máximas permitidas.")

        # Si todo está bien, agregar el horario
        self.horario_asignado.append(nuevo_horario)

    def __str__(self):
        """
        Representación en cadena del objeto Colaborador.

        Returns:
            str: Información resumida del colaborador.
        """
        return f"Colaborador(nombre={self.nombre}, legajo={self.legajo}, tipo_empleado={self.tipo_empleado})"
