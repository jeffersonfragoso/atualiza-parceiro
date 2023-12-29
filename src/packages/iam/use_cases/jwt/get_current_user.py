import structlog

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from src import _seedwork
from src.packages.iam.domain.commands import GetCurrentUserCommand
from src.packages.user.infra.repository import AbstractUserRepository

log = structlog.stdlib.get_logger()


class GetCurrentUserCommandExecutor(_seedwork.CommandExecutor):
    user_repository: AbstractUserRepository

    def execute(self, command: GetCurrentUserCommand):
        log.info("Executando commando")
        user = self.user_repository.get_by_user_name(command.user_name)

        if user:
            raise Exception("Usuário já Existe.")
        else:
            new_user = User(
                user_name=command.user_name,
                password_hash=Crypt.encrypt_secret(secret=command.password),
            )

            self.user_repository.add(new_user)
            print(new_user.events)
            self.set_events(new_user.events)

        return UserDto.OutputNewUser(data=new_user.to_dict())

    def commit(self) -> None:
        self.user_repository.commit()

    def rollback(self) -> None:
        self.user_repository.rollback()
