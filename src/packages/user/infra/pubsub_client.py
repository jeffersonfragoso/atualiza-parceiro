import abc
from collections.abc import Iterator

class AbstractPubSubClient(abc.ABC):
    @abc.abstractmethod
    def get_save_user_messages(self) -> Iterator[dict]:
        raise NotImplementedError

    @abc.abstractmethod
    def notify_email_changed(self, user_id: str, new_email: str, old_email: str) -> None:
        raise NotImplementedError


class InMemoryPubSubClient(AbstractPubSubClient):
    def __init__(self):
        super().__init__()
        self.commands: list[dict] = []
        self.commit_called = False
        self.commit_should_fail = False
        self.email_sent = False
        self.notify_email_set_called = False
        self.notify_email_set_failed = False
        self.notify_email_set_should_fail = False
        self.notify_kpi_called = False
        self.kpi_event: KpiEvent | None = None
        self.rollback_called = False
        self.rollback_should_fail = False
        self.kpi_event_sent = False

    def _get_save_user_messages(self) -> Iterator[dict]:
        yield from (command for command in self.commands)

    def _notify_kpi_service(self, event: KpiEvent) -> None:
        self.notify_kpi_called = True
        self.kpi_event = event

    def _notify_email_changed(self, user_id: str, new_email: str, old_email: str) -> None:
        self.notify_email_set_called = True
        if self.notify_email_set_should_fail:
            raise Exception('notify failed')
        self.notify_email_set_user_id = user_id
        self.notify_email_set_new_email = new_email
        self.notify_email_set_old_email = old_email

    def commit(self) -> None:
        self.commit_called = True
        if self.commit_should_fail:
            raise Exception('commit failed')
        if self.notify_email_set_called:
            self.email_sent = True
        if self.notify_kpi_called:
            self.kpi_event_sent = True

    def rollback(self) -> None:
        self.rollback_called = True
        if self.rollback_should_fail:
            raise Exception('rollback failed')
