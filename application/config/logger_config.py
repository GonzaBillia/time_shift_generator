# logger_config.py

import logging
import os

def setup_logger(name: str, log_file: str = "logs/application.log") -> logging.Logger:
    """
    Configura un logger con un ConsoleHandler y un FileHandler.
    Todos los mensajes >= DEBUG irán al archivo de log; 
    los mensajes >= INFO irán a la consola.
    
    :param name: Nombre del logger (por lo general, __name__).
    :param log_file: Ruta del archivo de log. Por defecto: logs/application.log
    :return: logger configurado.
    """

    # Asegúrate de que exista la carpeta logs/
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Crea o adquiere el logger
    logger = logging.getLogger(name)

    # Evita que se dupliquen mensajes si el logger ya está configurado
    if logger.hasHandlers():
        logger.handlers.clear()

    # Establece el nivel mínimo de severidad que se registrará
    logger.setLevel(logging.DEBUG)  # Capturará DEBUG y superiores

    # Formato del log
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler para la consola (StreamHandler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # mostrará mensajes de INFO o superior
    console_handler.setFormatter(formatter)

    # Handler para el archivo (FileHandler)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)    # guardará DEBUG y superior en el archivo
    file_handler.setFormatter(formatter)

    # Asigna los handlers al logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
