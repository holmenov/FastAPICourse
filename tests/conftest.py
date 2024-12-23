# ruff: noqa: E402
import json
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

import pytest
from httpx import AsyncClient, ASGITransport

from app.api.dependencies import get_db
from app.config import settings
from app.database import engine_null_pool, Base, async_session_maker_null_pool
from app.main import app
from app.schemas.car_models import SCarModelsData
from app.schemas.cars import SCarsData
from app.utils.db_manager import DBManager


@pytest.fixture(scope="session", autouse=True)
def check_db_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> DBManager:
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        yield db


@pytest.fixture(scope="function")
async def db() -> DBManager:
    async for db in get_db_null_pool():
        yield db


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def setup_db(check_db_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def setup_cars(setup_db):
    with open("tests/mock_cars.json", "r", encoding="utf-8") as json_data:
        cars_data = [car for car in json.load(json_data)]
    with open("tests/mock_car_models.json", "r", encoding="utf-8") as json_data:
        car_models_data = [car_model for car_model in json.load(json_data)]

    cars = [SCarsData.model_validate(car) for car in cars_data]
    car_models = [SCarModelsData.model_validate(car_model) for car_model in car_models_data]

    async with DBManager(session_factory=async_session_maker_null_pool) as _db:
        await _db.cars.add_bulk(cars)
        await _db.car_models.add_bulk(car_models)
        await _db.commit()


@pytest.fixture(scope="session")
async def ac() -> AsyncClient:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def register_user(setup_db, ac):
    await ac.post(
        "/auth/register",
        json={
            "email": "test@test.com",
            "password": "test",
            "first_name": "test",
            "nickname": "test",
        },
    )


@pytest.fixture(scope="session")
async def authenticated_ac(register_user, ac) -> AsyncClient:
    await ac.post(
        "/auth/login",
        json={
            "email": "test@test.com",
            "password": "test",
        },
    )
    assert ac.cookies["access_token"]
    yield ac
