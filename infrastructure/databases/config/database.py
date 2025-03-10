import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker, scoped_session, declarative_base
from urllib.parse import quote_plus
from application.config.logger_config import setup_logger
from infrastructure.databases.config.dict import DB_PREFIXES

# Crea el logger para este módulo
logger = setup_logger(__name__, "logs/db_config.log")
ENV_FILE = ".env"
load_dotenv(ENV_FILE)

Base = declarative_base()

class DBConfig:
    engines = {}  # Diccionario para almacenar los engines de cada BD
    sessions = {}  # Diccionario para manejar sesiones por BD

    @staticmethod
    def create_engine(db_name: str, pool_size: int = 10, max_overflow: int = 20):
        """
        Crea y devuelve un SQLAlchemy Engine con un Pool de Conexiones.
        Si ya existe un engine para `db_name`, lo reutiliza.

        Args:
            db_name (str): Nombre de la base de datos en el diccionario DB_PREFIXES.
            pool_size (int): Número de conexiones máximas en el pool.
            max_overflow (int): Número de conexiones adicionales en momentos de alta carga.

        Returns:
            SQLAlchemy Engine o None si falla la conexión.
        """
        try:
            if db_name in DBConfig.engines:
                return DBConfig.engines[db_name]  # Retorna engine si ya existe

            logger.info(f"Creando engine para la base de datos '{db_name}' con SQLAlchemy...")

            prefix = DB_PREFIXES.get(db_name)
            if not prefix:
                logger.error(f"[DBConfig] No existe configuración para db_name '{db_name}'.")
                return None

            host = os.getenv(f"{prefix}_DB_HOST")
            user = os.getenv(f"{prefix}_DB_USER")
            password = os.getenv(f"{prefix}_DB_PASSWORD", "")
            database = os.getenv(f"{prefix}_DB_DATABASE")
            port = os.getenv(f"{prefix}_DB_PORT")

            if not all([host, user, database, port]):
                logger.error(f"[DBConfig] Faltan variables de entorno para {db_name}.")
                return None

            # Codificar la contraseña para evitar problemas con caracteres especiales como '@'
            password_encoded = quote_plus(password)
            connection_url = f"mysql+pymysql://{user}:{password_encoded}@{host}:{port}/{database}?charset=utf8"

            engine = create_engine(
                connection_url,
                echo=False,
                future=True,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_pre_ping=True,  # Evita conexiones muertas
                pool_recycle=1800  # Recicla conexiones cada 30 minutos
            )

            DBConfig.engines[db_name] = engine  # Almacena el engine
            logger.info(f"Engine creado para '{database}' en {host}:{port}.")
            return engine

        except SQLAlchemyError as e:
            logger.error(f"Error de SQLAlchemy al crear el engine: {e}")
            return None
        except Exception as e:
            logger.exception(f"Error inesperado al crear el engine: {e}")
            return None

    @staticmethod
    def get_session(db_name: str):
        """
        Crea y devuelve una sesión de SQLAlchemy para la base de datos especificada.
        Usa `scoped_session` para manejar sesiones en entornos concurrentes.

        Args:
            db_name (str): Nombre de la base de datos en el diccionario DB_PREFIXES.

        Returns:
            SQLAlchemy Session o None si falla la creación.
        """
        engine = DBConfig.create_engine(db_name)
        if not engine:
            logger.error(f"No se pudo crear la sesión: no hay engine disponible para {db_name}.")
            return None

        if db_name not in DBConfig.sessions:
            SessionFactory = sessionmaker(bind=engine, future=True)
            DBConfig.sessions[db_name] = scoped_session(SessionFactory)  # Usa `scoped_session` para seguridad

        return DBConfig.sessions[db_name]()

    @staticmethod
    def check_connection(db_name: str) -> bool:
        """
        Verifica si la base de datos está accesible.

        Args:
            db_name (str): Nombre de la base de datos a verificar.

        Returns:
            bool: True si la conexión es válida, False en caso contrario.
        """
        engine = DBConfig.create_engine(db_name)
        if not engine:
            return False

        try:
            with engine.connect() as connection:
                result = connection.execute(text("SELECT 1"))
                logger.debug(f"Test SELECT 1 para '{db_name}': {result.scalar()}")
            return True
        except SQLAlchemyError as e:
            logger.error(f"Error al conectar con la base '{db_name}': {e}")
            return False

    @staticmethod
    def close_engine(db_name: str):
        """
        Cierra (dispose) el engine de SQLAlchemy para una base de datos específica.
        También limpia la sesión asociada.

        Args:
            db_name (str): Nombre de la base de datos a cerrar.
        """
        if db_name in DBConfig.sessions:
            DBConfig.sessions[db_name].remove()  # Limpia la sesión
            del DBConfig.sessions[db_name]

        if db_name in DBConfig.engines:
            try:
                DBConfig.engines[db_name].dispose()
                logger.info(f"Engine de SQLAlchemy cerrado correctamente para '{db_name}'.")
                del DBConfig.engines[db_name]
            except SQLAlchemyError as e:
                logger.error(f"Error al cerrar el engine para '{db_name}': {e}")
        else:
            logger.warning(f"No hay engine activo para '{db_name}'.")

    @staticmethod
    def get_db_session(db_name: str):
    # "MY_DB" es el nombre de la base de datos; ajústalo según corresponda
        session = DBConfig.get_session(db_name)
        try:
            yield session
        finally:
            session.close()