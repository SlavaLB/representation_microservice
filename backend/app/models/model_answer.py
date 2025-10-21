from sqlalchemy import Column, Integer
from app.models.base import BaseModel


class ModelAnswer(BaseModel):
    __tablename__ = "model_answers"

    number = Column(Integer, nullable=False)
    model_answer = Column(Integer, nullable=False)
