from pydantic import BaseModel
from datetime import datetime


class ActorCreate(BaseModel):
    first_name: str
    last_name: str
    # last_update: datetime


class ActorSchema(BaseModel):
    actor_id: int
    first_name: str
    last_name: str
    last_update: datetime

    class Config:
        from_attributes = True