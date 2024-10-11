from app.schemas.cars import SCarsData
from app.utils.db_manager import DBManager


async def test_add_car(db):
    car_data = SCarsData(mark="Chery")
    new_car_data = await db.cars.add(car_data)
    await db.commit()