import uvicorn
import asyncio
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.routers.users import user_router
from app.db_services.database import init_db, close_db
from app.exception_handlers.exception_handlers import UserExists, UserNotFoundException, RefreshTokenExpiredException, \
    InvalidRefreshTokenException


app = FastAPI(title="NotifyService")

# Подключаем роутеры
app.include_router(user_router)


@app.exception_handler(UserExists)
async def user_exists(request, exc):
    start_time = time.time()
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={'X-ErrorHandleTime': str(time.time() - start_time)}
    )


@app.exception_handler(UserNotFoundException)
async def user_not_found_exception_handler(request, exc):
    start_time = time.time()
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={'X-ErrorHandleTime': str(time.time() - start_time)}
    )


@app.exception_handler(RefreshTokenExpiredException)
async def refresh_token_expired_exception_handler(request, exc):
    start_time = time.time()
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={'X-ErrorHandleTime': str(time.time() - start_time)}
    )


@app.exception_handler(InvalidRefreshTokenException)
async def invalid_refresh_token_exception_handler(request, exc):
    start_time = time.time()
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
        headers={'X-ErrorHandleTime': str(time.time() - start_time)}
    )


# События запуска и остановки
@app.on_event("startup")
async def startup_event():
    await init_db()
    print("✅ Database connected successfully")


@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
    print("✅ Database connections closed")


# Для тестирования
@app.get("/")
async def root():
    return {"message": "Notification Service is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
