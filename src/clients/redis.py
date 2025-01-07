import logging
from redis.asyncio import Redis
from redis.exceptions import RedisError
from app.core.config import settings


class RedisClient:
    def __init__(self, db: int = 0):
        self.db = db
        self.redis_connection: Redis = None

    async def connect(self):
        self.redis_connection = Redis(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=self.db,
            username=settings.REDIS_USER,
        )
        try:
            await self.redis_connection.ping()
        except RedisError as e:
            logging.error(f"Redis connection error: {e}")
            raise

    async def close(self):
        if self.redis_connection:
            await self.redis_connection.close()

    async def get_connection(self) -> Redis:
        if not self.redis_connection:
            await self.connect()
        return self.redis_connection
