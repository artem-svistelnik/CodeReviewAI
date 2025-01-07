from fastapi import Depends

from clients.redis import RedisClient

redis_client = RedisClient()


def get_redis_client() -> RedisClient:
    return redis_client


async def get_redis_connection(redis: RedisClient = Depends(get_redis_client)):
    return await redis.get_connection()
