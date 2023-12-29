from typing import Any, Dict, Optional

from fastapi import status
from pydantic import BaseModel
from starlette.exceptions import HTTPException

from src.packages._shared.messages import (
    MENSAGEM_AUTENTICACAO_REQUERIDA,
    MENSAGEM_CREDENCIAIS_INVALIDAS,
)


class ContentHttpException(BaseModel):
    status_code: int
    message: str


class CustomHTTPException(HTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = None

    def __init__(
        self,
        message: str = None,
        headers: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.message = message or self.message
        self.status_code = self.status_code
        self.detail = self.message
        self.headers = headers

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(status_code={self.status_code!r}, msg={self.message!r})"

    @property
    def content(self):
        return ContentHttpException(
            status_code=self.status_code, message=self.message
        ).model_dump()


class BadRequestException(CustomHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    message = "Bad Request"


class NotFoundException(CustomHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    message = "Not Found"


class AuthenticationException(CustomHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    message = MENSAGEM_CREDENCIAIS_INVALIDAS


class NotAuthenticatedException(CustomHTTPException):
    status_code = status.HTTP_403_FORBIDDEN
    message = MENSAGEM_AUTENTICACAO_REQUERIDA
