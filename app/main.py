from fastapi import FastAPI
from core.settings import settings
from db.health import router as db_health_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"Hello World {settings.APP_NAME}"}

app.include_router(db_health_router)