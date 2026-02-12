from fastapi import FastAPI
from app.core.settings import settings
from app.db.health import router as db_health_router
from app.modules.auth.router import router as auth_router
from redis.asyncio import Redis

app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME} server is running..."}

app.include_router(db_health_router)
app.include_router(auth_router)


# for redis
@app.on_event("startup")
async def startup():
    app.state.redis = await Redis(host='localhost', port='6379')


@app.on_event("shutdown")
async def shutdown():
    await app.state.redis.close()


@app.get("/redis_set")
async def redis_set():
    await app.state.redis.set("test", "test")
    return {"message": "test"}


@app.get("/redis_get")
async def redis_get():
    result = await app.state.redis.get("test")
    return {"message": result}

