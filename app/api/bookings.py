from datetime import date

from fastapi_cache.decorator import cache
from fastapi import APIRouter, Body, Query
from fastapi.exceptions import HTTPException

from app.api.dependencies import DBDep, UserIdDep, PaginationDep
from app.schemas.bookings import SBookingsAdd, SBookingsAddRequest


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирование автомобилей"]
)


@router.get("/all", summary="Получить все бронирования")
@cache(expire=10)
async def get_bookings(db: DBDep):
    bookings = await db.bookings.get_all()
    return {"success": True, "data": bookings}


@router.get("/me", summary="Получить свои бронирования")
@cache(expire=10)
async def get_self_bookings(db: DBDep, user_id: UserIdDep):
    bookings = await db.bookings.get_one_or_none(user_id=user_id)
    return {"success": True, "data": bookings}


@router.post("", summary="Создание бронирование")
async def create_booking(db: DBDep, user_id: UserIdDep, data: SBookingsAddRequest = Body()):
    requested_car = await db.car_models.get_one_or_none(id=data.car_id)
    if requested_car is None:
        raise HTTPException(status_code=404, detail="Такого авто не существует")
    
    is_car_booked = await db.bookings.get_filtered_by_time(
        data.car_id, data.date_from, data.date_to
    )
    if is_car_booked:
        raise HTTPException(status_code=409, detail="Выбранный автомобиль на эти даты уже забронирован")
    
    _data = SBookingsAdd(user_id=user_id, price=requested_car.price, **data.model_dump())
    booking = await db.bookings.add(_data)
    await db.commit()
    return {"success": True, "data": booking}