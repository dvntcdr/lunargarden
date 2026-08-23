from fastapi import status


class AppException(Exception):
    status_code: int
    detail: str

    def __init__(self, detail: str | None = None) -> None:
        self.detail = detail or self.__class__.detail


class AlreadyExists(AppException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Already exists'


class InvalidCredentials(AppException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Invalid credentials'
