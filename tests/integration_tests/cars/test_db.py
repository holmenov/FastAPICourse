from app.database import async_session_maker_null_pool
from app.schemas.cars import SCarsData
from app.utils.db_manager import DBManager


async def test_add_car():
    async with DBManager(session_factory=async_session_maker_null_pool) as db:
        car_data = SCarsData(mark="Chery")
        new_car_data = await db.cars.add(car_data)
        await db.commit()