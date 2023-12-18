import structlog
from fastapi import APIRouter, Depends, Response, status

from src.packages.user.container import UserContainer, factory_user_container
from src.packages.user.domain.commands import CreateUserCommand
from src.packages.user.use_cases.dto import UserDto

log = structlog.stdlib.get_logger()
endpoints = APIRouter(prefix="/users")


@endpoints.post("", response_model=UserDto.OutputNewUser)
async def post(
    user_input: UserDto.InputNewUser,
    container: UserContainer = Depends(factory_user_container),
):
    log.info("Log inicial da requisição")
    cmd = CreateUserCommand(**user_input.model_dump())
    container.domain_channel.dispatch_command(cmd)
    return Response(status_code=status.HTTP_201_CREATED)
