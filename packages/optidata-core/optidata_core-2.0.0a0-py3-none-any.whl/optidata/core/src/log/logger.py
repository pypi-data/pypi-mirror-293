import logging
import logging.config
import os


class Logger:
    _instance = None

    def __new__(cls, config_file=None):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(config_file)
        return cls._instance

    def _initialize(self, config_file):
        if config_file and os.path.exists(config_file):
            logging.config.fileConfig(config_file)
        else:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger()

    def get_logger(self):
        return self.logger

    @classmethod
    def log_exception(cls, ex):
        logger = cls().get_logger()
        logger.error("Exception occurred", exc_info=True)

# Exportar una función para obtener el logger en lugar de crear múltiples instancias
def get_logger(config_file=None):
    return Logger(config_file=config_file).get_logger()

def get_path_base():
    # Obtiene el path absoluto del directorio donde se encuentra este archivo
    ruta_actual = os.path.abspath(__file__)
    # Obtiene el directorio base del proyecto
    path_base = os.path.dirname(ruta_actual)
    return path_base