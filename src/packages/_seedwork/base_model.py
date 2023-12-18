from pydantic import BaseModel


class CustomModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
