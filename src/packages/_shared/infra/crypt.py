from passlib.context import CryptContext

from src._seedwork.exceptions import AuthenticationException


class Crypt:
    ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def encrypt_secret(cls, secret: str) -> str:
        return cls.ctx.hash(secret)

    @classmethod
    def verify_secret(cls, secret: str, encrypted_secret: str) -> bool:
        correct_secret = cls.ctx.verify(secret, encrypted_secret)
        if not correct_secret:
            raise AuthenticationException("Credenciais inválidas")
        return correct_secret
