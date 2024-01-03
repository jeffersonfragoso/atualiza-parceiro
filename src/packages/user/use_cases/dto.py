from datetime import datetime
from typing import Dict, Optional

from fastapi import Depends
from pydantic import BaseModel

from src.packages._shared.infra.auth import Jwt


class UserDto:
    class InputNewUser(BaseModel):
        user_name: str
        password: str

    class OutputUser(BaseModel):
        data: Dict
        user_id: Optional[str] = None
        user_name: Optional[str] = None

    class InputSignIn(BaseModel):
        username: str
        senha: str

    class InputDataToEncode(BaseModel):
        sub: str
        exp: datetime

    class OutputSignIn(BaseModel):
        access_token: str
        expires_at: str
        token_type: str = "bearer"

    class InputCurrentUser(BaseModel):
        access_token: str = Depends(Jwt.auth_required)
