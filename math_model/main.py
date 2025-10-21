from fastapi import FastAPI

from app.api import math_router

app = FastAPI(root_path="/math")

app.include_router(
    math_router,
    tags=["math_algorithm"]
)
