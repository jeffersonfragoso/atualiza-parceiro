import _seedwork

from src.packages.user.domain.commands import CreateUserCommand
from src.packages.user.domain.entities import User
from src.packages.user.domain.events import UserCreatedEvent
from src.packages.user.infra.repository import AbstractUserRepository
from src.packages.user.infra import Crypt
from src.packages.user.use_cases.dto import UserDto


class CreateUserCommandExecutor(_seedwork.CommandExecutor):
    user_repository: AbstractUserRepository

    def execute(self, command: CreateUserCommand) -> UserDto.OutputNewUser:

        user = self.user_repository.get_by_user_name(command.user_name)

        if user:
          raise Exception("Usuário já Existe.")
        else:
          new_user = User(user_name=command.user_name, password_hash=Crypt.encrypt_secret(secret=command.password))

          self.user_repository.add(new_user)
          print(new_user.events)
          self.set_events(new_user.events)

        return UserDto.OutputNewUser(data=new_user.to_dict())

    def commit(self) -> None:
        self.user_repository.commit()

    def rollback(self) -> None:
        self.user_repository.rollback()


class UserCreatedEventExecutor(_seedwork.EventExecutor):
    email_client = lambda x, event: print(f"Enviando email de boas vindas para: {event.user_name}")

    def execute(self, event: UserCreatedEvent) -> None:
        print(f"Usuario cadastrado: {event.user_name}")
        self.email_client(event)
        # self.set_events(['TESTE'])

    def commit(self) -> None:
        print("Commit do evento executado")

    def rollback(self) -> None:
        print("Rollback do evento executado")