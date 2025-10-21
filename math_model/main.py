from fastapi import FastAPI

from app.api import math_router

app = FastAPI(
    root_path="/math",
    title="Документация по Math model",
    description="Общее описание продукта",
    version="1.0.0",
)

app.include_router(
    math_router,
    tags=["math_algorithm"]
)
