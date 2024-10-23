from app.exceptions import BookingsNotFoundException, check_date_to_after_date_from, ObjectNotFoundException, \
    CarNotFoundException, CarAlreadyBookedException, ObjectAlreadyExistException
from app.schemas.bookings import SBookingsAddRequest, SBookingsAdd
from app.service.base import BaseService


class BookingsService(BaseService):
    async def get_self_bookings(self, user_id: int):
        bookings = await self.db.bookings.get_all(user_id=user_id)
        if not bookings:
            raise BookingsNotFoundException
        return bookings

    async def create_booking(self, user_id: int, data: SBookingsAddRequest):
        check_date_to_after_date_from(data.date_from, data.date_to)
        try:
            requested_car = await self.db.car_models.get_one(id=data.car_id)
        except ObjectNotFoundException as ex:
            raise CarNotFoundException from ex
        
        is_car_booked = await self.db.bookings.get_filtered_by_time(
            data.car_id, data.date_from, data.date_to
        )
        if is_car_booked:
            raise CarAlreadyBookedException
        
        _data = SBookingsAdd(user_id=user_id, price=requested_car.price, **data.model_dump())
        booking = await self.db.bookings.add(_data)
        await self.db.commit()

        return booking
