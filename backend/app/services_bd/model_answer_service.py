from app.models import ModelAnswer
from app.services_bd.base import BaseService


class ModelAnswerService(BaseService):
    @property
    def model(self):
        return ModelAnswer

    async def save_answer(self, number: int, model_answer: int):
        return await self.create(number=number, model_answer=model_answer)
