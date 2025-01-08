from app.core.dependencies import get_openai_client
from app.core.dependencies import get_redis_client


def test_dependencies():
    redis_client = get_redis_client()
    openai_client = get_openai_client()

    assert redis_client is not None
    assert openai_client is not None
