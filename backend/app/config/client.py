import httpx
from app.config.settings import settings


async def get_math_client():
    """Зависимость: создаёт httpx.AsyncClient, передает его в MathClient и закрывает после."""
    async with httpx.AsyncClient(base_url=f"{settings.base_url_math_model}") as client:
        yield client
