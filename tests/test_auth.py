import pytest
from tortoise import Tortoise
from app.models.models import User
from app.core.security import auth_service
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Фикстура для тестового клиента"""
    return TestClient(app)


@pytest.mark.asyncio
async def test_register(client):
    """Тест регистрации пользователя"""
    # Инициализация базы
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.models"]}
    )
    await Tortoise.generate_schemas()

    try:
        response = client.post(
            "/auth/register",
            json={"username": "testuser", "password": "password123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access" in data
        assert "refresh" in data
    finally:
        await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_login_success(client):
    """Тест успешного входа"""
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.models"]}
    )
    await Tortoise.generate_schemas()

    try:
        # Создаем пользователя
        password_hash = auth_service.get_password_hash("password123")
        await User.create(username="existinguser", password=password_hash)

        response = client.post(
            "/auth/login",
            json={"username": "existinguser", "password": "password123"}
        )

        assert response.status_code == 200
        data = response.json()
        assert "access" in data
        assert "refresh" in data
    finally:
        await Tortoise.close_connections()


@pytest.mark.asyncio
async def test_login_wrong_password(client):
    """Тест входа с неправильным паролем"""
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": ["app.models.models"]}
    )
    await Tortoise.generate_schemas()

    try:
        password_hash = auth_service.get_password_hash("correct_password")
        await User.create(username="testuser", password=password_hash)

        response = client.post(
            "/auth/login",
            json={"username": "testuser", "password": "wrong_password"}
        )

        assert response.status_code == 400
    finally:
        await Tortoise.close_connections()
