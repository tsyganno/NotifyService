from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class NotificationType(str, Enum):
    like = "like"
    comment = "comment"
    repost = "repost"


class UserOut(BaseModel):
    id: int
    username: str
    avatar_url: str


# class Config:
# orm_mode = True


class NotificationCreate(BaseModel):
    type: NotificationType
    text: str


class NotificationOut(BaseModel):
    id: int
    user_id: int
    type: NotificationType
    text: str
    created_at: datetime
    user: UserOut

#
# class Config:
# orm_mode = True
#
#
# class PaginatedNotifications(BaseModel):
# total: int
# items: List[NotificationOut]


class LoginRegisterIn(BaseModel):
    username: str
    password: str


class AccessRefreshToken(BaseModel):
    access: str
    refresh: str
    user_id: int


class AccessToken(BaseModel):
    access: str  # ← Правильное имя поля
