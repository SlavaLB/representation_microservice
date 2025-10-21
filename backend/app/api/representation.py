from fastapi import APIRouter, Depends, Header

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.logger import logger
# from app.config.db import get_async_session


router = APIRouter(prefix='/representation')


@router.post(
    "/get_number_in_math_model",
    summary="Получает число, передает в мат модель, возвращает ответ",
)
async def get_number_in_math_model(
        number: int = Header(...),
        # session: AsyncSession = Depends(get_async_session)
):
    try:
        logger.info("Вызван эндпоинт get_number_in_math_model")

        return {"message": "Запись о трудозатратах успешно удалена"}

    except Exception as e:
        logger.error(
            "Ошибка get_number_in_math_model: %s", repr(e),
        )
        return {
            'message': 'Ошибка get_number_in_math_model',
            'detail': str(e)
        }
