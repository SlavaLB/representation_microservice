from fastapi import APIRouter, Header
router = APIRouter()


@router.post(
    "/number_in_math_model",
    summary="Получает число и умножает его на 2",
)
async def get_number_in_math_model(
        number: int = Header(...)
):
    return number * 2
