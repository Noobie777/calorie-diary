from sqlalchemy import Column, Integer, String, Float, Date
from database import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True,index=True)
    food = Column(String)
    calories = Column(Float)
    protein = Column(Float)
    fiber = Column(Float)
    date = Column(Date)