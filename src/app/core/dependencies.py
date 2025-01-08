from clients.redis import RedisClient
from clients.github import GitHubClient
from clients.openai import OpenAIClient

redis_client = RedisClient()


def get_redis_client() -> RedisClient:
    return redis_client


async def get_redis_connection():
    redis = get_redis_client()
    return await redis.get_connection()


def get_github_client() -> GitHubClient:
    return GitHubClient()


def get_openai_client() -> OpenAIClient:
    return OpenAIClient()
