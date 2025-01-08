from fastapi import HTTPException
from openai import OpenAI
from openai import OpenAIError

from app.core.config import settings


class OpenAIClient:
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_code(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                max_tokens=10,
                temperature=0,
            )
            return response.choices[0].message.content

        except OpenAIError as e:
            if e.status_code == 429:
                raise HTTPException(
                    status_code=e.response.status_code,
                    detail=f"OpenIA rate limit error: {e.code}",
                )

            raise HTTPException(
                status_code=e.response.status_code, detail=f"Openia error: {e.code}"
            )
