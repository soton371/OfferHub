from fastapi import FastAPI
from app.core.settings import settings
from app.db.health import router as db_health_router
from app.modules.user.router import router as user_router
from app.modules.common.router import router as common_router
from redis.asyncio import Redis

app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"{settings.APP_NAME} server is running..."}

app.include_router(db_health_router)
app.include_router(user_router)
app.include_router(common_router)

