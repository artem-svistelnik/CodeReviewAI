from pydantic import ConfigDict
from pydantic import Field
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "code-review-ai"
    DEBUG: int = 0
    BACKEND_CORS_ORIGINS: list[str] = Field(default_factory=list)
    SERVER_PORT: int = 8080
    SERVER_HOST: str = "0.0.0.0"
    RELOAD_ON_CHANGE: bool = True
    BASE_URL: str = "http://0.0.0.0:8080"
    ROOT_PATH: str = ""
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379
    REDIS_USER: str = ""
    REDIS_PASSWORD: str = ""
    GITHUB_TOKEN: str = ""
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = ""

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v

    model_config = ConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
