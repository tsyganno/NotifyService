import jwt

from fastapi import APIRouter

from app.core.config import settings
from app.core.logging import logger
from app.core.security import create_access_token, create_refresh_token, get_password_hash, verify_password
from app.db_services.crud import search_user_in_the_database, write_user_to_the_database
from app.rest_models.rest_models import AccessRefreshToken, LoginRegisterIn, AccessToken, RefreshIn
from app.exception_handlers.exception_handlers import UserExistsException, UserNotFoundException, \
    RefreshTokenExpiredException, InvalidRefreshTokenException


user_router = APIRouter(prefix="/auth")


@user_router.post('/login', response_model=AccessRefreshToken)
async def login(payload: LoginRegisterIn):
    """ Роут для получения access токенов """
    logger.info(f"Попытка входа пользователя: {payload.username}")
    user = await search_user_in_the_database(payload.username)
    if not user:
        logger.warning(f"Пользователь не найден: {payload.username}")
        raise UserNotFoundException()
    if not verify_password(payload.password, user.password):
        logger.warning(f"Неверный пароль для пользователя: {payload.username}")
        raise UserNotFoundException()
    access = create_access_token(user.id)
    refresh = create_refresh_token(user.id)
    logger.info(f"Успешный вход пользователя: {user.username} (ID: {user.id})")
    return {"access": access, "refresh": refresh, "user_id": user.id}


@user_router.post('/register', response_model=AccessRefreshToken)
async def create_new_user(payload: LoginRegisterIn):
    """ Роут для регистрации пользователя """
    logger.info(f"Попытка регистрации пользователя: {payload.username}")
    user = await search_user_in_the_database(payload.username)
    if not user:
        hashed = get_password_hash(payload.password)
        user = await write_user_to_the_database(payload.username, hashed)
        access = create_access_token(user.id)
        refresh = create_refresh_token(user.id)
        logger.info(f"Пользователь зарегистрирован: {user.username} (ID: {user.id})")
        return {"access": access, "refresh": refresh, "user_id": user.id}
    logger.warning(f"Попытка регистрации существующего пользователя: {payload.username}")
    raise UserExistsException()


@user_router.post("/refresh", response_model=AccessToken)
async def refresh(token: RefreshIn):
    """ Роут для получения refresh токенов """
    logger.debug("Обновление access токена")
    try:
        payload = jwt.decode(token.refresh, settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            logger.warning("Попытка использовать не refresh токен")
            raise InvalidRefreshTokenException()
        user_id = int(payload.get("sub"))
        access = create_access_token(user_id)
        logger.info(f"Access токен обновлен для пользователя: {user_id}")
        return {"access": access}
    except jwt.ExpiredSignatureError:
        logger.warning("Refresh токен истек")
        raise RefreshTokenExpiredException()
    except Exception as ex:
        logger.warning(f"Невалидный refresh токен: {type(ex).__name__}")
        raise InvalidRefreshTokenException()
