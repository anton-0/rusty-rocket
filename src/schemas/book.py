from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from src.schemas.rental import RentalBook


class Book(BaseModel):
    id: str
    title: str
    author: str
    available: bool

    class Config:
        orm_mode = True


class BookCreate(BaseModel):
    id: str
    title: str
    author: str


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None


class BookDetails(Book):
    rental: List[RentalBook] = []
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
