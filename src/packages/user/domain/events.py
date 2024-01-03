import datetime

from src._seedwork.event import Event


class UserCreatedEvent(Event):
    user_name: str = None
    password_hash: str = None
    created_at: datetime.datetime = None
