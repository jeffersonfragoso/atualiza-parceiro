from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import ExpiredSignatureError, JWTError, jwt
from pydantic import BaseModel

from src._seedwork.exceptions import (
    AuthenticationException,
    NotAuthenticatedException,
)
from src.config import get_settings
from src.packages._shared.messages import (
    MENSAGEM_AUTENTICACAO_REQUERIDA,
    MENSAGEM_SCHEMA_BEARER,
    MENSAGEM_TOKEN_INVALIDO_EXPIRADO,
)

variables = get_settings()
SECRET_KEY = variables.secret_key
ALGORITHM = variables.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = variables.access_token_expire_minutes
DATETIME_FORMAT = variables.datetime_format


class InputSignIn(BaseModel):
    email: str
    senha: str
    expires_in: Optional[int]


class InputDataToEncode(BaseModel):
    sub: str
    exp: Optional[datetime] = datetime.utcnow() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )


class OutputSignIn(BaseModel):
    access_token: str
    expires_at: str
    token_type: str = "bearer"


class CustomJWTBearer(HTTPBearer):
    """Implementado para customizar a integração do FastAPI
    com o botão "Authorize" na interface do swagger-ui.
    Possibilitando validações e customização de mensagens.
    """

    def __init__(self):
        super(CustomJWTBearer, self).__init__(auto_error=False)

    async def __call__(self, request: Request):
        authorization = request.headers.get("Authorization")
        scheme, token = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and token):
            raise NotAuthenticatedException(
                message=MENSAGEM_AUTENTICACAO_REQUERIDA
            )
        if scheme.lower() != "bearer":
            raise AuthenticationException(message=MENSAGEM_SCHEMA_BEARER)

        return token


class Jwt:
    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, ALGORITHM)
        except (JWTError, ExpiredSignatureError):
            raise AuthenticationException(
                message=MENSAGEM_TOKEN_INVALIDO_EXPIRADO
            )

    @staticmethod
    def create_access_token(data: InputDataToEncode) -> OutputSignIn:
        access_token = jwt.encode(data.model_dump(), SECRET_KEY, ALGORITHM)
        expiration_datetime = data.exp.strftime(DATETIME_FORMAT)
        return OutputSignIn(
            access_token=access_token, expires_at=expiration_datetime
        )

    @staticmethod
    async def auth_required(
        token=Depends(CustomJWTBearer()),
    ):
        return token
