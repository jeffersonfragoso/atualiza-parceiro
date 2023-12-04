from fastapi import APIRouter, Depends, Response, status

from src.packages.user.domain.commands import CreateUserCommand
from src.packages.user.container import UserContainer, factory_user_container
from src.packages.user.use_cases.dto import UserDto


endpoints = APIRouter(prefix="/users", tags=["users"])

@endpoints.post("", response_model=UserDto.OutputNewUser)
async def post(
  user_input: UserDto.InputNewUser,
  container: UserContainer = Depends(factory_user_container)
):
  cmd = CreateUserCommand(**user_input.model_dump())
  container.domain_channel.dispatch_command(cmd)
  return Response(status_code=status.HTTP_201_CREATED)
