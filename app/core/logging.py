import logging
import sys

from logging.handlers import RotatingFileHandler
from app.core.config import LOG_DIR, LOG_FILE_PATH


class LoggingConfig:
    """Класс для настройки логирования"""

    def __init__(self, log_level: str = "INFO", enable_file_logging: bool = True):
        self.log_level = getattr(logging, log_level.upper())
        self.enable_file_logging = enable_file_logging
        self._setup_directories()

    def _setup_directories(self):
        """Создание необходимых директорий"""
        LOG_DIR.mkdir(exist_ok=True)

    def _get_formatter(self) -> logging.Formatter:
        """Получить форматтер для логов"""
        return logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )

    def setup(self) -> logging.Logger:
        """Настройка логирования и возврат корневого логгера"""

        handlers = []

        # Консольный handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self._get_formatter())
        handlers.append(console_handler)

        # Файловый handler (если включен)
        if self.enable_file_logging:
            file_handler = RotatingFileHandler(
                LOG_FILE_PATH,
                maxBytes=5 * 1024 * 1024,
                backupCount=5,
                encoding='utf-8'
            )
            file_handler.setFormatter(self._get_formatter())
            handlers.append(file_handler)

        # Настройка базового конфига
        logging.basicConfig(
            level=self.log_level,
            handlers=handlers,
            force=True  # Перезаписать существующие handlers
        )

        # Отключаем propagation для сторонних логгеров
        self._disable_external_loggers()

        logger = logging.getLogger()
        logger.info("Логирование инициализировано")
        logger.info(f"Уровень логирования: {logging.getLevelName(self.log_level)}")

        return logger

    def _disable_external_loggers(self):
        """Отключение/настройка сторонних логгеров"""
        external_loggers = ["aiogram.event", "aiogram", "uvicorn.access"]

        for logger_name in external_loggers:
            external_logger = logging.getLogger(logger_name)
            external_logger.propagate = False
            external_logger.setLevel(logging.WARNING)


# Использование
logging_config = LoggingConfig(log_level="INFO", enable_file_logging=True)
logger = logging_config.setup()

# Для получения именованного логгера в других модулях:
# from app.utils.logging import get_logger
# logger = get_logger(__name__)
