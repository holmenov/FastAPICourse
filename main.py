from fastapi import FastAPI, Body, Query
from cars import router as cars_router
import uvicorn


app = FastAPI()
app.include_router(cars_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)