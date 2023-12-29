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


class OutputAccessToken(BaseModel):
    access_token: str
    expires_at: datetime
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


class JWTManager:
    @staticmethod
    def decode_token(token: str) -> dict:
        try:
            return jwt.decode(token, SECRET_KEY, ALGORITHM)
        except (JWTError, ExpiredSignatureError):
            raise AuthenticationException(
                message=MENSAGEM_TOKEN_INVALIDO_EXPIRADO
            )

    @staticmethod
    def create_access_token(data: InputDataToEncode) -> OutputAccessToken:
        access_token = jwt.encode(data.model_dump(), SECRET_KEY, ALGORITHM)
        expiration_datetime = data.exp.strftime(DATETIME_FORMAT)
        return OutputAccessToken(
            access_token=access_token, expires_at=expiration_datetime
        )

    @staticmethod
    async def auth_required(
        token=Depends(CustomJWTBearer()),
    ):
        return token

    # @TODO: Transformar em UseCase Signin
    # @staticmethod
    # async def sign_in(input_signin, db_session) -> OutputAccessToken:
    #     usuario_in_db = await crud.usuario.get(
    #         db_session=db_session, get_by="nm_email", id=input_signin.email
    #     )

    #     if usuario_in_db is None:
    #         raise AuthenticationException(
    #             message=MENSAGEM_CREDENCIAIS_INVALIDAS
    #         )

    #     if not Crypt.verify_secret(input_signin.senha, usuario_in_db.nm_senha):
    #         raise AuthenticationException(
    #             message=MENSAGEM_CREDENCIAIS_INVALIDAS
    #         )

    #     if input_signin.expires_in:
    #         expires_at = datetime.utcnow() + timedelta(
    #             minutes=input_signin.expires_in
    #         )

    #     data_to_encode = InputDataToEncode(
    #         sub=usuario_in_db.nm_email, exp=expires_at
    #     )

    #     token = JWTManager.create_access_token(data_to_encode)

    #     return token

    # @TODO: Transformar em UseCase GetCurrentUser
    # @staticmethod
    # async def get_current_user(
    #     acces_token=Depends(CustomJWTBearer()),
    #     session: AsyncSession = ActiveSession,
    # ) -> Usuario:
    #     try:
    #         data = JWTController.decode_token(acces_token)
    #     except (JWTError, ValidationError):
    #         raise AuthenticationException(
    #             message=MENSAGEM_TOKEN_INVALIDO_EXPIRADO
    #         )

    #     user_name = data["sub"]

    #     current_user = await crud.usuario.get(
    #         db_session=session, get_by="nm_email", id=user_name
    #     )
    #     if not current_user:
    #         raise AuthenticationException(
    #             message=MENSAGEM_CREDENCIAIS_INVALIDAS
    #         )

    #     return CurrentUser(
    #         cd_usuario=current_user.cd_usuario,
    #         email=current_user.nm_email,
    #         nome=current_user.nm_usuario,
    #     )
