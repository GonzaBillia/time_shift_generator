from domain.specs.base import Specification
from sqlalchemy.sql.elements import BooleanClauseList

class SqlSpecification(Specification):
    """
    Clase base para specs SQL.
    Además de is_satisfied_by, define to_expression para queries SQLAlchemy.
    """
    def to_expression(self) -> BooleanClauseList:
        raise NotImplementedError("Subclasses must override to_expression method.")
