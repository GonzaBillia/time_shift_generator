import os
import pymysql
from pymysql import MySQLError
from application.config.logger_config import setup_logger
from infrastructure.databases.config.dict import DB_PREFIXES

# Crea el logger para este módulo
logger = setup_logger(__name__, "logs/db_config.log")

class DBConfig:
    @staticmethod
    def create_connection(db_name: str):
        """
        Crea y devuelve una conexión a la base de datos MySQL 
        usando las variables de entorno definidas.
        Retorna None si la conexión falla.
        """

        try:
            logger.info("Iniciando creación de conexión a la base de datos...")

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

            # Intenta conectar
            connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database=database,
                port=int(port),
                cursorclass=pymysql.cursors.DictCursor,
                charset='utf8'
            )

            logger.info(f"Conexión exitosa a la base de datos {database} en {host}:{port}.")
            return connection

        except MySQLError as e:
            logger.error(f"Error de MySQL al conectar: {e}")
            return None
        except ValueError as e:
            logger.error(f"Puerto no válido u otro error de valor: {e}")
            return None
        except Exception as e:
            logger.exception(f"Error inesperado al crear la conexión: {e}")
            return None

    @staticmethod
    def check_connection(connection):
        """
        Verifica si la conexión está activa.
        Retorna True si está abierta, False en caso contrario.
        """
        try:
            if connection and connection.open:
                logger.debug("La conexión está activa.")
                return True
            else:
                logger.warning("La conexión no está activa o es None.")
                return False
        except MySQLError as e:
            logger.error(f"Error al verificar la conexión: {e}")
            return False

    @staticmethod
    def close_connection(connection):
        """
        Cierra la conexión a la base de datos si está activa.
        """
        try:
            if connection and connection.open:
                connection.close()
                logger.info("Conexión cerrada correctamente.")
            else:
                logger.warning("No hay conexión activa para cerrar.")
        except MySQLError as e:
            logger.error(f"Error al cerrar la conexión: {e}")

    @staticmethod
    def open_cursor(connection):
        """
        Abre y devuelve un cursor para realizar consultas.
        Lanza ConnectionError si la conexión no está activa.
        """
        try:
            if DBConfig.check_connection(connection):
                cursor = connection.cursor()
                logger.debug("Cursor abierto correctamente.")
                return cursor
            else:
                raise ConnectionError("No se pudo abrir el cursor: conexión no activa.")
        except MySQLError as e:
            logger.error(f"Error al abrir el cursor: {e}")
            raise
