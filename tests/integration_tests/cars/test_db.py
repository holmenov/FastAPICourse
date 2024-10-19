from app.schemas.cars import SCarsData


async def test_add_car(db):
    car_data = SCarsData(mark="Chery")
    await db.cars.add(car_data)
    await db.commit()