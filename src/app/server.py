import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvloop

from app.core.config import settings
from app.core.dependencies import redis_client

from routes import include_routes


def get_application():
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    uvloop.install()
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        root_path=settings.ROOT_PATH,
    )
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_routes(_app)

    @_app.on_event("startup")
    async def startup():
        await redis_client.connect()

    @_app.on_event("shutdown")
    async def shutdown():
        await redis_client.close()

    return _app


app = get_application()
