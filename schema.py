from pydantic import BaseModel
from datetime import datetime


class AccountCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str


class AccountSchema(BaseModel):
    actor_id: int
    first_name: str
    last_name: str
    username: str
    
    class Config:
        from_attributes = True
        
        
class CurrentAccountSchema(BaseModel):
    actor_id: int
    first_name: str
    last_name: str
    username: str
    last_update: datetime
    hashed_password: str
    is_admin: bool
    
    class Config:
        from_attributes = True