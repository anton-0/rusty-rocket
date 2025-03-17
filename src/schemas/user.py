from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from src.schemas.rental import RentalUser


class User(BaseModel):
    id: str
    name: str

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    id: str
    name: str


class UserUpdate(BaseModel):
    name: Optional[str] = None


class UserDetails(User):
    rentals: List[RentalUser] = []
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
