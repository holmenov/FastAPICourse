import json

import pytest
from httpx import AsyncClient, ASGITransport

from app.config import settings
from app.database import engine_null_pool, Base
from app.main import app


@pytest.fixture(scope='session', autouse=True)
def check_db_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope='session', autouse=True)
async def setup_cars():
    with open("tests/mock_cars.json", "r") as json_data:
        cars_data = [car for car in json.load(json_data)]
    with open("tests/mock_car_models.json", "r") as json_data:
        car_models_data = [car_model for car_model in json.load(json_data)]

    transport = ASGITransport(app=app)

    for car in cars_data:
        async with AsyncClient(transport=transport, base_url='http://testserver') as ac:
            await ac.post("/cars", json=car)

    for car_model in car_models_data:
        async with AsyncClient(transport=transport, base_url='http://testserver') as ac:
            url = f"/cars/{car_model['car_mark_name']}/models"
            del car_model['car_mark_name']
            await ac.post(url=url, json=car_model)


@pytest.fixture(scope='session', autouse=True)
async def setup_db(check_db_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='session', autouse=True)
async def register_user(setup_db):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url='http://testserver') as ac:
        await ac.post(
            "/auth/register",
            json={
                "email": "test@test.com",
                "password": "test",
                "first_name": "test",
                "nickname": "test",
            }
        )