import jwt
from jose import JWTError
from jwt import ExpiredSignatureError
from fastapi import Depends
from tortoise.exceptions import DoesNotExist
from datetime import datetime, timedelta
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.models.models import User
from app.core.config import ALGO, settings
from app.core.logging import logger
from app.exception_handlers.exception_handlers import AccessTokenExpiredException, InvalidAccessTokenException, \
    UserNotFoundException


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_password_hash(password: str) -> str:
    """ Получение хеш-пароля """
    logger.info(f"Создание хеша пароля для пользователя")
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """ Проверка пароля """
    try:
        result = pwd_context.verify(plain_password, hashed_password)
        logger.info(f"Проверка пароля: {'успешно' if result else 'неудачно'}")
        return result
    except Exception as e:
        logger.error(f"Ошибка проверки пароля: {e}")
        return False


def create_access_token(user_id: int) -> str:
    """ Создание access-токена """
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire, "type": "access"}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)
    logger.info(f"Создан access токен для пользователя {user_id}, истекает: {expire}")
    return token


def create_refresh_token(user_id: int) -> str:
    """ Создание refresh-токена """
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": str(user_id), "exp": expire, "type": "refresh"}
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGO)
    logger.info(f"Создан refresh токен для пользователя {user_id}, истекает: {expire}")
    return token


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    """ Извлечение текущего пользователя из JWT access-токена """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGO])
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            logger.warning("Невалидный токен: отсутствует user_id")
            raise InvalidAccessTokenException()
    except ExpiredSignatureError:
        logger.info("Access токен истек")
        raise AccessTokenExpiredException()
    except (JWTError, ValueError):
        logger.info(f"Невалидный токен: {type(e).__name__}")
        raise InvalidAccessTokenException()

    try:
        user = await User.get(id=user_id)
        logger.info(f"Успешная аутентификация пользователя: {user.username}")
    except DoesNotExist:
        logger.warning(f"Пользователь не найден: ID {user_id}")
        raise UserNotFoundException()

    return user
