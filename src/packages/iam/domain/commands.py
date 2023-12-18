from src._seedwork.command import Command


class GetCurrentUserCommand(Command):
    user_name: str
    password: str
