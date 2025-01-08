from unittest.mock import AsyncMock

import pytest


@pytest.fixture
def mock_openai_client():
    mock_client = AsyncMock()
    mock_client.analyze_code.return_value = "Mocked OpenAI response"
    return mock_client


async def test_openai_client(mock_openai_client):
    prompt = "Test prompt"
    result = await mock_openai_client.analyze_code(prompt)
    assert result == "Mocked OpenAI response"
    mock_openai_client.analyze_code.assert_called_once_with(prompt)
