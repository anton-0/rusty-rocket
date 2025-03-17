import re

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, TIMESTAMP
from sqlalchemy.orm import relationship, DeclarativeBase, validates
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id = Column(String(6), primary_key=True, unique=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    available = Column(Boolean, default=True)

    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    rental = relationship("Rental", back_populates="book", cascade="all, delete")

    @validates("id")
    def validate_id(self, key, value):
        """Ensures that ID has 6 digits."""
        if not re.fullmatch(r"\d{6}", value):
            raise ValueError("Book ID must be exactly 6 digits.")
        return value


class User(Base):
    __tablename__ = "users"

    id = Column(String(6), primary_key=True, unique=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    rentals = relationship("Rental", back_populates="user", cascade="all, delete")

    @validates("id")
    def validate_id(self, key, value):
        """Ensures that ID has 6 digits."""
        if not re.fullmatch(r"\d{6}", value):
            raise ValueError("User ID must be exactly 6 digits.")
        return value


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    book_id = Column(String, ForeignKey("books.id", ondelete="CASCADE"), nullable=True)
    active = Column(Boolean, default=True, nullable=False)
    rental_date = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=func.now()
    )
    return_date = Column(TIMESTAMP(timezone=True), default=None, onupdate=func.now())

    user = relationship("User", back_populates="rentals")
    book = relationship("Book", back_populates="rental")
