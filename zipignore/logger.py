import logging
from loguru import logger
import sys
from pathlib import Path

# Crear carpeta de logs si no existe
Path("logs").mkdir(exist_ok=True)

# Formato personalizado para consola y archivo
LOG_FORMAT = (
    "<level>▶ {level: <8}</level> | "
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<cyan>{name}:{function}:{line}</cyan> - "
    "<level>{message}</level>"
)


def setup_loguru(level: str = "DEBUG", log_file: str = "logs/zipignore_operation.log") -> None:
    """
    Configures loguru with:
    - Console output
    - Rotating file output
    - Interception of standard logs (uvicorn, sqlalchemy, etc.)
    """
    # Eliminar handlers previos
    logger.remove()

    # Salida en consola
    logger.add(sys.stdout, level=level, colorize=True, format=LOG_FORMAT)

    # Salida en archivo rotativo
    logger.add(log_file, rotation="1 week", retention="1 month", level=level, format=LOG_FORMAT)

    # Redirigir logs estándar a loguru
    class InterceptHandler(logging.Handler):
        def emit(self, record):
            # Intenta obtener el nivel desde loguru, o usa el numérico de fallback
            try:
                log_level = logger.level(record.levelname).name
            except ValueError:
                log_level = record.levelno

            logger.opt(depth=6, exception=record.exc_info).log(log_level, record.getMessage())


    intercept_handler = InterceptHandler()
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access", "fastapi", "sqlalchemy"):
        logging.getLogger(name).handlers = [intercept_handler]
        logging.getLogger(name).setLevel(logging.DEBUG)

# Deja importable globalmente
__all__ = ["logger", "setup_loguru"]
