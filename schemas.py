from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import date
from typing import Optional

class FoodLogCreate(BaseModel):
    food: str = Field(..., min_length=1, max_length=1000)
    calories: float = Field(..., ge=0, le=2000)
    protein: float = Field(..., ge=0)
    fiber: float = Field(..., ge=0)
    date: date
    @field_validator("date")
    def date_not_in_future(cls, v):
        if v > date.today():
            raise ValueError("Date cannot be in the future")
        return v

class FoodLogRead(BaseModel):
    id: int
    food: str
    calories: float
    protein: float
    fiber: float
    date: date
    model_config = ConfigDict(from_attributes=True)

class FoodLogUpdate(BaseModel):
    food: Optional[str] = Field(None, min_length=1, max_length=1000)
    calories: Optional[float] = Field(None, ge=0, le=2000)
    protein: Optional[float] = Field(None, ge=0)
    fiber: Optional[float] = Field(None, ge=0)
    date: Optional[date] = None

    @field_validator("date")
    def date_not_in_future(cls, v):
        if v and v > date.today():
            raise ValueError("Date cannot be in the future")
        return v

class UserCreate(BaseModel):
    email: str
    password: str

class UserRead(BaseModel):
    id: int
    email: str

    model_config = ConfigDict(from_attributes=True)


# class FoodLog(BaseModel):
#     food: str
#     calories: float
#     protein: float
#     fiber: float
#     date: date