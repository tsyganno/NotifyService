import jwt
from jose import JWTError
from jwt import ExpiredSignatureError
from fastapi import Depends
from tortoise.exceptions import DoesNotExist
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.exception_handlers.exception_handlers import AccessTokenExpiredException, InvalidAccessTokenException, UserNotFoundException
from app.models.models import User
from app.core.config import ALGO, settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(user_id: int) -> str:
    """ Создание access-токена """
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)


def create_refresh_token(user_id: int) -> str:
    """ Создание refresh-токена """
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """ Извлечение текущего пользователя из JWT access-токена """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGO])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise InvalidAccessTokenException()
    except ExpiredSignatureError:
        raise AccessTokenExpiredException()
    except (JWTError, ValueError):
        raise InvalidAccessTokenException()

    try:
        user = await User.get(id=user_id)
    except DoesNotExist:
        raise UserNotFoundException()

    return user
