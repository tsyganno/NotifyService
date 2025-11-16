from app.core.security import verify_password, get_password_hash


def test_password_hashing():
    """Тест хеширования паролей"""
    password = "my_secure_password"
    hashed = get_password_hash(password)

    assert verify_password(password, hashed) is True
    assert verify_password("wrong_password", hashed) is False

    # Проверяем что два хеша одного пароля разные (из-за соли)
    hashed2 = get_password_hash(password)
    assert hashed != hashed2
