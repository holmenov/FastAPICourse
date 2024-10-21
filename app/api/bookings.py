from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body
from fastapi.exceptions import HTTPException

from app.api.dependencies import DBDep, UserIdDep
from app.exceptions import check_date_to_after_date_from, ObjectAlreadyExistException, CarAlreadyBookedException
from app.schemas.bookings import SBookingsAdd, SBookingsAddRequest


router = APIRouter(prefix="/bookings", tags=["Бронирование автомобилей"])


@router.get("/all", summary="Получить все бронирования")
@cache(expire=10)
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"success": True, "data": bookings}


@router.get("/me", summary="Получить свои бронирования")
@cache(expire=10)
async def get_self_bookings(db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_all(user_id=user_id)
    return {"success": True, "data": bookings}


@router.post("", summary="Создание бронирование")
async def create_booking(db: DBDep, user_id: UserIdDep, data: SBookingsAddRequest = Body()):
    check_date_to_after_date_from(data.date_from, data.date_to)
    requested_car = await db.car_models.get_one_or_none(id=data.car_id)
    if requested_car is None:
        raise HTTPException(status_code=404, detail="Автомобиль по заданным параметрам не найден")

    is_car_booked = await db.bookings.get_filtered_by_time(
        data.car_id, data.date_from, data.date_to
    )
    if is_car_booked:
        raise CarAlreadyBookedException

    _data = SBookingsAdd(user_id=user_id, price=requested_car.price, **data.model_dump())
    
    try:
        booking = await db.bookings.add(_data)
    except ObjectAlreadyExistException as ex:
        raise CarAlreadyBookedException

    await db.commit()
    return {"success": True, "data": booking}
