from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime, UTC

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True,index=True)
    food = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    fiber = Column(Float)
    date = Column(Date)
    user_id = Column(Integer, ForeignKey("users.id"),index=True )
    owner = relationship("User", back_populates="logs")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String,nullable=False)
    logs = relationship("Log", back_populates="owner")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    revoked = Column(Boolean,default=False)
    created_at = Column(Date,default=datetime.now(UTC))