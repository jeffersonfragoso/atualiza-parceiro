class CustomException(Exception):
    message: str

    def __init__(self) -> None:
        super().__init__(self.message)


class BadRequestException(CustomException):
    message: str = "Bad Request"


class NotFoundException(CustomException):
    message: str = "Not Found"


class AuthenticationException(CustomException):
    message: str = "Invalid authorization code."
