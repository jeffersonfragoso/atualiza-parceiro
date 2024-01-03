import structlog
from fastapi import APIRouter, Depends, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from src.packages._shared.infra.auth import Jwt, CustomJWTBearer
from src.packages.user.container import UserContainer, factory_user_container
from src.packages.user.domain.commands import (
    CreateUserCommand,
    GetCurrentUserCommand,
    SignInCommand,
)
from src.packages.user.use_cases.dto import UserDto

log = structlog.stdlib.get_logger()
endpoints = APIRouter(prefix="/users")


@endpoints.post("", response_model=UserDto.OutputUser)
async def post(
    user_input: UserDto.InputNewUser,
    container: UserContainer = Depends(factory_user_container),
):
    log.info("Log inicial da requisição")
    cmd = CreateUserCommand(**user_input.model_dump())
    new_user = container.domain_channel.dispatch_command(cmd)
    return JSONResponse(
        content=jsonable_encoder(new_user), status_code=status.HTTP_201_CREATED
    )


@endpoints.post("/sign-in")
async def sign_in(
    credenciais: UserDto.InputSignIn,
    container: UserContainer = Depends(factory_user_container),
) -> UserDto.OutputSignIn:
    """
    Realizar Signin
    """
    cmd = SignInCommand(**credenciais.model_dump())
    token = container.domain_channel.dispatch_command(cmd)

    return JSONResponse(
        content=jsonable_encoder(token), status_code=status.HTTP_200_OK
    )


@endpoints.post("/privado/1", dependencies=[Depends(Jwt.auth_required)])
async def privado_1(
    access_token=Depends(CustomJWTBearer()),
    container: UserContainer = Depends(factory_user_container),
):
    """
    Informações do usuário logado
    """
    cmd = GetCurrentUserCommand(access_token=access_token)
    current_user = container.domain_channel.dispatch_command(cmd)

    return JSONResponse(
        content=jsonable_encoder(current_user), status_code=status.HTTP_200_OK
    )
