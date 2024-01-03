from datetime import datetime, timedelta

import structlog

import _seedwork
from src._seedwork.exceptions import AuthenticationException
from src.config import get_settings
from src.packages._shared.infra.auth.jwt import InputDataToEncode, Jwt
from src.packages._shared.infra.crypt import Crypt
from src.packages._shared.messages import MENSAGEM_CREDENCIAIS_INVALIDAS
from src.packages.user.domain.commands import SignInCommand
from src.packages.user.infra.repository import AbstractUserRepository
from src.packages.user.use_cases.dto import UserDto

log = structlog.stdlib.get_logger()


class SignInCommandExecutor(_seedwork.CommandExecutor):
    user_repository: AbstractUserRepository

    def execute(self, command: SignInCommand) -> UserDto.OutputSignIn:
        log.info("Executando commando")

        user_in_db = self.user_repository.get_by_user_name(command.username)

        if not user_in_db:
            raise AuthenticationException(
                message=MENSAGEM_CREDENCIAIS_INVALIDAS
            )

        if not Crypt.verify_secret(command.senha, user_in_db.password_hash):
            raise AuthenticationException(
                message=MENSAGEM_CREDENCIAIS_INVALIDAS
            )

        expires_at = datetime.utcnow() + timedelta(
            minutes=get_settings().access_token_expire_minutes
        )
        data_to_encode = InputDataToEncode(
            sub=user_in_db.user_name, exp=expires_at
        )

        token = Jwt.create_access_token(data_to_encode)

        return token

    def commit(self) -> None:
        self.user_repository.commit()

    def rollback(self) -> None:
        self.user_repository.rollback()
