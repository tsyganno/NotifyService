import logging
import sys

from logging.handlers import RotatingFileHandler
from app.core.config import LOG_DIR, LOG_FILE_PATH


def setup_logging(log_level: str = "INFO", enable_file_logging: bool = True) -> logging.Logger:
    """
    Настройка логирования для приложения

    Args:
        log_level: Уровень логирования (DEBUG, INFO, WARNING, ERROR)
        enable_file_logging: Включить запись логов в файл

    Returns:
        logging.Logger: Настроенный логгер
    """
    # Создаем папку для логов если не существует
    LOG_DIR.mkdir(exist_ok=True)

    # Создаем форматтер
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
    )

    # Создаем обработчики
    handlers = []

    # Консольный обработчик
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    handlers.append(console_handler)

    # Файловый обработчик (если включен)
    if enable_file_logging:
        file_handler = RotatingFileHandler(
            LOG_FILE_PATH,
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)

    # Настройка базового конфига
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        handlers=handlers,
        force=True  # Перезаписать существующие handlers
    )

    # Отключаем propagation для сторонних логгеров
    _disable_external_loggers()

    # Получаем корневой логгер
    logger = logging.getLogger()
    logger.info("Логирование успешно настроено")
    logger.info(f"Уровень логирования: {log_level}")

    return logger


def _disable_external_loggers():
    """Отключение propagation для сторонних логгеров"""
    external_loggers = ["aiogram.event", "aiogram", "uvicorn.access"]

    for logger_name in external_loggers:
        external_logger = logging.getLogger(logger_name)
        external_logger.propagate = False
        external_logger.setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """
    Получить именованный логгер

    Args:
        name: Имя логгера (обычно __name__)

    Returns:
        logging.Logger: Настроенный логгер
    """
    return logging.getLogger(name)


# Инициализация логирования при импорте
logger = setup_logging(log_level="INFO", enable_file_logging=True)
