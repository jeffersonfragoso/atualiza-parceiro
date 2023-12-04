from sqlalchemy.orm import Session
from abc import abstractmethod
from src._seedwork.repository import AbstractRepository
from src.packages._shared.infra import orm
from src.packages.user.domain.entities import User


class AbstractUserRepository(AbstractRepository):
    @abstractmethod
    def get_by_user_name(self, id_: str) -> User:
        raise NotImplementedError

    @abstractmethod
    def add(self, user: User) -> None:
        raise NotImplementedError


class InMemoryUserRepository(AbstractUserRepository):
    def __init__(self):
        super().__init__()
        self.users_by_user_name: dict[str, User] = {}
        self._saved_users: list[User] = []
        self.commit_called = False
        self.rollback_called = False
        self.commit_should_fail = False
        self.rollback_should_fail = False

    def get_by_user_name(self, user_name: str) -> User:
        result = self.users_by_user_name.get(user_name)
        return result

    def add(self, user: User) -> None:
        self._saved_users.append(user)

    def commit(self) -> None:
        self.commit_called = True
        if self.commit_should_fail:
            raise Exception('commit failed')
        for user in self._saved_users:
            self.users_by_user_name[user.id] = user

    def rollback(self) -> None:
        self.rollback_called = True
        if self.rollback_should_fail:
            raise Exception('rollback failed')
        self._saved_users.clear()


class SqlAlchemyUserRepository(AbstractUserRepository):
    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def add(self, user: User):
        print("Adicionando Usuario")
        self.session.add(self.to_orm(user))

    def delete(self, user: User):
        self.session.delete(self.to_orm(user))

    def get_by_user_name(self, user_name: str) -> User:
        user = self.session.query(orm.User).filter_by(user_name=user_name).first()
        return user

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()

    def to_orm(self, entity: User):
        _entity = entity.model_copy(deep=True).to_dict()
        _entity.pop('events')
        return orm.User(**(_entity))
