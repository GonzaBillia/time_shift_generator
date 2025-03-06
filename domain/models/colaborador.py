from __future__ import annotations
from typing import List, Dict, Tuple
from datetime import date
from .horario import Horario
from .tipo_colaborador import TipoEmpleado
from .rol import Rol

class Colaborador:
    def __init__(
        self,
        id: int,
        nombre: str,
        legajo: int,
        email: str,
        telefono: str,
        dni: str,
        sucursales: List[int],  # Lista de IDs de sucursales donde trabaja
        roles: List[Rol],  # Lista de roles asignados
        horario_preferido: List[Tuple[int, Horario]],
        dias_preferidos: List[int],  # 0=Lunes, 6=Domingo
        tipo_empleado: TipoEmpleado,
        horario_asignado: List[Tuple[int, Horario]],  # (sucursal_id, Horario)
        hs_extra: Dict[str, int],  # {'devolver': int, 'cobrar': int}
        vacaciones: List[date],
        horario_corrido: bool = False,
    ):
        """
        Inicializa un objeto Colaborador.

        Args:
            id (int): Identificador único del colaborador.
            nombre (str): Nombre del colaborador.
            legajo (int): Número de legajo del colaborador.
            email (str): Correo electrónico.
            telefono (str): Teléfono del colaborador.
            dni (str): Documento de identidad.
            sucursales (List[int]): Lista de IDs de sucursales en las que trabaja.
            roles (List[Rol]): Lista de roles asignados.
            horario_preferido (Horario): Horario preferido del colaborador.
            dias_preferidos (List[int]): Días preferidos para trabajar.
            tipo_empleado (TipoEmpleado): Tipo de contrato del colaborador.
            horario_asignado (List[Tuple[int, Horario]]): Lista de horarios asignados con sucursales.
            hs_extra (Dict[str, int]): Horas extras a cobrar o devolver.
            vacaciones (List[date]): Lista de fechas de vacaciones.
            horario_corrido (bool): Indica si el colaborador tiene horario continuo o partido.
        """
        self.id = id
        self.nombre = nombre
        self.legajo = legajo
        self.email = email
        self.telefono = telefono
        self.dni = dni
        self.sucursales = sucursales
        self.roles = roles
        self.horario_preferido = horario_preferido
        self.dias_preferidos = dias_preferidos
        self.tipo_empleado = tipo_empleado
        self.horario_asignado = horario_asignado
        self.hs_extra = hs_extra
        self.vacaciones = vacaciones
        self.horario_corrido = horario_corrido

    # ✅ MÉTODOS PARA GESTIÓN DE HORARIOS
    def agregar_horario(self, sucursal_id: int, nuevo_horario: Horario):
        """Asigna un horario al colaborador en una sucursal específica."""
        if sucursal_id not in self.sucursales:
            raise ValueError(f"El colaborador no trabaja en la sucursal {sucursal_id}.")

        # Verificar superposición de horarios
        for sucursal, horario_existente in self.horario_asignado:
            if sucursal == sucursal_id and horario_existente.se_superpone(nuevo_horario):
                raise ValueError("El nuevo horario se superpone con un horario existente.")

        self.horario_asignado.append((sucursal_id, nuevo_horario))

    def calcular_horas_totales_semanales(self) -> float:
        """Calcula el total de horas trabajadas en la semana."""
        if not self.horario_asignado:
            return 0.0
        minutos_totales = sum(horario.duracion() for _, horario in self.horario_asignado)
        return minutos_totales / 60  # Convertir a horas

    def verificar_horas_semanales(self) -> bool:
        """Verifica si las horas trabajadas no exceden el límite del contrato."""
        return self.calcular_horas_totales_semanales() <= self.tipo_empleado.horas_semanales

    def verificar_horas_diarias(self) -> bool:
        """Verifica si las horas diarias trabajadas no exceden el límite permitido."""
        horas_por_dia = {}
        for _, horario in self.horario_asignado:
            dia = horario.dia  # Suponiendo que Horario tiene un atributo `dia`
            horas_dia = horas_por_dia.get(dia, 0) + horario.duracion() / 60
            if horas_dia > self.tipo_empleado.horas_por_dia_max:
                return False
            horas_por_dia[dia] = horas_dia
        return True

    # ✅ MÉTODOS PARA GESTIÓN DE VACACIONES Y HORAS EXTRA
    def agregar_vacacion(self, fecha: date):
        """Agrega una fecha de vacaciones al colaborador."""
        if fecha in self.vacaciones:
            raise ValueError("El colaborador ya tiene esa fecha registrada como vacaciones.")
        self.vacaciones.append(fecha)

    def agregar_horas_extra(self, tipo: str, cantidad: int):
        """Agrega horas extras al colaborador."""
        if tipo not in {'devolver', 'cobrar'}:
            raise ValueError("El tipo debe ser 'devolver' o 'cobrar'.")
        self.hs_extra[tipo] = self.hs_extra.get(tipo, 0) + cantidad

    # ✅ REPRESENTACIÓN EN TEXTO
    def __str__(self):
        """Representación en cadena del objeto Colaborador."""
        return f"Colaborador(id={self.id}, nombre={self.nombre}, tipo_empleado={self.tipo_empleado.tipo}, horario_corrido={self.horario_corrido})"
