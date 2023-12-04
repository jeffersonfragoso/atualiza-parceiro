from src._seedwork.command import Command


class CreateUserCommand(Command):
  user_name: str
  password: str
