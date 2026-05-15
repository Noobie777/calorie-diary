from fastapi import FastAPI
from database import engine
import models
from routes import logs

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(logs.router)
