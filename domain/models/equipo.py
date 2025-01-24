from __future__ import annotations
from typing import List
from domain.models.colaborador import Colaborador
from domain.models.sucursal import Sucursal

class Equipo:
    def __init__(self, id: int, nombre: str, sucursal: Sucursal, colaboradores: List[Colaborador] = None):
        """
        Inicializa un objeto Equipo.

        Args:
            nombre (str): Nombre del equipo.
            sucursal (Sucursal): Sucursal a la que pertenece el equipo.
            colaboradores (List[Colaborador], opcional): Lista de colaboradores que pertenecen al equipo.
        """
        self.id = id
        self.nombre = nombre
        self.sucursal = sucursal
        self.colaboradores = colaboradores if colaboradores is not None else []

    def agregar_colaborador(self, colaborador: Colaborador) -> bool:
        """
        Agrega un colaborador al equipo si no excede la capacidad definida por la sucursal.

        Args:
            colaborador (Colaborador): Objeto de la clase Colaborador.

        Returns:
            bool: True si el colaborador fue agregado exitosamente, False de lo contrario.
        """
        try:
            self.colaboradores.append(colaborador)
            return True
        except ValueError as e:
            print(f"Error al agregar colaborador: {e}")
            return False

    def quitar_colaborador(self, colaborador: Colaborador) -> bool:
        """
        Quita un colaborador del equipo.

        Args:
            colaborador (Colaborador): Objeto de la clase Colaborador.

        Returns:
            bool: True si el colaborador fue quitado exitosamente, False de lo contrario.
        """
        if colaborador in self.colaboradores:
            self.colaboradores.remove(colaborador)
            return True
        else:
            print("El colaborador no pertenece al equipo.")
            return False

    def obtener_colaboradores(self) -> List[Colaborador]:
        """
        Devuelve una lista de los colaboradores del equipo.

        Returns:
            List[Colaborador]: Lista de objetos Colaborador.
        """
        return self.colaboradores