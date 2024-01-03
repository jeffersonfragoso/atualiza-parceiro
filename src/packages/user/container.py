from src._seedwork.domain_channel import DomainChannel
from src.packages._shared.infra.database import Database, factory_sqlite_db
from src.packages.user.infra.repository import SqlAlchemyUserRepository
from src.packages.user.use_cases import (
    CreateUserCommandExecutor,
    UserCreatedEventExecutor,
    SignInCommandExecutor,
    GetCurrentUserCommandExecutor,
)


class UserContainer:
    def __init__(self, db: Database) -> None:
        self._db = db

        # Register all dependecies
        self.user_repository = SqlAlchemyUserRepository(self._db.get_session())

        # Catalog all commands {name: instance}
        self.commands_catalog = {
            "CreateUserCommand": CreateUserCommandExecutor(
                user_repository=self.user_repository
            ),
            "SignInCommand": SignInCommandExecutor(
                user_repository=self.user_repository
            ),
            "GetCurrentUserCommand": GetCurrentUserCommandExecutor(
                user_repository=self.user_repository
            ),
        }

        # Catalog all events {name: instance}
        self.events_catalog = {
            "UserCreatedEvent": [UserCreatedEventExecutor()]
            # Event2().name : EventExecutor2(dependencias),
            # Event3().name : EventExecutor3(dependencias),
        }

        self.domain_channel = DomainChannel(
            self.commands_catalog, self.events_catalog
        )


def factory_user_container() -> UserContainer:
    db = Database(factory_engine=factory_sqlite_db)
    db.init_db()
    return UserContainer(db)
