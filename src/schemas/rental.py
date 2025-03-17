from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class RentalCreate(BaseModel):
    user_id: str
    book_id: str


class Rental(BaseModel):
    id: int
    active: bool
    rental_date: Optional[datetime]
    return_date: Optional[datetime]

    class Config:
        orm_mode = True


class RentalBook(Rental):
    user_id: str


class RentalUser(Rental):
    book_id: str
