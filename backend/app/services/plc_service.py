from fastapi import Depends
from app.config.depends import get_plc_client


class PLCService:
    def __init__(self, client=Depends(get_plc_client)):
        self.client = client

    async def send_command(self, number: int) -> int:
        """Отправляет число в PLC service и возвращает ответ"""
        response = await self.client.post("/command_in_backend", headers={"number": str(number)})
        return response.json()
