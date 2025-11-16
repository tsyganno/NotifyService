from app.models.models import Notification, User
from app.rest_models.rest_models import NotificationOut, UserOut


def create_notification_out(notification: Notification, user: User) -> NotificationOut:
    """ Вспомогательная функция """
    return NotificationOut(
        id=notification.id,
        user_id=notification.user.id,
        type=notification.type,
        text=notification.text,
        created_at=notification.created_at,
        user=UserOut(
            id=user.id,
            username=user.username,
            avatar_url=user.avatar_url
        ),
    )
