from fastapi import Depends

from app.config.depends import get_math_client


class MathService:
    def __init__(self, client=Depends(get_math_client)):
        self.client = client

    async def send_number(self, number: int) -> int:
        """Отправляет число в math model и возвращает результат"""
        response = await self.client.post(
            "/number_in_math_model", headers={"number": str(number)}
        )
        return response.json()
