from app.models.models import User, Notification
from app.core.config import created_at_irkutsk_tz


async def write_user_to_the_database(username: str, password: str):
    """ Запись пользователя в таблицу User в БД """
    user = await User.create(username=username, password_hash=password, created_at=created_at_irkutsk_tz)
    return user


async def search_user_in_the_database(username: str):
    """ Поиск пользователя по username в таблице User в БД """
    user = await User.filter(username=username).first()
    return user


async def write_notification_to_the_database(user: User, type_not: str, text: str):
    """ Запись уведомления в таблицу Notification в БД """
    notification = await Notification.create(user=user, type=type_not, text=text, created_at=created_at_irkutsk_tz)
    return notification


async def search_notifications_user_in_the_database(user: User, offset: int, limit: int):
    """ Поиск уведомлений пользователя в таблице Notification в БД """
    notifications = await Notification.filter(user_id=user.id).order_by("-created_at").offset(offset).limit(limit).prefetch_related("user")
    return notifications


async def delete_notification_user_by_id_from_the_database(notification_id: int, user: User):
    """ Удаление уведомления пользователя по id из таблицы Notification в БД """
    notification = await Notification.get(id=notification_id, user_id=user.id)
    return notification
