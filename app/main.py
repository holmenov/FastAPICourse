from contextlib import asynccontextmanager
from fastapi import FastAPI
import uvicorn
import sys
import logging
from pathlib import Path
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

sys.path.append(str(Path(__file__).parent.parent))

logging.basicConfig(level=logging.INFO)

from app.init import redis_manager  # noqa: E402
from app.api.cars import router as cars_router  # noqa: E402
from app.api.car_models import router as car_models_router  # noqa: E402
from app.api.auth import router as auth_router  # noqa: E402
from app.api.bookings import router as bookings_router  # noqa: E402
from app.api.features import router as features_router  # noqa: E402
from app.api.images import router as images_router  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi_cache")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(cars_router)
app.include_router(car_models_router)
app.include_router(bookings_router)
app.include_router(features_router)
app.include_router(images_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
