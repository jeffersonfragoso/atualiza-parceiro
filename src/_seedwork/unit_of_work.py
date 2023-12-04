from abc import ABC
from types import TracebackType
from typing import Type

from src._seedwork.command import Command, CommandExecutor
from src._seedwork.event import Event, EventExecutor


class CommandUnitOfWork(ABC):
    def __init__(self, command: Command, executor: CommandExecutor):
        self._executor = executor
        self._command = command
        self.result =  None

    def __enter__(self):
        self.result = self._executor.execute(self._command)
        return self

    def __exit__(self, exc_type: Type, exc_val: Exception, exc_tb: TracebackType) -> bool | None:
        if exc_val:
            self._executor.rollback()
        else:
            self._executor.commit()

class EventUnitOfWork(ABC):
    def __init__(self, event: Event, executor: EventExecutor):
        self._executor = executor
        self._event = event
        self.result =  None

    def __enter__(self):
        self.result = self._executor.execute(self._event)
        return self

    def __exit__(self, exc_type: Type, exc_val: Exception, exc_tb: TracebackType) -> bool | None:
        if exc_val:
            self._executor.rollback()
        else:
            self._executor.commit()
