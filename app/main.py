import uvicorn

from fastapi import FastAPI
from tortoise import Tortoise

from app.core.redis import init_redis, close_redis, get_redis
from app.routers.users import user_router
from app.routers.notifications import notification_router
from app.core.config import TORTOISE_ORM
from app.core.logging import logger


app = FastAPI(title="NotifyService")

# Подключаем роутеры
app.include_router(user_router)
app.include_router(notification_router)


async def init_db():
    """Инициализация БД и создание таблиц"""
    await Tortoise.init(config=TORTOISE_ORM)
    await Tortoise.generate_schemas(safe=True)


async def close_db():
    """Закрытие соединений с БД"""
    await Tortoise.close_connections()


@app.on_event("startup")
async def startup_event():
    """Запуск приложения"""
    await init_redis()
    await init_db()
    logger.info("Приложение запущено")


@app.on_event("shutdown")
async def shutdown_event():
    """Остановка приложения"""
    await close_db()
    await close_redis()
    logger.info("Приложение остановлено")


@app.get("/health")
async def health_check():
    """Простой health check без внешних зависимостей"""
    return {"status": "healthy", "service": "NotifyService"}


@app.get("/health/full")
async def full_health_check():
    """Полный health check с проверкой БД и Redis"""
    try:
        # Проверка Redis
        redis_client = get_redis()
        await redis_client.ping()
        # Проверка БД (простая проверка подключения)
        await Tortoise.get_connection("default").execute_query("SELECT 1")
        return {"status": "healthy", "database": "connected", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
