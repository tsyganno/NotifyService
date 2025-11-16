import uvicorn

from fastapi import FastAPI

from app.routers.users import user_router
from app.routers.notifications import notification_router
from app.db_services.database import init_db, close_db
from app.core.logging import logger


app = FastAPI(title="NotifyService")

# Подключаем роутеры
app.include_router(user_router)
app.include_router(notification_router)


# События запуска и остановки
@app.on_event("startup")
async def startup_event():
    await init_db()
    logger.info("База данных успешно подключена")


@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
    logger.info("Подключения к базе данных закрыты")


# Для тестирования
@app.get("/")
async def root():
    return {"message": "Notification Service is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
