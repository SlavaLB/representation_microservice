from fastapi import FastAPI

from app.api import plc_router

app = FastAPI(
    root_path="/plc",
    title="Документация по PLC service",
    description="Общее описание продукта",
    version="1.0.0",
)

app.include_router(
    plc_router,
    tags=["PLCservice"]
)
