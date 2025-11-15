import jwt

from fastapi import APIRouter

from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.db_services.crud import search_user_in_the_database, write_user_to_the_database
from app.rest_models.rest_models import AccessRefreshToken, LoginRegisterIn, AccessToken
from app.exception_handlers.exception_handlers import UserExists, UserNotFoundException, RefreshTokenExpiredException, \
    InvalidRefreshTokenException


user_router = APIRouter(prefix="/auth")


@user_router.post('/login', response_model=AccessRefreshToken)
async def login(payload: LoginRegisterIn):
    """ Роут для получения access токенов """
    user_data_from_db = await search_user_in_the_database(payload.username)
    if not user_data_from_db:
        raise UserNotFoundException()
    if user_data_from_db.username is None or payload.password != user_data_from_db.password:
        raise UserNotFoundException()
    access = create_access_token(user_data_from_db.id)
    refresh = create_refresh_token(user_data_from_db.id)
    return {"access": access, "refresh": refresh, "user_id": user_data_from_db.id}


@user_router.post('/register', response_model=AccessRefreshToken)
async def create_new_user(payload: LoginRegisterIn):
    """ Роут для регистрации пользователя """
    user_db = await search_user_in_the_database(payload.username)
    if not user_db:
        user = await write_user_to_the_database(payload.username, payload.password)
        access = create_access_token(user.id)
        refresh = create_refresh_token(user.id)
        return {"message": "User successfully created.", "access": access, "refresh": refresh, "user_id": user.id}
    raise UserExists()


@user_router.post("/refresh", response_model=AccessToken)
async def refresh(token: dict):
    """ Роут для получения refresh токенов """
    try:
        payload = jwt.decode(token.get("refresh"), settings.SECRET_KEY, algorithms=["HS256"])
        if payload.get("type") != "refresh":
            raise Exception()
        user_id = int(payload.get("sub"))
    except jwt.ExpiredSignatureError:
        raise RefreshTokenExpiredException()
    except Exception:
        raise InvalidRefreshTokenException()
    access = create_access_token(user_id)
    return {"access": access}
