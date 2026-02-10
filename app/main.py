from fastapi import FastAPI
from app.core.settings import settings
from app.db.health import router as db_health_router
from app.modules.auth.router import router as auth_router

app = FastAPI()


@app.get("/")
async def root():
    return {"message": f"Hello World {settings.APP_NAME}"}

app.include_router(db_health_router)
app.include_router(auth_router)
