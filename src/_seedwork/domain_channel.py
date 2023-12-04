from __future__ import annotations

import collections
from typing import Deque, Any, Dict

from .command import Command, CommandExecutor
from .event import Event, EventExecutor
from .unit_of_work import CommandUnitOfWork, EventUnitOfWork

class DomainChannel:
    def __init__(
      self,
      commands_catalog: Dict[str, CommandExecutor],
      events_catalog: Dict[str, EventExecutor],
    ):
      self._commands_catalog = commands_catalog
      self._events_catalog = events_catalog
      self._events_to_dispatch: Deque[Event] = collections.deque()

    def dispatch_command(self, command: Command) -> Any:
        executor = self._commands_catalog.get(command.name)
        with CommandUnitOfWork(command, executor) as uow:
            result = uow.result
            self._events_to_dispatch.extend(executor.events)
        self._dispatcher_events()
        return result

    def _dispatcher_events(self) -> None:
        while self._events_to_dispatch:
          event = self._events_to_dispatch.popleft()
          executors = self._events_catalog.get(event.name)
          for executor in executors:
              with EventUnitOfWork(event, executor) as uow:
                  self._events_to_dispatch.extend(executor.events)
