from functools import lru_cache
from typing import Any
from src._seedwork.domain_channel import DomainChannel
from src.packages._shared.infra.database import Database

from src.packages.user.infra.repository import SqlAlchemyUserRepository
from src.packages.user.domain.commands import CreateUserCommand
from src.packages.user.domain.entities import UserCreatedEvent
from src.packages.user.use_cases import CreateUserCommandExecutor, UserCreatedEventExecutor
from src.packages._shared.infra.database import Database, factory_sqlite_db


class UserContainer():
  def __init__(self, db: Database) -> None:
    self._db = db

    # Register all dependecies
    self.user_repository  = SqlAlchemyUserRepository(self._db.get_session())

    # Catalog all commands {name: instance}
    self.commands_catalog = {
      'CreateUserCommand' : CreateUserCommandExecutor(user_repository=self.user_repository),
      # Command2().name : CommandExecutor2(dependencias),
      # Command3().name : CommandExecutor3(dependencias),
    }

    # Catalog all events {name: instance}
    self.events_catalog = {
      'UserCreatedEvent' : [UserCreatedEventExecutor()]
      # Event2().name : EventExecutor2(dependencias),
      # Event3().name : EventExecutor3(dependencias),
    }

    self.domain_channel = DomainChannel(self.commands_catalog, self.events_catalog)


def factory_user_container() -> UserContainer:
  db = Database(factory_engine=factory_sqlite_db)
  db.init_db()
  return UserContainer(db)
