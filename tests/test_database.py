from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(bind=engine)

def override_get_db():
    print("Using Test DB")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
