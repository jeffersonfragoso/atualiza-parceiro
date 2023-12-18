from src._seedwork.exceptions import BadRequestException, NotFoundException


class UserNotFoundError(NotFoundException):
    message = "User information not found."


class UserAlreadyRegisterError(BadRequestException):
    message = "User already register."
