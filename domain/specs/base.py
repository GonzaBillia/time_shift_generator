class Specification:
    """
    Clase base para representar una regla o criterio.
    Debe implementar el método is_satisfied_by.
    """
    def is_satisfied_by(self, candidate) -> bool:
        """
        Este método se encarga de evaluar si 'candidate' cumple
        con la especificación o criterio definido.
        """
        raise NotImplementedError("Subclasses must override is_satisfied_by method.")


class AndSpecification(Specification):
    """
    Permite combinar dos especificaciones con un operador lógico AND.
    """
    def __init__(self, spec1: Specification, spec2: Specification):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, candidate) -> bool:
        return self.spec1.is_satisfied_by(candidate) and self.spec2.is_satisfied_by(candidate)


class OrSpecification(Specification):
    """
    Permite combinar dos especificaciones con un operador lógico OR.
    """
    def __init__(self, spec1: Specification, spec2: Specification):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, candidate) -> bool:
        return self.spec1.is_satisfied_by(candidate) or self.spec2.is_satisfied_by(candidate)


class NotSpecification(Specification):
    """
    Permite negar una especificación con un operador lógico NOT.
    """
    def __init__(self, spec: Specification):
        self.spec = spec

    def is_satisfied_by(self, candidate) -> bool:
        return not self.spec.is_satisfied_by(candidate)
