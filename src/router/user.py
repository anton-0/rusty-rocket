from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, APIRouter

from src import models
from src.database import get_db
import src.schemas.user as user

router = APIRouter()


@router.post("/", response_model=user.User)
def create_user(user: user.UserCreate, db: Session = Depends(get_db)):
    """Creates a new user entity"""

    try:
        db_user = models.User(**user.model_dump())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=e.args)
    return db_user


@router.get("/", response_model=list[user.User])
def get_users(db: Session = Depends(get_db)):
    """Retrieves all users from the database"""

    return db.query(models.User).all()


@router.get("/{user_id}", response_model=user.UserDetails)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """Retrieves a user by id"""

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=user.User)
def update_user(
    user_id: str, user_update: user.UserUpdate, db: Session = Depends(get_db)
):
    """Updates a particular user"""

    db_user = db.query(models.User).filter(models.User.id == user_id)
    user = db_user.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db_user.update(user_update.model_dump(exclude_unset=True))

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    """Deletes a user from the database"""

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user_rentals = db.query(models.Rental).filter(models.Rental.user_id == user_id)
    if user_rentals:
        raise HTTPException(status_code=400, detail="User is currently renting a book")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
