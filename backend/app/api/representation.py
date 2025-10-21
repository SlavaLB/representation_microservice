from fastapi import APIRouter, Depends, Header

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logger import logger
from app.config.settings import settings

from app.config.db import get_async_session

from app.models import ModelAnswer

router = APIRouter(prefix='/representation')


@router.post(
    "/get_number_in_math_model",
    summary="Получает число, передает в мат модель, возвращает ответ",
)
async def get_number_in_math_model(
        number: int = Header(...),
        session: AsyncSession = Depends(get_async_session)
):
    try:
        logger.info("Вызван эндпоинт get_number_in_math_model")

        # Создаем новую запись в БД
        model_answer = ModelAnswer(number=number)

        # Добавляем в сессию
        session.add(model_answer)

        # Сохраняем в БД
        await session.commit()

        # Обновляем объект чтобы получить ID и created_at
        await session.refresh(model_answer)

        logger.info(
            "Создана запись в БД",
            record_id=model_answer.id,
            number=model_answer.number,
            created_at=model_answer.created_at
        )

        return {
            "message": "Число успешно сохранено в БД",
            "record_id": model_answer.id,
            "number": model_answer.number,
            "created_at": model_answer.created_at.isoformat()
        }

    except Exception as e:
        logger.error(
            "Ошибка get_number_in_math_model: %s", repr(e),
        )
        return {
            'message': 'Ошибка get_number_in_math_model',
            'detail': str(e)
        }
