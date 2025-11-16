import pytest
from tortoise import Tortoise
from app.models.models import User
from app.core.security import get_password_hash
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_create_notification(client):
    """Тест создания уведомления с авторизацией"""
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.models"]}
    )
    await Tortoise.generate_schemas()

    try:
        # Создаем пользователя
        password_hash = get_password_hash("password123")
        user = await User.create(username="notification_user", password=password_hash)

        # Логинимся для получения токена
        login_response = client.post(
            "/auth/login",
            json={"username": "notification_user", "password": "password123"}
        )
        token = login_response.json()["access"]
        headers = {"Authorization": f"Bearer {token}"}

        # Создаем уведомление
        notification_data = {
            "type": "like",
            "text": "This is a test message",
        }

        response = client.post(
            "/notifications",
            headers=headers,
            json=notification_data
        )

        assert response.status_code == 200
        data = response.json()
        assert data["type"] == "like"
        assert data["text"] == "This is a test message"

    finally:
        await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_create_notification_unauthorized(client):
    """Тест создания уведомления без авторизации"""
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.models"]}
    )
    await Tortoise.generate_schemas()

    try:
        response = client.post(
            "/notifications",
            json={"type": "like", "text": "This is a test message"}
        )

        assert response.status_code == 401  # Unauthorized

    finally:
        await Tortoise.close_connections()
