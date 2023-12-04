from abc import ABC, abstractmethod
from datetime import datetime, timezone
from typing import List
from uuid import uuid4

from pydantic import Field
from src._seedwork.base_model import CustomModel

class Event(ABC, CustomModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    created_at: datetime = Field(
      default_factory=lambda: datetime.now(timezone.utc)
    )

    @property
    def name(self) -> str:
      return type(self).__name__

    def to_dict(self):
      return self.model_dump()


class EventExecutor(ABC, CustomModel):
  events: List[Event] = Field(default_factory=lambda: [])

  def execute(self, event: Event):
      raise NotImplementedError

  def set_events(self, events: List):
    self.events.extend(events)

  @abstractmethod
  def commit(self) -> None:
    raise NotImplementedError

  @abstractmethod
  def rollback(self) -> None:
    raise NotImplementedError
