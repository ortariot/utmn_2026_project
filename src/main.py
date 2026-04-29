from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api.v1.misk import router as misk_router
from api.v1.charendpoints import router as char_router
from api.v1.authendpoint import router as auth_router
from api.v1.aiendpoints import router as ai_router


@asynccontextmanager
async def lifspan(app: FastAPI):
    print("Startup init")

    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    yield

    print("Shutdown")

    redis.close()


app = FastAPI(
    docs_url="/api/docs", openapi_url="/api/openapi.json", lifespan=lifspan
)


app.include_router(misk_router, prefix="/api/v1/misk", tags=["misk"])
app.include_router(char_router, prefix="/api/v1/char", tags=["char"])
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(ai_router, prefix="/api/v1/ai", tags=["ai"])


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
