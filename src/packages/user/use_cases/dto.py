from typing import Dict, Optional

from pydantic import BaseModel


class UserDto:
    class InputNewUser(BaseModel):
        user_name: str
        password: str

    class OutputNewUser(BaseModel):
        data: Dict
        user_id: Optional[str] = None
        user_name: Optional[str] = None
