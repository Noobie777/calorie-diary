from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import crud
from database import SessionLocal
from schemas import UserCreate, UserRead


router = APIRouter()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup", response_model = UserRead)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)