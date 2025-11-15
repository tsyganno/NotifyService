import pytz

from datetime import datetime
from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parent.parent.parent  # корень проекта


class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    REDIS_URL: str

    class Config:
        env_file = BASE_DIR / ".env"  # имя файла с переменными окружения


irkutsk_tz = pytz.timezone("Asia/Irkutsk")
created_at_irkutsk_tz = datetime.now(irkutsk_tz)

# Создаём объект settings для использования в проекте
settings = Settings()

LOG_DIR = BASE_DIR / "logs"
LOG_FILE_PATH = LOG_DIR / "prod.log"

print(
    settings.POSTGRES_HOST,
    settings.POSTGRES_PORT,
    settings.POSTGRES_USER,
    settings.POSTGRES_DB
)
