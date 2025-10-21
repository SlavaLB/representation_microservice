from fastapi import APIRouter, Header
router = APIRouter(prefix='/math_model')


@router.post(
    "/number_in_math_model",
    summary="Получает число и умножает его на 2",
)
async def get_number_in_math_model(
        number: int = Header(...)
):
    return number * 2
