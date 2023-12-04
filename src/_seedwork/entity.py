from abc import ABC
from typing import List
from uuid import uuid4

from pydantic import Field
from src._seedwork.event import Event
from src._seedwork.base_model import CustomModel


class Entity(ABC, CustomModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    events: List[Event] = Field(default_factory=lambda: [])

    def to_dict(self):
        entity_dict = self.model_dump()
        return entity_dict

    def notify_domain_event(self, event: Event):
        print(f'Evento de domínio ocorrido: {event.name}:{event.id}')
        self.events.append(event)
