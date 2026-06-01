from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import crud
from database import SessionLocal,get_db
from schemas import FoodLogCreate, FoodLogRead, FoodLogUpdate
from authentication.auth import get_current_user
from models import User
from datetime import date

router = APIRouter()

@router.post("/logs",response_model=FoodLogRead)
def create_log(log: FoodLogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return crud.create_log(db, log,current_user)


@router.get("/logs",response_model=list[FoodLogRead])
def get_logs(skip: int = 0,
             limit: int = 10,
             food: str | None = None,
             min_calories: int | None = None,
             max_calories: int | None = None,
             sort: str = "desc",
             start_date: date | None = None,
             end_date: date | None = None,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    return crud.get_logs(db,current_user,
                         skip,
                         limit,
                         food,
                         min_calories,
                         max_calories,
                         sort,
                         start_date,
                         end_date
                         )


@router.get("/logs/{id}",response_model=FoodLogRead)
def get_log(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    log = crud.get_log(db, id,current_user)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log


@router.delete("/logs/{id}")
def delete_log(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    log = crud.delete_log(db, id, current_user)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return {"message": "Log deleted"}

@router.put("/logs/{id}",response_model=FoodLogRead)
def update_log(id:int, updated_log: FoodLogCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    log = crud.update_log(db, id, updated_log,current_user)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log

@router.patch("/logs/{id}",response_model=FoodLogRead)
def patch_log(id: int, updated_log: FoodLogUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    log = crud.patch_log(db, id, updated_log,current_user)
    if not log:
        raise HTTPException(status_code=404, detail="Log not found")
    return log