from fastapi import HTTPException


class UserExists(HTTPException):
    def __init__(self, detail: str = 'Error! User already exists.', status_code: int = 400):
        super().__init__(detail=detail, status_code=status_code)


class UserNotFoundException(HTTPException):
    def __init__(self, detail: str = 'Error! The user was not found.', status_code: int = 400):
        super().__init__(detail=detail, status_code=status_code)


class RefreshTokenExpiredException(HTTPException):
    def __init__(self, detail: str = 'Refresh token expired', status_code: int = 401):
        super().__init__(detail=detail, status_code=status_code)


class InvalidRefreshTokenException(HTTPException):
    def __init__(self, detail: str = 'Invalid refresh token', status_code: int = 401):
        super().__init__(detail=detail, status_code=status_code)
