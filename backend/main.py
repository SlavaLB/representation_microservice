from fastapi import FastAPI

from app.api import representation_router, logs_router

app = FastAPI(root_path="/api")

app.include_router(
    representation_router,
    prefix="/api/representation",
    tags=["Representation"]
)

app.include_router(
    logs_router,
    prefix="/api/logs",
    tags=["Logs"]
)
