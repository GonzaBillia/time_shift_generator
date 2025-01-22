from sqlalchemy import and_, or_, not_
from .base_sql_specs import SqlSpecification

class AndSqlSpecification(SqlSpecification):
    """
    Combina dos SqlSpecification mediante un operador AND a nivel de base de datos.
    """
    def __init__(self, spec1: SqlSpecification, spec2: SqlSpecification):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, candidate) -> bool:
        """
        (Opcional) Si quieres la misma lógica en memoria, combina
        is_satisfied_by de las specs hijas.
        """
        return self.spec1.is_satisfied_by(candidate) and self.spec2.is_satisfied_by(candidate)

    def to_expression(self):
        """
        Retorna una expresión SQLAlchemy que combine los filtros
        de las dos sub-especificaciones con un AND lógico.
        """
        return and_(
            self.spec1.to_expression(),
            self.spec2.to_expression()
        )


class OrSqlSpecification(SqlSpecification):
    """
    Combina dos SqlSpecification mediante un operador OR a nivel de base de datos.
    """
    def __init__(self, spec1: SqlSpecification, spec2: SqlSpecification):
        self.spec1 = spec1
        self.spec2 = spec2

    def is_satisfied_by(self, candidate) -> bool:
        return self.spec1.is_satisfied_by(candidate) or self.spec2.is_satisfied_by(candidate)

    def to_expression(self):
        return or_(
            self.spec1.to_expression(),
            self.spec2.to_expression()
        )


class NotSqlSpecification(SqlSpecification):
    """
    Aplica el operador NOT a otra SqlSpecification.
    """
    def __init__(self, spec: SqlSpecification):
        self.spec = spec

    def is_satisfied_by(self, candidate) -> bool:
        return not self.spec.is_satisfied_by(candidate)

    def to_expression(self):
        return not_(self.spec.to_expression())