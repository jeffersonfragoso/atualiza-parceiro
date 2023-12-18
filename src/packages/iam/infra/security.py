from datetime import datetime, timedelta

from fastapi import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from src._seedwork.exceptions import AuthenticationException
from src.config import get_settings
from src.packages._shared.infra.crypt import Crypt

ALGORITHM = get_settings().algorithm
SECRET_KEY = get_settings().secret_key


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return Crypt.verify_secret(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return Crypt.encrypt_secret(password)


def create_access_token(subject: dict, expires_delta: timedelta = None) -> (str, str):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=get_settings().access_token_expire_minutes)
    payload = {"exp": expire, **subject}
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    expiration_datetime = expire.strftime(get_settings().datetime_format)
    return encoded_jwt, expiration_datetime


def decode_jwt(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        return (
            decoded_token
            if decoded_token["exp"] >= int(round(datetime.utcnow().timestamp()))
            else None
        )
    except Exception as e:
        return {}


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise AuthenticationException(message="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise AuthenticationException(message="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise AuthenticationException(message="Invalid authorization code.")

    def verify_jwt(self, jwt_token: str) -> bool:
        is_token_valid: bool = False
        try:
            payload = decode_jwt(jwt_token)
        except Exception as e:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid
