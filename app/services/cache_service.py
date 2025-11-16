import pickle
from typing import Optional, List
from app.core.redis import get_redis
from app.core.config import settings
from app.core.logging import logger


def _get_cache_key(prefix: str, user_id: int, offset: int, limit: int) -> str:
    """Генерация ключа для кэша"""
    return f"{prefix}:{user_id}:{offset}:{limit}"


async def get_cached_notifications(user_id: int, offset: int, limit: int) -> Optional[List]:
    """Получение уведомлений из кэша"""
    try:
        redis_client = get_redis()
        cache_key = _get_cache_key("notifications", user_id, offset, limit)
        cached_data = await redis_client.get(cache_key)
        if cached_data:
            logger.info(f"Кэш HIT для пользователя {user_id}, offset={offset}, limit={limit}")
            return pickle.loads(cached_data.encode('latin1'))
        logger.info(f"Кэш MISS для пользователя {user_id}, offset={offset}, limit={limit}")
        return None
    except Exception as e:
        logger.error(f"Ошибка получения из кэша: {e}")
        return None


async def set_cached_notifications(user_id: int, offset: int, limit: int, notifications: List):
    """Сохранение уведомлений в кэш"""
    try:
        redis_client = get_redis()
        cache_key = _get_cache_key("notifications", user_id, offset, limit)
        serialized_data = pickle.dumps(notifications).decode('latin1')
        await redis_client.setex(
            cache_key,
            settings.CACHE_EXPIRE_SECONDS,
            serialized_data
        )
        logger.info(f"Уведомления сохранены в кэш: пользователь {user_id}")
    except Exception as e:
        logger.error(f"Ошибка сохранения в кэш: {e}")


async def invalidate_user_cache(user_id: int):
    """Инвалидация всех кэшей уведомлений пользователя"""
    try:
        redis_client = get_redis()
        pattern = f"notifications:{user_id}:*"
        keys = await redis_client.keys(pattern)
        if keys:
            await redis_client.delete(*keys)
            logger.info(f"Кэш инвалидирован для пользователя {user_id}, удалено ключей: {len(keys)}")
        else:
            logger.info(f"Кэш не найден для пользователя {user_id}")
    except Exception as e:
        logger.error(f"Ошибка инвалидации кэша: {e}")
