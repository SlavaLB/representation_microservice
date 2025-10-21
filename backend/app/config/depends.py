import httpx
from fastapi import Depends

from app.config.db import AsyncSessionLocal
from app.config.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession

from app.services_bd.model_answer_service import ModelAnswerService


async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session


async def get_math_client():
    """Зависимость: создаёт httpx.AsyncClient, передает его в MathClient и закрывает после."""
    async with httpx.AsyncClient(base_url=f"{settings.base_url_math_model}") as math_client:
        yield math_client


async def get_plc_client():
    """Зависимость: создаёт httpx.AsyncClient, передает его в MathClient и закрывает после."""
    async with httpx.AsyncClient(base_url=f"{settings.base_url_plc_model}") as plc_client:
        yield plc_client


async def get_model_answer_db_service(
    session: AsyncSession = Depends(get_async_session)
) -> ModelAnswerService:
    return ModelAnswerService(session)
