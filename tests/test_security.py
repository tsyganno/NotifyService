from app.core.security import auth_service


def test_password_hashing():
    """Тест хеширования паролей"""
    password = "my_secure_password"
    hashed = auth_service.get_password_hash(password)

    assert auth_service.verify_password(password, hashed) is True
    assert auth_service.verify_password("wrong_password", hashed) is False

    # Проверяем что два хеша одного пароля разные (из-за соли)
    hashed2 = auth_service.get_password_hash(password)
    assert hashed != hashed2
