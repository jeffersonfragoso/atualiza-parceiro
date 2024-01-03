import structlog
from jose import JWTError
from pydantic import ValidationError

import _seedwork
from src._seedwork.exceptions import AuthenticationException
from src.packages._shared.infra.auth.jwt import Jwt
from src.packages._shared.messages import (
    MENSAGEM_CREDENCIAIS_INVALIDAS,
    MENSAGEM_TOKEN_INVALIDO_EXPIRADO,
)
from src.packages.user.domain.commands import GetCurrentUserCommand
from src.packages.user.infra.repository import AbstractUserRepository
from src.packages.user.use_cases.dto import UserDto

log = structlog.stdlib.get_logger()


class GetCurrentUserCommandExecutor(_seedwork.CommandExecutor):
    user_repository: AbstractUserRepository

    def execute(self, command: GetCurrentUserCommand) -> UserDto.OutputUser:
        log.info("Executando commando")

        try:
            data = Jwt.decode_token(command.access_token)
        except (JWTError, ValidationError):
            raise AuthenticationException(
                message=MENSAGEM_TOKEN_INVALIDO_EXPIRADO
            )

        user_name = data["sub"]
        current_user = self.user_repository.get_by_user_name(user_name)

        if not current_user:
            raise AuthenticationException(
                message=MENSAGEM_CREDENCIAIS_INVALIDAS
            )

        return UserDto.OutputUser(data=current_user.to_dict())

    def commit(self) -> None:
        self.user_repository.commit()

    def rollback(self) -> None:
        self.user_repository.rollback()
