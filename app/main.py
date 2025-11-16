import uvicorn

from fastapi import FastAPI

from app.core.redis import init_redis, close_redis, get_redis
from app.routers.users import user_router
from app.routers.notifications import notification_router
from app.db_services.database import init_db, close_db
from app.core.logging import logger


app = FastAPI(title="NotifyService")

# Подключаем роутеры
app.include_router(user_router)
app.include_router(notification_router)


@app.on_event("startup")
async def startup_event():
    """Запуск приложения"""
    await init_db()
    await init_redis()
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
        from tortoise import Tortoise
        await Tortoise.get_connection("default").execute_query("SELECT 1")
        return {"status": "healthy", "database": "connected", "redis": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
