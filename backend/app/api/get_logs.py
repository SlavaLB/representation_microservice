from fastapi import APIRouter, HTTPException

from app.config.logger import log_parser
from fastapi.responses import JSONResponse


router = APIRouter(prefix='/api')


@router.get("/logs")
async def get_logs(limit: int = 100, level: str = None):
    """
    Получить логи в формате JSON
    Параметры:
    - limit: ограничение количества записей на уровень (по умолчанию 100)
    - level: конкретный уровень логирования (debug, info, warning, error)
    """
    try:
        levels = [level] if level else ['debug', 'info', 'warning', 'error']

        result = {}
        for log_level in levels:
            logs = log_parser.parse_log_file(log_level)
            # Ограничиваем количество записей и переворачиваем порядок (новые сверху)
            result[log_level] = logs[-limit:][::-1]

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка при чтении логов: {str(e)}")


@router.get("/logs_levels")
async def get_log_levels():
    """Получить доступные уровни логирования"""
    levels = ['debug', 'info', 'warning', 'error']
    return {"available_levels": levels}


@router.get("/logs_stats")
async def get_log_stats():
    """Получить статистику по логам"""
    stats = {}
    total_entries = 0

    for level in ['debug', 'info', 'warning', 'error']:
        log_file = log_parser.log_dir / f"{level}.log"
        if log_file.exists():
            with open(log_file, 'r', encoding='utf-8') as f:
                count = sum(1 for _ in f)
                stats[level] = count
                total_entries += count
        else:
            stats[level] = 0

    return {
        "statistics": stats,
        "total_entries": total_entries
    }