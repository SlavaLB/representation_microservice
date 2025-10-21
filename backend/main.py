from fastapi import FastAPI

from app.api import representation_router, logs_router

app = FastAPI(
    root_path="/api",
    title="Документация по Backend",
    description="Общее описание продукта",
    version="1.0.0",
)

app.include_router(
    representation_router,
    prefix="/representation",
    tags=["Representation"]
)

app.include_router(
    logs_router,
    prefix="/logs",
    tags=["Logs"]
)
