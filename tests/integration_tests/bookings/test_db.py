from datetime import date

from app.schemas.bookings import SBookingsAdd


async def test_booking_crud(db):
    car_model_id = (await db.car_models.get_all())[0].id
    user_id = (await db.users.get_all())[0].id
    booking_data = SBookingsAdd(
        date_from = date(year=2024, month=10, day=10),
        date_to = date(year=2024, month=10, day=20),
        car_id = int(car_model_id),
        user_id = int(user_id),
        price = 5000
    )
    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.model_dump(exclude={"id"}) ==  booking_data.model_dump()

    new_booking_data = SBookingsAdd(
        date_from = date(year=2024, month=10, day=10),
        date_to = date(year=2024, month=10, day=25),
        car_id = int(car_model_id),
        user_id = int(user_id),
        price = 5000
    )
    await db.bookings.edit(new_booking_data, id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking.model_dump(exclude={"id"}) ==  new_booking_data.model_dump()

    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking

    await db.commit()