from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True,index=True)
    food = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    fiber = Column(Float)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="logs")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String,nullable=False)
    logs = relationship("Log", back_populates="owner")