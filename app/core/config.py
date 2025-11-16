from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # корень проекта


class Settings(BaseSettings):
    # PostgreSQL настройки
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    # JWT настройки
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    # Redis настройки
    REDIS_URL: str
    CACHE_EXPIRE_SECONDS: int  # 5 минут по умолчанию

    class Config:
        env_file = BASE_DIR / ".env"  # имя файла с переменными окружения


# Создаём объект settings для использования в проекте
settings = Settings()

LOG_DIR = BASE_DIR / "logs"
LOG_FILE_PATH = LOG_DIR / "prod.log"

ALGO = "HS256"

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@db:5432/{settings.POSTGRES_DB}"},
    "apps": {
        "models": {
            "models": ["app.models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}
