from tortoise import Tortoise
from app.core.config import settings

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"},
    "apps": {
        "models": {
            "models": ["app.models.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
    # await Tortoise.generate_schemas() # можно использовать для быстрого старта


async def close_db():
    await Tortoise.close_connections()
