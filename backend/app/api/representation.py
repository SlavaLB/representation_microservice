from fastapi import APIRouter, Depends, Header

from app.config.depends import get_model_answer_db_service
from app.config.logger import logger
from app.services import MathService, PLCService

router = APIRouter()


@router.post(
    "/get_number_in_math_model",
    summary="Получает число, передает в мат модель, возвращает ответ",
)
async def get_number_in_math_model(
        number: int = Header(...),
        math_services=Depends(MathService),
        plc_services=Depends(PLCService),
        model_answer_db_service=Depends(get_model_answer_db_service)
):
    try:
        logger.info("Вызван эндпоинт get_number_in_math_model")

        answer_in_model = await math_services.send_number(number)
        logger.info(f"Ответ от эндпоинта модели number_in_math_model: {answer_in_model}")

        # Создаем новую запись в БД
        model_answer = await model_answer_db_service.save_answer(
            number=number,
            model_answer=answer_in_model
        )

        logger.info(
            "Создана запись в БД",
            record_id=model_answer.id,
            number=model_answer.number,
            model_answer=model_answer.model_answer,
            created_at=model_answer.created_at
        )

        command_in_plc = await plc_services.send_command(number)

        logger.info(f"Команда:{number} была отправлена и {command_in_plc}")
        return {
            "message": "Число успешно сохранено в БД",
            "model_answer": model_answer.model_answer,
            "plc_answer": command_in_plc

        }

    except Exception as e:
        return {
            'message': 'Ошибка get_number_in_math_model',
            'detail': str(e)
        }
