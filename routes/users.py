from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from database import SessionLocal,get_db
from models import User
from schemas import UserCreate, UserRead, Token, RefreshToken, LogoutRequest
from fastapi.security import OAuth2PasswordRequestForm
from authentication.auth import create_access_token, get_current_user, create_refresh_token,refresh_token_verification
router = APIRouter()


@router.post("/signup", response_model = UserRead)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.post("/login", response_model = Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    crud.save_refresh_token(db,refresh_token,user.id)
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.post("/refresh")
def refresh_token(request: RefreshToken, db: Session = Depends(get_db)):
    email = refresh_token_verification(request.refresh_token,db)
    crud.revoke_refresh_token(db, request.refresh_token)
    new_refresh_token = create_refresh_token(data={"sub": email})
    user = crud.get_user_by_email(db, email)
    crud.save_refresh_token(db,new_refresh_token,user.id)
    new_access_token = create_access_token(data={"sub": email})
    return {"access_token": new_access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}

@router.post("/logout")
def logout(request: LogoutRequest, db: Session = Depends(get_db)):
    refresh_token_verification(request.refresh_token,db)
    crud.revoke_refresh_token(db, request.refresh_token)
    return {"message": "Logged out successfully"}