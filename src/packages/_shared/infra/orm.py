from sqlalchemy import event, Column, DateTime, String
from sqlalchemy.orm import declarative_base

# from src.packages.user.domain import entities

Base = declarative_base()


class User(Base):
  __tablename__ = 'users'

  id = Column("id", String, primary_key=True, autoincrement=False)
  user_name = Column("user_name", String, nullable=False, unique=True)
  password_hash = Column("password_hash", String, nullable=False)
  created_at = Column("created_at", DateTime, nullable=False)

