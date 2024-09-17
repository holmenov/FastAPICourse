from fastapi import FastAPI
import uvicorn

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from app.api.cars import router as cars_router
from app.config import settings


app = FastAPI()
app.include_router(cars_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)