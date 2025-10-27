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
        logger.info("###################################")
        logger.info("###################################")
        logger.info("Вызван эндпоинт get_number_in_math_model")

        logger.info(f"Передаем данные в математическую модель send_number({number})")
        answer_in_model = await math_services.send_number(number)
        logger.info(f"Ответ от модели: {answer_in_model}")

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
        logger.info(f"Передаем ответ от модели в PLCservice: {answer_in_model}")
        command_in_plc = await plc_services.send_command(answer_in_model)
        logger.info(f"Ответ от PLCservice: {command_in_plc}")
        logger.info("###################################")
        logger.info("###################################")
        return {
            "message": "Команда успешно сохранена в БД",
            "model_answer": f"Ответ от модели: {model_answer.model_answer}",
            "plc_answer": f"Ответ от PLCservice: {command_in_plc}"

        }

    except Exception as e:
        return {
            'message': 'Ошибка get_number_in_math_model',
            'detail': str(e)
        }
