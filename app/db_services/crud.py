from app.models.models import User
from app.core.config import created_at_irkutsk_tz


async def write_user_to_the_database(username: str, password: str):
    """ Запись пользователя в таблицу User в БД """
    user = await User.create(username=username, password_hash=password, created_at=created_at_irkutsk_tz)
    return user


async def search_user_in_the_database(username: str):
    """ Поиск пользователя по username в таблице User в БД """
    user = await User.filter(username=username).first()  # Возвращает либо пользователя, либо None
    return user
