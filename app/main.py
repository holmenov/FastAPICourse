from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.api.cars import router as cars_router
from app.api.car_models import router as car_models_router
from app.api.auth import router as auth_router
from app.api.bookings import router as bookings_router
from app.api.features import router as features_router


app = FastAPI()
app.include_router(auth_router)
app.include_router(cars_router)
app.include_router(car_models_router)
app.include_router(bookings_router)
app.include_router(features_router)


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000)