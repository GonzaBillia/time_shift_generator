import os
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker
from application.config.logger_config import setup_logger
from infrastructure.databases.config.dict import DB_PREFIXES

# Crea el logger para este módulo
logger = setup_logger(__name__, "logs/db_config.log")

class DBConfig:
    @staticmethod
    def create_engine(db_name: str):
        """
        Crea y devuelve un SQLAlchemy Engine usando las variables
        de entorno definidas. Retorna None si la configuración o 
        la creación del engine falla.
        """
        try:
            logger.info("Iniciando creación de engine para la base de datos con SQLAlchemy...")

            # Verifica si el db_name está mapeado
            prefix = DB_PREFIXES.get(db_name)
            if not prefix:
                logger.error(f"[DBConfig] No existe configuración para db_name '{db_name}'.")
                return None

            # Lee las variables según el prefijo
            host = os.getenv(f"{prefix}_DB_HOST")
            user = os.getenv(f"{prefix}_DB_USER")
            password = os.getenv(f"{prefix}_DB_PASSWORD")
            database = os.getenv(f"{prefix}_DB_DATABASE")
            port = os.getenv(f"{prefix}_DB_PORT")

            # Validación básica
            if not all([host, user, password, database, port]):
                logger.error(f"[DBConfig] Faltan variables de entorno para {db_name}.")
                return None

            # Arma la URL de conexión de SQLAlchemy (ejemplo MySQL con driver PyMySQL)
            connection_url = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}?charset=utf8"

            engine = create_engine(connection_url, echo=False, future=True)
            logger.info(f"Engine de SQLAlchemy creado correctamente para '{database}' en {host}:{port}.")
            return engine

        except SQLAlchemyError as e:
            logger.error(f"Error de SQLAlchemy al crear el engine: {e}")
            return None
        except Exception as e:
            logger.exception(f"Error inesperado al crear el engine: {e}")
            return None

    @staticmethod
    def check_connection(engine):
        """
        Verifica si podemos obtener una conexión del engine. 
        Retorna True si podemos conectar, False en caso contrario.
        """
        if not engine:
            logger.warning("No hay engine para verificar la conexión.")
            return False

        try:
            with engine.connect() as connection:
                # Basta con "hacer algo" en la conexión para ver si falla
                result = connection.execute("SELECT 1")
                logger.debug(f"Resultado de test SELECT 1: {result.scalar()}")
            logger.debug("La conexión mediante el engine es válida.")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error al intentar conectar con el engine: {e}")
            return False

    @staticmethod
    def close_engine(engine):
        """
        Cierra (dispose) el engine de SQLAlchemy si existe, 
        liberando todas las conexiones del pool.
        """
        if engine:
            try:
                engine.dispose()
                logger.info("Engine de SQLAlchemy cerrado correctamente (dispose).")
            except SQLAlchemyError as e:
                logger.error(f"Error al cerrar el engine: {e}")
        else:
            logger.warning("No hay engine activo para cerrar.")

    @staticmethod
    def open_session(engine):
        """
        Crea y devuelve una sesión de SQLAlchemy.
        Lanza excepción si no puede crearse la sesión.
        """
        if not engine:
            logger.error("No se puede crear la sesión: engine es None.")
            return None

        try:
            SessionLocal = sessionmaker(bind=engine, future=True)
            session = SessionLocal()
            logger.debug("Sesión de SQLAlchemy creada correctamente.")
            return session
        except SQLAlchemyError as e:
            logger.error(f"Error al crear la sesión: {e}")
            return None
