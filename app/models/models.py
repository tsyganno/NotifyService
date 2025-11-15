from tortoise import Model, fields
from enum import Enum


class NotificationType(str, Enum):
    like = "like"
    comment = "comment"
    repost = "repost"


class User(Model):
    """ Пользователи """
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)
    avatar_url = fields.CharField(255, default="https://example.com/default-avatar.png")
    created_at = fields.DatetimeField(auto_now_add=True)
    notifications: fields.ReverseRelation["Notification"]

    class Meta:
        table = "users"  # ← Явно указываем имя таблицы


class Notification(Model):
    """ Уведомления """
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="notifications", on_delete=fields.CASCADE)
    type = fields.CharEnumField(NotificationType)
    text = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "notifications"
