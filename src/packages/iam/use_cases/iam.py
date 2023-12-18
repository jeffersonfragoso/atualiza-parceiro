import structlog

from dependency_injector.wiring import Provide, inject
from fastapi import Depends
from jose import jwt
from pydantic import ValidationError

from src import _seedwork
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


@inject
def get_current_user(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        raise AuthError(detail="Could not validate credentials")
    current_user: User = service.get_by_id(token_data.id)
    if not current_user:
        raise AuthError(detail="User not found")
    return current_user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    return current_user


def get_current_user_with_no_exception(
    token: str = Depends(JWTBearer()),
    service: UserService = Depends(Provide[Container.user_service]),
) -> User:
    try:
        payload = jwt.decode(token, configs.SECRET_KEY, algorithms=ALGORITHM)
        token_data = Payload(**payload)
    except (jwt.JWTError, ValidationError):
        return None
    current_user: User = service.get_by_id(token_data.id)
    if not current_user:
        return None
    return current_user


def get_current_super_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise AuthError("Inactive user")
    if not current_user.is_superuser:
        raise AuthError("It's not a super user")
    return current_user
