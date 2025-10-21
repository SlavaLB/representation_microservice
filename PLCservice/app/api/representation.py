from fastapi import APIRouter, Header
router = APIRouter()


@router.post(
    "/command_in_backend",
    summary="Получает команду и печатает",
)
async def get_number_in_math_model(
        number: int = Header(...)
):
    return "Команда передана на PLC"
