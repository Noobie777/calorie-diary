from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
from config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

#DATABASE_URL = os.getenv("DATABASE_URL")
DATABASE_URL = settings.DATABASE_URL

# engine = create_engine(
#     DATABASE_URL,connect_args={"check_same_thread":False}
# )
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()