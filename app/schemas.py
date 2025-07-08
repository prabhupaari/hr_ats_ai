from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class JDCreate(BaseModel):
    title: str
    description: str

class JDOut(JDCreate):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
