from datetime import datetime

from fastapi import APIRouter
from fastapi import Depends
from app.core.dependencies import get_redis_connection


health_router = APIRouter(prefix="/health", tags=["Health"])


@health_router.get("")
async def health_check(redis=Depends(get_redis_connection)):
    try:
        current_time = await redis.time()
        timestamp = current_time[0] + current_time[1] / 1_000_000
        formatted_time = datetime.utcfromtimestamp(timestamp).isoformat()
        return {"status": "OK", "current_time": formatted_time}
    except Exception as exc:
        return {"status": "ERROR", "message": str(exc)}
