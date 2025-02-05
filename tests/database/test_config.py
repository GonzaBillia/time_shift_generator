import pytest
from infrastructure.databases.config.database import DBConfig

def test_database_connection():
    """Verifica que la base de datos está accesible."""
    assert DBConfig.check_connection("rrhh") == True

def test_get_session():
    """Verifica que se puede obtener una sesión válida."""
    session = DBConfig.get_session("rrhh")
    assert session is not None
    session.close()
