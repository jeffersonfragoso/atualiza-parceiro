from src._seedwork.command import Command


class CreateUserCommand(Command):
    user_name: str
    password: str


class GetCurrentUserCommand(Command):
    access_token: str


class SignInCommand(Command):
    username: str
    senha: str
