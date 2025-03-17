from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

from src import models
from src.database import get_db
import src.schemas.book as schema


router = APIRouter()


@router.post("/", response_model=schema.Book)
def create_book(book: schema.BookCreate, db: Session = Depends(get_db)):
    """Creates a new book entity"""

    try:
        db_book = models.Book(**book.model_dump())
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args)
    return db_book


@router.get("/", response_model=list[schema.Book])
def get_books(db: Session = Depends(get_db)):
    """Retrieves all books from the database"""

    return db.query(models.Book).all()


@router.get("/{book_id}", response_model=schema.BookDetails)
def get_book(book_id: str, db: Session = Depends(get_db)):
    """Retrieves a book by id"""

    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.put("/{book_id}", response_model=schema.Book)
def update_book(
    book_id: str, book_update: schema.BookUpdate, db: Session = Depends(get_db)
):
    """Updates a particular book"""

    db_book = db.query(models.Book).filter(models.Book.id == book_id)
    book = db_book.first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db_book.update(book_update.model_dump(exclude_unset=True))
    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}")
def delete_book(book_id: str, db: Session = Depends(get_db)):
    """Deletes a book from the database"""

    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.available:
        raise HTTPException(status_code=400, detail="Book is currently rented out")

    db.delete(book)
    db.commit()
    return {"message": "Book deleted successfully"}


@router.put("/{book_id}/rental/{user_id}", response_model=schema.Book)
def rent_book(book_id: str, user_id: str, db: Session = Depends(get_db)):
    """Creates a rental entity with given book and user ids"""

    db_book = db.query(models.Book).filter(models.Book.id == book_id)
    book = db_book.first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if not book.available:
        raise HTTPException(status_code=400, detail="Book is already borrowed")

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_rental = models.Rental(user_id=user_id, book_id=book_id)
    db.add(db_rental)

    db_book.update({"available": False})
    db.commit()
    db.refresh(book)
    return book


@router.put("/{book_id}/return", response_model=schema.Book)
def return_book(book_id: str, db: Session = Depends(get_db)):
    """Updates book availability and rental status"""

    db_book = db.query(models.Book).filter(models.Book.id == book_id)
    book = db_book.first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    if book.available:
        raise HTTPException(status_code=400, detail="Book is already available")

    db_rental = db.query(models.Rental).filter(
        models.Rental.book_id == book_id and models.Rental.active
    )
    rental = db_rental.first()
    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    db_book.update({"available": True})
    db_rental.update({"active": False})
    db.commit()
    db.refresh(book)
    return book
