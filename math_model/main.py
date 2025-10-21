from fastapi import FastAPI

from app.api import math_router

app = FastAPI()

app.include_router(
    math_router,
    tags=["math_algorithm"]
)
