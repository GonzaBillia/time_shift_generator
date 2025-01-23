from abc import ABC, abstractmethod

class Specification(ABC):
    """
    Clase base para representar una regla o criterio.
    Debe implementar el método is_satisfied_by.
    """
    @abstractmethod
    def is_satisfied_by(self, candidate) -> bool:
        """
        Este método se encarga de evaluar si 'candidate' cumple
        con la especificación o criterio definido.
        """
        raise NotImplementedError("Subclasses must override is_satisfied_by method.")
