from fastapi import APIRouter, Depends, Query, status
from typing import List
from tortoise.exceptions import DoesNotExist

from app.models.models import User
from app.core.security import get_current_user
from app.rest_models.rest_models import NotificationOut, NotificationCreate, UserOut
from app.exception_handlers.exception_handlers import NotificationNotFoundException
from app.db_services.crud import write_notification_to_the_database, search_notifications_user_in_the_database, \
    delete_notification_user_by_id_from_the_database

notification_router = APIRouter(prefix="/notifications")


@notification_router.post("", response_model=NotificationOut)
async def create_notification(notification_data: NotificationCreate, current_user: User = Depends(get_current_user)):
    """ Роут для создания уведомления пользователем """
    notification = await write_notification_to_the_database(current_user, notification_data.type, notification_data.text)

    # Создаем правильный UserOut объект
    user_data = UserOut(
        id=current_user.id,
        username=current_user.username,
        avatar_url=current_user.avatar_url
    )

    return NotificationOut(
        id=notification.id,
        user_id=notification.user.id,
        type=notification.type,
        text=notification.text,
        created_at=notification.created_at,
        user=user_data,
    )


@notification_router.get("", response_model=List[NotificationOut])
async def get_notifications(current_user: User = Depends(get_current_user), limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    """ Роут получения списка своих уведомлений с пагинацией """
    notifications = await search_notifications_user_in_the_database(current_user, offset, limit)

    user_data = UserOut(
        id=current_user.id,
        username=current_user.username,
        avatar_url=current_user.avatar_url
    )

    result = []
    for n in notifications:
        result.append(
            NotificationOut(
                id=n.id,
                user_id=n.user.id,
                type=n.type,
                text=n.text,
                created_at=n.created_at,
                user=user_data,
            )
        )
    return result


@notification_router.delete("/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(notification_id: int, current_user: User = Depends(get_current_user)):
    """ Роут для удаления своего уведомления """
    try:
        notification = await delete_notification_user_by_id_from_the_database(notification_id, current_user)
    except DoesNotExist:
        raise NotificationNotFoundException()
    await notification.delete()
