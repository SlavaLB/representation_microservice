from fastapi import APIRouter, Depends, Header

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.client import get_math_client, get_plc_client
from app.config.logger import logger

from app.config.db import get_async_session

from app.models import ModelAnswer

router = APIRouter()


@router.post(
    "/get_number_in_math_model",
    summary="Получает число, передает в мат модель, возвращает ответ",
)
async def get_number_in_math_model(
        number: int = Header(...),
        session: AsyncSession = Depends(get_async_session),
        math_client=Depends(get_math_client),
        plc_client=Depends(get_plc_client)
):
    try:
        logger.info("Вызван эндпоинт get_number_in_math_model")

        result = await math_client.post("/number_in_math_model", headers={"number": str(number)})
        answer = result.json()
        logger.info(f"Ответ от эндпоинта модели number_in_math_model: {answer}")

        # Создаем новую запись в БД
        model_answer = ModelAnswer(
            number=number,
            model_answer=answer
        )

        session.add(model_answer)
        await session.commit()
        await session.refresh(model_answer)

        logger.info(
            "Создана запись в БД",
            record_id=model_answer.id,
            number=model_answer.number,
            model_answer=model_answer.model_answer,
            created_at=model_answer.created_at
        )

        result = await plc_client.post("/command_in_backend", headers={"number": str(answer)})
        answer = result.json()

        return {
            "message": "Число успешно сохранено в БД",
            "model_answer": model_answer.model_answer,
            "plc_answer": answer

        }

    except Exception as e:
        return {
            'message': 'Ошибка get_number_in_math_model',
            'detail': str(e)
        }
