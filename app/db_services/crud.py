from tortoise.exceptions import DoesNotExist

from app.models.models import User, Notification
from app.core.logging import logger
from app.services.cache_service import get_cached_notifications, set_cached_notifications, invalidate_user_cache
from app.services.other_functions import create_notification_out
from app.exception_handlers.exception_handlers import NotificationNotFoundException


async def write_user_to_the_database(username: str, password: str):
    """ Запись пользователя в таблицу User в БД """
    user = await User.create(username=username, password=password)
    logger.info(f"Пользователь создан: ID {user.id}, {username}")
    return user


async def search_user_in_the_database(username: str):
    """ Поиск пользователя по username в таблице User в БД """
    user = await User.filter(username=username).first()
    if user:
        logger.info(f"Пользователь найден: ID {user.id}")
    else:
        logger.info(f"Пользователь не найден: {username}")
    return user


async def write_notification_to_the_database(user: User, type_not: str, text: str):
    """ Запись уведомления в таблицу Notification в БД """
    notification = await Notification.create(user=user, type=type_not, text=text)
    logger.info(f"Уведомление создано: ID {notification.id}")
    # Инвалидируем кэш пользователя
    await invalidate_user_cache(user.id)
    return notification


async def search_notifications_user_in_the_database(user: User, offset: int, limit: int):
    """ Поиск уведомлений пользователя в таблице Notification в БД """
    notifications = await Notification.filter(user_id=user.id).order_by("-created_at").offset(offset).limit(limit).prefetch_related("user")
    return notifications


async def search_notifications_user_in_the_database_with_cache(user: User, offset: int, limit: int):
    """ Поиск уведомлений с кэшированием """
    logger.debug(f"Поиск уведомлений с кэшем: пользователь {user.id}, offset={offset}, limit={limit}")
    # Пытаемся получить из кэша
    cached_notifications = await get_cached_notifications(user.id, offset, limit)
    if cached_notifications is not None:
        logger.info(f"Уведомления из кэша: пользователь {user.id}, найдено {len(cached_notifications)} записей")
        return cached_notifications
    logger.info(f"Кэш пустой, запрос к БД: пользователь {user.id}")
    # Если нет в кэше - получаем из БД
    notifications_db = await search_notifications_user_in_the_database(user, offset, limit)
    notifications_out = [create_notification_out(n, user) for n in notifications_db]
    # Сохраняем в кэш
    await set_cached_notifications(user.id, offset, limit, notifications_out)
    logger.info(f"Уведомления из БД: пользователь {user.id}, найдено {len(notifications_out)} записей, сохранено в кэш")
    return notifications_out


async def delete_notification_user_by_id_from_the_database(notification_id: int, user: User):
    """ Удаление уведомления пользователя по id из таблицы Notification в БД """
    try:
        notification = await Notification.get(id=notification_id, user_id=user.id)
        logger.info(f"Уведомление {notification_id} найдено для удаления")
        # Инвалидируем кэш перед удалением
        await invalidate_user_cache(user.id)
        return notification
    except DoesNotExist:
        logger.warning(f"Уведомление {notification_id} не найдено для пользователя {user.id}")
        raise NotificationNotFoundException()
