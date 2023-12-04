from passlib.context import CryptContext


class WrongPassword(Exception):
    pass


class Crypt:

  ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

  @classmethod
  def encrypt_secret(cls, secret: str) -> str:
      return cls.ctx.hash(secret)

  @classmethod
  def verify_secret(cls, secret: str, encrypted_secret: str) -> bool:
      correct_password = cls.ctx.verify(secret, encrypted_secret)
      if not correct_password:
          raise WrongPassword("Wrong Password")
