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

#Async learning. Test Endpoints.
@app.get("/async-test")
async def async_test():

    await asyncio.sleep(5)

    return {"message": "Async worked"}

@app.get("/sync-test")
def sync_test():
    time.sleep(5)
    return {"message": "Sync worked"}

@app.get("/coroutine-test")
async def coroutine_test():

    async def greet():

        return "hello"

    result = await greet()

    return {

        "result": str(result)

    }

@app.get("/gather-test")
async def gather_test():
    result = []
    async def task1():
        await asyncio.sleep(5)
        return "task1 done"
    async def task2():
        await asyncio.sleep(5)
        return "task2 done"
    # results = await asyncio.gather(
    #     task1(),
    #     task2()
    # )
    result.append(await task1())
    result.append(await task2())
    return {"results": result}

@app.get("/task-test")
async def task_test():
    async def bg_task():
        print("task started")
        await asyncio.sleep(2)
        raise Exception("task failed")
    asyncio.create_task(bg_task())
    return {"result": "Request returned"}

@app.get("/cancel-test")
async def cancel_test():
    async def worker():
        try:
            print("worker started")
            await asyncio.sleep(10)
            print("worker finished")
        except asyncio.CancelledError:
            print("worker cancelled")
            raise
    task = asyncio.create_task(worker())
    await asyncio.sleep(2)
    task.cancel()
    return {"message": "task cancelled"}

@app.get("/switch-test")
async def switch_test():
    async def worker(name):
        print(f"worker {name} started")
        await asyncio.sleep(10)
        print(f"worker {name} finished")
    await asyncio.gather(worker("A"), worker("B"))
    return {"message": "finished"}

@app.get("/timeout-test")
async def timeout_test():
    async def slow_task():
        await asyncio.sleep(10)
        return "slow_task finished"
    try:
        result = await asyncio.wait_for(slow_task(), timeout=3)
    except asyncio.TimeoutError:
        return {"error": "Task timed out"}