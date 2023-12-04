from datetime import datetime, timezone
from typing import Optional

from pydantic import Field

from src._seedwork.entity import Entity
from src.packages.user.domain.events import UserCreatedEvent


class User(Entity):
  user_name: str
  password_hash: str
  created_at: Optional[datetime] = Field(
    default_factory=lambda: datetime.now(timezone.utc)
  )

  def model_post_init(self, __context):
    self.notify_domain_event(
      UserCreatedEvent(user_name=self.user_name, password_hash=self.password_hash)
    )
