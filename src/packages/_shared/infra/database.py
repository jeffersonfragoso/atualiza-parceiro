from functools import lru_cache

from sqlalchemy import create_engine
from sqlalchemy.engine.mock import MockConnection
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from src.config import get_settings
from src.packages._shared.infra.orm import Base


def factory_default_engine() -> MockConnection:
    engine = create_engine(
        url=get_settings().db_url,
        isolation_level="REPEATABLE READ",
    )
    Base.metadata.create_all(engine)
    return engine


def factory_default_session(engine=None) -> Session:
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )


class Database:
    def __init__(
        self,
        factory_engine=factory_default_engine,
        factory_session=factory_default_session,
    ) -> None:
        self._factory_engine = factory_engine
        self._factory_session = factory_session
        self._engine: None

    def init_db(self) -> MockConnection:
        self._engine = self._factory_engine()

    def get_session(self) -> Session:
        session = self._factory_session(self._engine)()
        return session


@lru_cache
def factory_sqlite_db() -> MockConnection:
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    return engine
