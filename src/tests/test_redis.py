import pytest
from fastapi import Depends
from app.core.dependencies import get_redis_client
from app.core.dependencies import get_redis_connection
from clients.redis import RedisClient


@pytest.fixture
async def redis_connection():
    redis = await get_redis_connection()
    yield redis
    await redis.close()


async def test_cache_review(redis_connection: RedisClient):
    await redis_connection.setex("review_key", 3600, "review_data")
    cached_data = await redis_connection.get("review_key")
    assert cached_data.decode() == "review_data"
