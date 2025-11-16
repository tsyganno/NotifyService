from fastapi import HTTPException


class UserExistsException(HTTPException):
    """Исключение: пользователь уже существует"""
    def __init__(self, detail: str = 'Error! User already exists.', status_code: int = 400):
        super().__init__(detail=detail, status_code=status_code)


class UserNotFoundException(HTTPException):
    """Исключение: пользователь не найден"""
    def __init__(self, detail: str = 'Error! The user was not found.', status_code: int = 400):
        super().__init__(detail=detail, status_code=status_code)


class AccessTokenExpiredException(HTTPException):
    """Исключение: access токен истек"""
    def __init__(self, detail: str = 'Access token expired', status_code: int = 401):
        super().__init__(detail=detail, status_code=status_code)


class InvalidAccessTokenException(HTTPException):
    """Исключение: невалидный access токен"""
    def __init__(self, detail: str = 'Invalid access token', status_code: int = 401):
        super().__init__(detail=detail, status_code=status_code)


class RefreshTokenExpiredException(HTTPException):
    """Исключение: refresh токен истек"""
    def __init__(self, detail: str = 'Refresh token expired', status_code: int = 401):
        super().__init__(detail=detail, status_code=status_code)


class InvalidRefreshTokenException(HTTPException):
    """Исключение: невалидный refresh токен"""
    def __init__(self, detail: str = 'Invalid refresh token', status_code: int = 401):
        super().__init__(detail=detail, status_code=status_code)


class NotificationNotFoundException(HTTPException):
    """Исключение: уведомление не найдено"""
    def __init__(self, detail: str = 'Error! The notification was not found.', status_code: int = 404):
        super().__init__(detail=detail, status_code=status_code)
