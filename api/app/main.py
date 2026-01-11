from fastapi import FastAPI

from app.routers.env import router as env_router
from app.routers.harvest import router as harvest_router
from app.routers.health import router as health_router

app = FastAPI(title="Heartful API")


app.include_router(health_router)
app.include_router(harvest_router)
app.include_router(env_router)
