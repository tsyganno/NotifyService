from fastapi import APIRouter, Depends, Query, status
from typing import List

from app.models.models import User
from app.core.logging import logger
from app.core.security import get_current_user
from app.services.other_functions import create_notification_out
from app.rest_models.rest_models import NotificationOut, NotificationCreate, UserOut
from app.db_services.crud import write_notification_to_the_database, search_notifications_user_in_the_database, \
    delete_notification_user_by_id_from_the_database

notification_router = APIRouter(prefix="/notifications")


@notification_router.post("", response_model=NotificationOut)
async def create_notification(notification_data: NotificationCreate, user: User = Depends(get_current_user)):
    """ Роут для создания уведомления пользователем """
    try:
        notification = await write_notification_to_the_database(user, notification_data.type, notification_data.text)
        logger.info(f"Уведомление создано: ID {notification.id}, пользователь: {user.username}")
        return create_notification_out(notification, user)
    except Exception as ex:
        logger.error(f"Ошибка создания уведомления: {ex}")


@notification_router.get("", response_model=List[NotificationOut])
async def get_notifications(user: User = Depends(get_current_user), limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    """ Роут получения списка своих уведомлений с пагинацией """
    notifications = await search_notifications_user_in_the_database(user, offset, limit)
    logger.debug(f"Найдено уведомлений: {len(notifications)}")
    return [create_notification_out(n, user) for n in notifications]


@notification_router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(notification_id: int, current_user: User = Depends(get_current_user)):
    """ Роут для удаления своего уведомления """
    notification = await delete_notification_user_by_id_from_the_database(notification_id, current_user)
    await notification.delete()
    logger.info(f"Уведомление {notification_id} удалено")
