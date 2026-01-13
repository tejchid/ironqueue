from pydantic import BaseModel
from typing import Any

class JobCreate(BaseModel):
    type: str
    payload: Any
    max_attempts: int = 3

class JobRead(BaseModel):
    id: int
    type: str
    payload: Any
    status: str
    attempts: int
    max_attempts: int

    class Config:
        orm_mode = True
