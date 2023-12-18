from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from pydantic import Field

from src._seedwork.base_model import CustomModel

from .event import Event


class Command(ABC, CustomModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @property
    def name(self) -> str:
        return type(self).__name__

    def to_dict(self):
        return self.model_dump()


class CommandExecutor(ABC, CustomModel):
    events: List[Event] = Field(default_factory=lambda: [])

    def execute(self, command: Command):
        raise NotImplementedError

    def set_events(self, entity_events: List):
        print("Repassando evento de dominio")
        self.events.extend(entity_events)

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
