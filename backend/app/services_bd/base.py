from abc import ABC, abstractmethod
from typing import Type, TypeVar
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta

T = TypeVar("T", bound=DeclarativeMeta)


class BaseService(ABC):
    """Абстрактный сервис для работы с одной моделью"""

    def __init__(self, session: AsyncSession):
        self.session = session

    @property
    @abstractmethod
    def model(self) -> Type[T]:
        """Модель SQLAlchemy, с которой работает сервис"""
        ...

    async def create(self, **kwargs) -> T:
        """Создает запись в БД"""
        obj = self.model(**kwargs)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj

    async def get_by_id(self, id: int) -> T or None:
        return await self.session.get(self.model, id)

    async def delete(self, obj: T):
        await self.session.delete(obj)
        await self.session.commit()

    async def update(self, obj: T, **kwargs) -> T:
        for key, value in kwargs.items():
            setattr(obj, key, value)
        self.session.add(obj)
        await self.session.commit()
        await self.session.refresh(obj)
        return obj
