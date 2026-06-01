from fastapi import FastAPI
from database import engine
import models
from routes import logs, users
import asyncio
import time
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from limiter import limiter

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(logs.router)
app.include_router(users.router)

#Rate Limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
