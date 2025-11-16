import redis.asyncio as redis
from app.core.config import settings
from app.core.logging import logger

# Глобальная переменная для Redis клиента
redis_client = None


async def init_redis():
    """Инициализация Redis подключения"""
    global redis_client
    try:
        redis_client = redis.from_url(
            settings.REDIS_URL,
            encoding="utf-8",
            decode_responses=True
        )
        await redis_client.ping()
        logger.info("Redis подключен успешно")
        return redis_client
    except Exception as e:
        logger.error(f"Ошибка подключения к Redis: {e}")
        raise


async def close_redis():
    """Закрытие Redis подключения"""
    global redis_client
    if redis_client:
        await redis_client.close()
        logger.info("Redis отключен")


def get_redis():
    """Получение Redis клиента"""
    if redis_client is None:
        raise RuntimeError("Redis не инициализирован")
    return redis_client
