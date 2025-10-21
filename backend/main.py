from fastapi import FastAPI

from app.api import representation_router, logs_router

app = FastAPI()

app.include_router(
    representation_router,
    tags=["Representation"]
)

app.include_router(
    logs_router,
    tags=["Logs"]
)
